#!/usr/bin/env python3
############################################################
# Program is part of PlotData                              #
# Author: Falk Amelung, Dec 2023                           #
############################################################

import os
import sys
import re
import argparse
from minsar.objects import message_rsmas

############################################################
EXAMPLE = """example:
  cmd = 'plot_data.py --help'
        plot_data.py MaunaLoaSenDT87 --plot-type ifgram --seismicity --GPS
        plot_data.py MaunaLoaSenDT87 --plot-type shaded_relief --seismicity --GPS'
        plot_data.py MaunaLoaSenAT124 MaunaLoaSenDT87 --noseismicity --GPS'
        plot_data.py MaunaLoaSenAT124 MaunaLoaSenDT87 --ref-point 19.55,-155.45'
        plot_data.py MaunaLoaSenDT87/mintpy_5_20  --plot-type velocity'
        plot_data.py MaunaLoaSenDT87/mintpy_5_20 MaunaLoaSenAT124/mintpy_5_20 --plot-type horzvert --ref-point 19.55,-155.45 --period 20220801-20221127 --plot-box 19.43:19.5,-155.62:-155.55 --vlim -5 5 --save-gbis'
        plot_data.py MaunaLoaSenDT87/mintpy_5_20 MaunaLoaSenAT124/mintpy_5_20 --plot-type velocity --ref-point 19.55,-155.45 --period 20220801-20221127 --vlim -20 20 --save-gbis --GPS --seismicity --fontsize 14'
        plot_data.py MaunaLoaSenDT87/mintpy_5_20  --plot-type shaded-relief --GPS --GPS-scale-fac 200 --GPS-key-length 1'
        plot_data.py MaunaLoaSenDT87/mintpy_5_20  --plot-type shaded-relief --GPS --seismicity'
        plot_data.py MaunaLoaSenDT87/mintpy_5_20  --plot-type shaded-relief --plot-box 19.43:19.5,-155.62:-155.55  --seismicity'
        plot_data.py GalapagosSenDT128/mintpy  --plot-type=velocity --plot-box=-0.52:-0.28,-91.7:-91.4 --period=20200131-20231231 --GPS --seismicity'
        plot_data.py GalapagosSenDT128/mintpy GalapagosSenAT106/mintpy_orig  --plot-type=horzvert --plot-box=-1.0:-0.75,-91.55:-91.25 --period=20220101-20230831 --vlim -5 5'
        plot_data.py MaunaLoaSenDT87/mintpy_5_20 MaunaLoaSenAT124/mintpy_5_20 --plot-type velocity --ref-point 19.55,-155.45 --period 20220801-20221127 --vlim -20 20 --save-gbis --GPS --seismicity --fontsize 14'
        plot_data.py GalapagosSenDT128/mintpy  --plot-type=velocity --plot-box=-0.52:-0.28,-91.7:-91.4 --period=20200131-20221231 --GPS --seismicity'
"""

def create_parser():
    synopsis = 'Plotting of InSAR, GPS and Seismicity data'
    epilog = EXAMPLE
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

    inps = parser.parse_args()

    if len(inps.data_dir) < 1 or len(inps.data_dir) > 2:
        parser.error('USER ERROR: You must provide 1 or 2 directory paths.')
        
    print('create_parser: inps.plot_box:',inps.plot_box)
    inps.plot_box = [float(val) for val in inps.plot_box.replace(':', ',').split(',')]  # converts to plot_box=[19.3, 19.6, -155.8, -155.4]
    if inps.reference_lalo:
        reference_lalo = inps.reference_lalo
        inps.reference_lalo = [float(val) for val in reference_lalo.split(',')]         # converts to reference_point=[19.3, -155.8]
    if inps.period:
        period = inps.period
        inps.period = [val for val in period.split('-')]                                # converts to period=['20220101', '20221101']

    return inps

############################################################
def main():
    if len(sys.argv) == 1:
        # called without arguments (from vscode)
        cmd = 'plot_data.py GalapagosSenDT128/mintpy  --plot-type=velocity --plot-box=-0.52:-0.28,-91.7:-91.4 --period=20200131-20221231'
        cmd = os.path.expandvars(cmd)
        cmd = re.sub(' +', ' ', cmd) .rstrip()
        sys.argv = cmd.split()
    inps = create_parser()
    print('inps: ',inps)
    message_rsmas.log(os.getcwd(), os.path.basename(__file__) + ' ' + ' '.join(sys.argv[1:]))

    # import
    from prepare_plot import run_prepare
    from prepare_plot import run_plot
    
    os.chdir(os.getenv('SCRATCHDIR'))
    data_dict = run_prepare(inps)
    run_plot(data_dict, inps)

    return

    # return data_dict, inps, iargs
    # return None, None, None

############################################################
if __name__ == '__main__':
    main()
