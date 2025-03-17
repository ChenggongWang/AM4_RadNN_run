import numpy as np 
import time 
import os  
import xarray as xr
import psutil
import gc

year_list = np.arange(1996,2005)
ori_var = [
 'olr',
 'lwdn_sfc',
 'swdn_sfc',
 'swup_sfc',
 'swup_toa',
 'tdt_lw',
 'tdt_sw',
 'tdt_lw_clr',
 'tdt_sw_clr',
 'olr_clr',
 'lwdn_sfc_clr',
 'swdn_sfc_clr',
 'swup_sfc_clr',
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
xe = np.arange(-4,4.01,0.2)
err_pred_hist = np.zeros(len(xe)-1)
err_pred_hist_err = np.zeros(len(xe)-1)
for year in year_list:
    for ti in range(1,7):
        # file_path = '/scratch/gpfs/cw55/AM4/work/CTL2000_test2000s_nn_stellarcpu_intelmpi_22_768PE/'
        # ds= xr.open_mfdataset([file_path+f'HISTORY/{year}0101.atmos_8xdaily.tile{ti}.nc' for year in year_list])  
        # ds_nn_3h = ds

        file_path = '/scratch/gpfs/cw55/AM4/work/CTL2000_test2000s_nn_stellarcpu_intelmpi_22_768PE/' 
        filename= file_path+f'HISTORY/{year}0101.atmos_8xdaily.tile{ti}.nc'

        zero_time = time.time()
        # file_stats = os.stat(filename)
        # print(f"Converting file: {filename} | Raw file size: {file_stats.st_size / (1024**3):5.1f} GB ")
        os.system(f'cp --parents {filename} /dev/shm/')
        print("loaded data into /dev/shm")
        with xr.open_dataset(f"/dev/shm/{filename}").isel(time=slice(None,-1)) as ds: 
            var_list=build_var_list(ds,ori_var)
            eng_err_check = ds['nn_lwup_sfc'].load()
            
            err_pred = {}
            for svar in ori_var:
                # warp operations in with statement to manage the memory better
                sta_time = time.time()
                print(f'Read {svar:12s} ...', end='')
                da = ds[svar].load()
                nnda = ds[f'nn_{svar}'].load() 
                # # Getting % usage of virtual_memory ( 3rd field)
                # print('RAM memory % used:', psutil.virtual_memory()[2],end = '| ')
                # # Getting usage of virtual_memory in GB ( 4th field)
                # print('RAM Used (GB):', psutil.virtual_memory()[3]/1e9)

                err_pred[svar] = abs(nnda - da)/(abs(da).mean(['time'])+1e-10)
                print(f' done. Use time: {time.time() - sta_time: 3.0f}s')
                del da, nnda
                # gc.collect()
        used_time = time.time() - zero_time  
        print(f'    | timer: {used_time:4.0f}s')
        os.system(f'rm -f  /dev/shm/{filename}')
        # calculate index
        err_pred_index = err_pred[ori_var[0]].copy()
        for svar in ori_var[1:]:
            if 'tdt' in svar:
                err_pred_index += err_pred[svar].sum('pfull')
                # pass
            else:
                err_pred_index += err_pred[svar]
                
        err_pred_index_log1 = np.log(err_pred_index.values.flatten()/142)/np.log(10)
        index_sel = np.argwhere(eng_err_check.values.flatten()<0)
        err_pred_index_log2 = err_pred_index_log1[index_sel]
        hist1,xe = np.histogram(err_pred_index_log1,xe)
        hist2,xe = np.histogram(err_pred_index_log2,xe)
        err_pred_hist     += hist1
        err_pred_hist_err += hist2

import pickle
with  open('error_eng_stats_hist_1996_2004_interactive.p', 'wb') as file:
    pickle.dump([xe,err_pred_hist,err_pred_hist_err],file)
