import numpy as np
import time 
import os  
import xarray as xr
import subprocess 
import pickle 
from datetime import datetime
# datetime object containing current date and time

now = datetime.now()
print("now =", now)
# dd/mm/YY H:M:S
t_string = now.strftime("%y%m%d%H%M") 

file_path1 = '/scratch/gpfs/cw55/AM4/work/CTL2000_test2000s_nn_stellarcpu_intelmpi_22_768PE/'
file_path2 = '/scratch/gpfs/cw55/AM4/work/CTL2000_test2000s_nn_stellarcpu_intelmpi_22_768PE_base/'
year_list = np.arange(1996,2005)

nn_ratio = np.zeros((2,7,len(year_list)*12))

for yi, year in enumerate(year_list):
    for fi, fp in enumerate([file_path1, file_path2]):
        print(year)
        for ti in range(1,7):
            now = datetime.now()
            print("now =", now)
            ds = xr.open_dataset(fp+f'/HISTORY/{year}0101.atmos_8xdaily.tile{ti}.nc')    
            data = ds['nn_lwup_sfc'].load()
            for mi in range(12):
                time_sel = data.time.dt.month.isin([mi+1])
                tmp = data.isel(time=time_sel).values
                tmp = np.where(tmp<0, 1, 0 )
                tmp_count = np.sum(tmp)
                # print(tmp, data.size, f'{tmp/data.size*100:5.2f}%')
                nn_ratio[fi,ti-1,yi*12+mi] = tmp_count/tmp.size*100
        ds = xr.open_dataset(fp+f'/POSTP/{year}0101.atmos_8xdaily.nc')  
        data = ds['nn_lwup_sfc'].load()
        for mi in range(12):
            time_sel = data.time.dt.month.isin([mi+1])
            tmp = data.isel(time=time_sel).values
            tmp = np.where(tmp<0, 1, 0 )
            tmp_count = np.sum(tmp)
            # print(tmp, data.size, f'{tmp/data.size*100:5.2f}%')
            nn_ratio[fi,6,yi*12+mi] = tmp_count/tmp.size*100 
        
now = datetime.now()
print("now =", now) 

pickle.dump( [year_list,nn_ratio], open( f"nn_ratio.train_good_init.{t_string}.p", "wb" ) )

