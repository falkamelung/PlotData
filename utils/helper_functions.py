#! /usr/bin/env python3
import os
from mintpy.utils import readfile, writefile
from mintpy.objects import HDFEOS
import numpy as np
from pathlib import Path

def prepend_scratchdir_if_needed(path):
    """ Prepends $SCRATCHDIR if path is project name """
    path_obj = Path(path)

    if path_obj.is_file():
        raise Exception('ERROR: need to be directory: ' + path)

    if len(Path(path_obj).parts)-1 == 0:
        path = os.getenv('SCRATCHDIR') + '/' + path
    return path

def find_nearest_start_end_date(fname, start_date, end_date):
    ''' Find nearest dates to start and end dates given as YYYYMMDD '''
    
    dateList = HDFEOS(fname).get_date_list()
    
    start_date_int = int(start_date)
    end_date_int = int(end_date)
    
    if start_date_int < int(dateList[0]):
        raise Exception("ERROR: No earlier date found than ", start_date_int )
    if end_date_int > int(dateList[-1]):
        raise Exception("ERROR:  No later date found than ", end_date_int )
    
    # print ('start_date_int: ',start_date_int)
    for date in reversed(dateList):
        date_int = int(date)
        # print(date_int)
        if date_int <= start_date_int:
            mod_start_date = date
            # print("Date just before start date:", date)
            break
            
    # print ('end_date_int: ',end_date_int)
    for date in dateList:
        date_int = int(date)
        # print(date_int)
        if date_int >= end_date_int:
            mod_end_date = date
            # print("Date just after end date:", date)
            break

    return mod_start_date, mod_end_date
    
def get_dem_extent(atr_dem):
    # get the extent which is required for plotting
    # [-156.0, -154.99, 18.99, 20.00]
    dem_extent = [float(atr_dem['X_FIRST']), float(atr_dem['X_FIRST']) + int(atr_dem['WIDTH'])*float(atr_dem['X_STEP']), 
        float(atr_dem['Y_FIRST']) + int(atr_dem['FILE_LENGTH'])*float(atr_dem['Y_STEP']), float(atr_dem['Y_FIRST'])] 
    return(dem_extent)     

