import xarray as xr  
import time 
import argparse, sys
import os 
import time
import psutil
import gc
ori_var = [
 'lwdn_sfc',
 'swdn_sfc',
 'swup_sfc',
 'olr',
 'swdn_toa',
 'swup_toa',
 'tdt_lw',
 'tdt_sw',
 'tdt_lw_clr',
 'tdt_sw_clr',
 'lwdn_sfc_clr',
 'swdn_sfc_clr',
 'swup_sfc_clr',
 'olr_clr',
 'swup_toa_clr',]
def build_var_list(ds, orivar):
    err_var = []
    for _ in orivar:
        if _ in list(ds.variables) : 
            # check nn var
            if f'nn_{_}' in list(ds.variables) : 
                err_var.append(_) 
            else:
                print(f'nn_{_} do not exist in data file. Please check!')
        else:
            print(f'{_} do not exist in data file. Please check!')
    return err_var

if __name__ == '__main__':  
    ##################################################### 
    parser=argparse.ArgumentParser()
    parser.add_argument("--filename", help="filepattern, hourly, daily file name before .nc") 
    args=parser.parse_args()
    filename = args.filename 
    # file_path = '/scratch/gpfs/cw55/AM4/work/CTL2000_sst0.5Kperyear_nn_stellarcpu_intelmpi_22_768PE_base/'
    # filename = file_path+f'POSTP/19810101.atmos_8xdaily.nc'
    
    zero_time = time.time()
    file_stats = os.stat(filename)
    print(f"Converting file: {filename} | Raw file size: {file_stats.st_size / (1024**3):5.1f} GB ")
    os.system(f'cp --parents {filename} /dev/shm/')
    print("load data into /dev/shm")
    with xr.open_dataset(f"/dev/shm/{filename}") as ds: 
        var_list=build_var_list(ds,ori_var)
        lwup_sfc = ds['nn_lwup_sfc'].load()
        ds_new = lwup_sfc.groupby('time.month').mean('time').to_dataset()
    for svar in var_list:
        # warp operations in with statement to manage the memory better
        with xr.open_dataset(f"/dev/shm/{filename}") as ds: 
            sta_time = time.time()
            print(f'Read {svar:12s} ...', end='')
            ## Getting % usage of virtual_memory ( 3rd field)
            #print('RAM memory % used:', psutil.virtual_memory()[2],end = '')
            ## Getting usage of virtual_memory in GB ( 4th field)
            #print('RAM Used (GB):', psutil.virtual_memory()[3]/1000000000)
            da = ds[svar].load()
            nnda = ds[f'nn_{svar}'].load() 
            ds_new[svar]         = da.groupby('time.month').mean('time')
            ds_new[f'nn_{svar}'] = nnda.groupby('time.month').mean('time')
            ## Getting % usage of virtual_memory ( 3rd field)
            #print('RAM memory % used:', psutil.virtual_memory()[2],end = '')
            ## Getting usage of virtual_memory in GB ( 4th field)
            #print('RAM Used (GB):', psutil.virtual_memory()[3]/1000000000)
            #gc.collect()

            err = nnda - da
            del da, nnda
            ds_new[f'bias_{svar}'] = err.groupby('time.month').mean('time')
            ds_new[f'mae_{svar}']  = abs(err).groupby('time.month').mean('time')
            ds_new[f'rmse_{svar}'] = ((err**2).groupby('time.month').mean('time'))**0.5

            err_adj = xr.where(lwup_sfc<0,0,err)
            ds_new[f'adj_bias_{svar}'] = err_adj.groupby('time.month').mean('time')
            ds_new[f'adj_mae_{svar}']  = abs(err_adj).groupby('time.month').mean('time')
            ds_new[f'adj_rmse_{svar}'] = ((err_adj**2).groupby('time.month').mean('time'))**0.5
            print(f' done. Use time: {time.time() - sta_time: 3.0f}s')
            del err, err_adj
    # add time axis
    ds_new = ds_new.rename({'month':'time'}) 
    new_time = xr.concat([_[1][0] for _ in ds.time.groupby('time.month')],dim='time')
    ds_new['time'] = new_time
    ds_new['grid_xt'] = ds['grid_xt']
    ds_new['grid_yt'] = ds['grid_yt']
    if 'tile' in filename:
        new_filename = f"{filename[:-9]}.monavg_error.{filename[-8:]}"
    else:
        new_filename = f"{filename[:-3]}.monavg_error.nc"
    ds_new.to_netcdf(new_filename)
    file_stats_new = os.stat(new_filename)
    used_time = time.time() - zero_time  
    print(f'    | New Size: {file_stats_new.st_size / (1024**3):5.1f} GB | timer: {used_time:4.0f}s')
    os.system(f'rm -f  /dev/shm/{filename}')
    
# import xarray as xr  
# import time 
# import argparse, sys
# import os 

# if __name__ == '__main__':  
#     sta_time = time.time()
#     ##################################################### 
#     parser=argparse.ArgumentParser()
#     parser.add_argument("--filename", help="filepattern, hourly, daily file name before .nc") 
#     args=parser.parse_args()
#     filename = args.filename 

#     file_stats = os.stat(filename)
#     print(f"Converting file: {filename} | Raw file size: {file_stats.st_size / (1024**3):5.1f} GB ")
#     with xr.open_dataset(filename) as ds:
#         # ds = ds.load() # slower?
#         ds_new = ds.groupby('time.month').mean('time')
#         # add time axis
#         ds_new = ds_new.rename({'month':'time'}) 
#         new_time = xr.concat([_[1][0] for _ in ds.time.groupby('time.month')],dim='time')
#         ds_new['time'] = new_time
#         ds_new.to_netcdf(f"{filename}.monavg.nc")
#     used_time = time.time() - sta_time  
#     file_stats_new = os.stat(f"{filename}.monavg.nc")
#     print(f'    | New Size: {file_stats_new.st_size / (1024**3):5.1f} GB | timer: {used_time:4.0f}s')
