#! /usr/bin/env python3
import os
import argparse
from mintpy.utils import readfile, writefile
from mintpy.objects import HDFEOS
import numpy as np
from pathlib import Path

EXAMPLE = """example:
  plot_data.py  MaunaLoaSenDT87 MaunaLoaSenAT124 
  plot_data.py  MaunaLoaSenDT87       
"""

def create_parser(subparsers=None):
    synopsis = 'Plotting of InSAR, GPS and Seismicity data'
    epilog = EXAMPLE
    parser = argparse.ArgumentParser(description='Plot InSAR, GPS and seismicity data\n')

    line_file = os.path.dirname(os.path.abspath("__file__")) + '/data/hawaii_lines_new.mat'

    parser.add_argument('data_dir', nargs='*', help='Directory(s) with InSAR data.\n')

    parser.add_argument('--plotBox', '--subset-lalo', dest='plot_box', default='19.29:19.6,-155.79:-155.41',
                        help='geographic area plotted')
    parser.add_argument('--startDate', dest='start_date', default='20220801',help='start date')
    parser.add_argument('--endDate', dest='end_date', default='20221115',help='end date')
    parser.add_argument('--seismicity', dest='flag_seismicity', action='store_true', default=True,
                        help='flag to add seismicity')
    parser.add_argument('--noseismicity', dest='flag_noseismicity', action='store_true',default=False,
                        help='flag to remove seismicity')
    parser.add_argument('--gps', dest='flag_gps', action='store_true', default=True,
                        help='flag to add gps vectors')
    parser.add_argument('--nogps', dest='flag_nogps', action='store_true',default=False,
                        help='flag to remove gps vectors')
    parser.add_argument('--plotType', dest='plot_type', default='velocity',
                        help='Type of plot: velocity, ifgram, shaded_relief (Default: velocity).')
    parser.add_argument('--lines', dest='line_file', default=line_file, help='fault file')
    parser.add_argument('--gpsScaleFac', dest='gps_scale_fac', default=500, help='GPS scale factor')
    parser.add_argument('--gpsKeyLength', dest='gps_key_length', default=4, help='GPS key length')
    parser.add_argument('--gpsUnits', dest='gps_unit', default="cm", help='GPS units')
 
    args = parser.parse_args()
    
    if len(args.data_dir) < 1 or len(args.data_dir) > 2:
        parser.error('ERROR: You must provide 1 or 2 directory paths.')
    if len(args.data_dir) == 2:
        args.plot_type='horzvert'
    if args.flag_noseismicity:
       args.flag_seismicity = False
    del args.flag_noseismicity
    if args.flag_nogps:
       args.flag_gps = False
    del args.flag_nogps
    
    inps = args
    inps.plot_box = [float(val) for val in inps.plot_box.replace(':', ',').split(',')]  # converts to plot_box=[19.3, 19.6, -155.8, -155.4]

    #inps.argv = iargs if iargs else sys.argv[1:]

    return inps

def is_jupyter():
    jn = True
    try:
        get_ipython()
    except:
        jn = False
    return jn
    
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

    print('###############################################')
    print(' Given start_date, end_date:', start_date, end_date) 
    print(' Found start_date, end_date:', mod_start_date, mod_end_date) 
    print('###############################################')

    return mod_start_date, mod_end_date
    
def get_flight_direction(dir):
    direction = dir.split('Sen')[1][0]
    if direction == 'A':
        direction = 'Asc'
    elif direction == 'D':
        direction = 'Desc'
    else:
        raise Exception('ERROR: direction is not A or B -- exiting: ')  
    return direction


def get_dem_extent(atr_dem):
    # get the extent which is required for plotting
    # [-156.0, -154.99, 18.99, 20.00]
    dem_extent = [float(atr_dem['X_FIRST']), float(atr_dem['X_FIRST']) + int(atr_dem['WIDTH'])*float(atr_dem['X_STEP']), 
        float(atr_dem['Y_FIRST']) + int(atr_dem['FILE_LENGTH'])*float(atr_dem['Y_STEP']), float(atr_dem['Y_FIRST'])] 
    return(dem_extent)     

