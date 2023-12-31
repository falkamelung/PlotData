#! /usr/bin/env python3
import os
import argparse
import subprocess
import glob
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
    # parser = create_argument_parser(name, synopsis=synopsis, description=synopsis, epilog=epilog, subparsers=subparsers)
    parser = argparse.ArgumentParser(description=synopsis, epilog=epilog)
    
    line_file = os.getenv('RSMASINSAR_HOME') + '/tools/plotdata' + '/data/hawaii_lines_new.mat'

    parser.add_argument('data_dir', nargs='*', help='Directory(s) with InSAR data.\n')
    parser.add_argument('--plot-box',  nargs='?', dest='plot_box', type=str, default='19.29:19.6,-155.79:-155.41',
                        help='geographic area plotted')
    parser.add_argument('--period', dest='period', default='20220101-20221101', help='time period (20220101-20221101)')    
    parser.add_argument('--seismicity', dest='flag_seismicity', action='store_true', default=False, help='flag to add seismicity')
    parser.add_argument('--GPS', dest='flag_gps', action='store_true', default=False, help='flag to add GPS vectors')
    parser.add_argument('--plot-type', dest='plot_type', default='velocity', help='Type of plot: velocity, horzvert, ifgram, step, shaded_relief (Default: velocity).')
    parser.add_argument('--lines', dest='line_file', default=line_file, help='fault file (Default: plotdata/data/hawaii_lines_new.mat)')
    parser.add_argument('--GPS-scale-fac', dest='gps_scale_fac', default=500, type=int, help='GPS scale factor (Default: 500)')
    parser.add_argument('--GPS-key-length', dest='gps_key_length', default=4, type=int, help='GPS key length (Default: 4)')
    parser.add_argument('--GPS-units', dest='gps_unit', default="cm", help='GPS units (Default: cm)')
    parser.add_argument('--unit', dest='unit', default="cm", help='InSAR units (Default: cm)')
    parser.add_argument('--fontsize', dest='font_size', default=12, type=int, help='fontsize for view.py (Default: 12)')

    parser.add_argument('--ref-point', dest='reference_lalo', type=str, default=False, help='reference point')
    parser.add_argument('--mask-thresh', dest='mask_vmin', type=float, default=0.7, help='coherence threshold for masking (Default: 0.7)')
    parser.add_argument('--vlim', dest='vlim', nargs=2, metavar=('VMIN', 'VMAX'), type=float, help='colorlimit')
    parser.add_argument('--save-gbis', dest='flag_save_gbis', action='store_true', default=False, help='save GBIS files')

    return parser

def cmd_line_parse(iargs=None):
    """Command line parser."""
    parser = create_parser()
    print('cmd_line_parse: iargs:',iargs)
    print('cmd_line_parse: parser:',parser)
    
    #import pdb; pdb.set_trace()
    args = parser.parse_args(args=iargs)
    print('cmd_line_parse: args:',args)
    print('cmd_line_parse: args.plot_box:',args.plot_box)

    if len(args.data_dir) < 1 or len(args.data_dir) > 2:
        parser.error('ERROR: You must provide 1 or 2 directory paths.')
        
    inps = args
    print('cmd_line_parse: inps.plot_box:',inps.plot_box)
    inps.plot_box = [float(val) for val in args.plot_box.replace(':', ',').split(',')]  # converts to plot_box=[19.3, 19.6, -155.8, -155.4]
    if inps.reference_lalo:
        reference_lalo = args.reference_lalo
        inps.reference_lalo = [float(val) for val in reference_lalo.split(',')]         # converts to reference_point=[19.3, -155.8]
    if inps.period:
        period = args.period
        inps.period = [val for val in period.split('-')]                                # converts to period=['20220101', '20221101']

    return inps

def is_jupyter():
    jn = True
    try:
        get_ipython()
    except:
        jn = False
    return jn

def get_file_names(path):
    """gets the youngest eos5 file. Path can be: 
    MaunaLoaSenAT124
    MaunaLoaSenAT124/mintpy/S1_qq.he5
    ~/onedrive/scratch/MaunaLoaSenAT124/mintpy/S1_qq.he5'
    """
    if os.path.isfile(path):
        eos_file = path
    elif os.path.isfile(os.getenv('SCRATCHDIR') + '/' + path):
        eos_file = os.getenv('SCRATCHDIR') + '/' + path
    else:
        if not 'mintpy' in path:
            files = glob.glob( path + '/mintpy/*.he5' )
        else:
            files = glob.glob( path + '/*.he5' )
        eos_file = max(files, key=os.path.getctime)

    keywords = ['SenDT', 'SenAT', 'CskAT', 'CskDT']
    elements = path.split(os.sep)   
    project_dir = None
    for element in elements:
        for keyword in keywords:
            if keyword in element:
                project_dir = element
                project_base_dir = element.split(keyword)[0]
                track_dir = keyword + element.split(keyword)[1]
                break
    
    geo_vel_file = eos_file.rsplit('/', 1)[0] + '/geo/geo_velocity.h5'
    geo_geometry_file = eos_file.rsplit('/', 1)[0] + '/geo/geo_geometryRadar.h5'

    out_geo_vel_file = project_base_dir + '/' + track_dir + '/geo_velocity.h5'

    return eos_file, geo_vel_file, geo_geometry_file, project_base_dir, out_geo_vel_file    

def prepend_scratchdir_if_needed(path):
    """ Prepends $SCRATCHDIR if path is project name (got complicated; neet to refactor) """

    path, mintpy_dir = remove_directory_containing_mintpy_from_path(path)
    path_obj = Path(path)

    if path_obj.is_file():
        raise Exception('ERROR: need to be directory: ' + path)
    if len(Path(path_obj).parts) == 1:
        path = os.getenv('SCRATCHDIR') + '/' + path
    if  mintpy_dir:
        path = path + '/' + mintpy_dir
   
    return path

def save_gbis_plotdata(eos_file, geo_vel_file, start_date_mod, end_date_mod):
    timeseries_file = eos_file.rsplit('/', 1)[0] + '/timeseries_tropHgt_demErr.h5'
    vel_file = geo_vel_file.replace('geo_','')
    geom_file = vel_file.replace('velocity','inputs/geometryRadar')
    print('eos_file', eos_file)

    cmd = f'timeseries2velocity.py {timeseries_file} --start-date {start_date_mod} --end-date {end_date_mod} --output {vel_file}' 
    cmd1 = f'save_gbis.py {vel_file} -g {os.path.dirname(eos_file)}/inputs/geometryRadar.h5' 
    print('timeseries2velocity command:',cmd)
    output = subprocess.check_output(cmd.split())
    print('ave_gbis command:',cmd1.split())
    output = subprocess.check_output(cmd1.split())

def remove_directory_containing_mintpy_from_path(path):
    mintpy_dir = None
    dirs = path.split('/')
    for i in range(len(dirs) - 1, -1, -1):
        dir = dirs[i]
        if 'mintpy' in dir:
            mintpy_dir = dir
            # Remove the directory and all subsequent directories
            dirs = dirs[:i]
            break
    cleaned_path = '/'.join(dirs)
    return cleaned_path,  mintpy_dir
  
def find_nearest_start_end_date(fname, start_date, end_date):
    ''' Find nearest dates to start and end dates given as YYYYMMDD '''
    
    dateList = HDFEOS(fname).get_date_list()
    
    start_date_int = int(start_date)
    end_date_int = int(end_date)
    
    if start_date_int < int(dateList[0]):
        raise Exception("USER ERROR: No date found earlier than ", start_date_int )
    if end_date_int > int(dateList[-1]):
        raise Exception("USER ERROR:  No date found later than ", end_date_int )
    
    # print ('start_date_int: ',start_date_int)
    for date in reversed(dateList):
        date_int = int(date)
        # print(date_int)
        if date_int <= start_date_int:
            mod_start_date = date
            # print("Date just before start date:", date)
            break
    # print ('start_date_int: ',start_date_int)
    for date in reversed(dateList):
        date_int = int(date)
        # print(date_int)
        if date_int <= end_date_int:
            mod_end_date = date
            # print("Date just before end date:", date)
            break
    
    #This works for the data after end date 
    # for date in dateList:
    #     date_int = int(date)
    #     if date_int >= end_date_int:
    #         mod_end_date = date
    #         # print("Date just after end date:", date)
    #         break

    print('###############################################')
    print(' Given start_date, end_date:', start_date, end_date) 
    print(' Found start_date, end_date:', mod_start_date, mod_end_date) 
    print('###############################################')

    return mod_start_date, mod_end_date
    
def get_data_type(file):
    dir = os.path.dirname(file)
    while 'Sen' not in os.path.basename(dir) and 'Csk' not in os.path.basename(dir):
        dir = os.path.dirname(dir)
        if dir == os.path.dirname(dir):  # Check if we have reached the root directory
            break
    if 'Sen' in os.path.basename(dir) or 'Csk' in os.path.basename(dir):
        #print("Directory containing 'Sen' or 'Csk':", dir)
        tmp = dir.split('Sen')[1][0] if 'Sen' in os.path.basename(dir) else dir.split('Csk')[1][0]
        direction = tmp[0]
        if direction == 'A':
            type = 'Asc'
        elif direction == 'D':
            type = 'Desc'
        else:
            raise Exception('USER ERROR: direction is not A or D -- exiting ')  
    else:
        #print("File does not contain 'Sen' or 'Csk':", file)
        if file == 'up.h5':
            type = 'Up'
        elif file == 'hz.h5':
            type = 'Horz'
        else:
            type = 'Dem'
            #raise Exception('ERROR: file not up.h5 or horz.h5 -- exiting: ' + file)  
           
    return type

def get_dem_extent(atr_dem):
    # get the extent which is required for plotting
    # [-156.0, -154.99, 18.99, 20.00]
    dem_extent = [float(atr_dem['X_FIRST']), float(atr_dem['X_FIRST']) + int(atr_dem['WIDTH'])*float(atr_dem['X_STEP']), 
        float(atr_dem['Y_FIRST']) + int(atr_dem['FILE_LENGTH'])*float(atr_dem['Y_STEP']), float(atr_dem['Y_FIRST'])] 
    return(dem_extent)     

