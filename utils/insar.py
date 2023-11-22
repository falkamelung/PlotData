import os
import glob

def generate_view_ifgram_cmd(work_dir, date12, plot_box):
    ifgram_file = work_dir + '/geo_ifgramStack.h5'
    timeseries_file = work_dir + '/geo_timeseries_tropHgt_demErr.h5'
    geom_file = work_dir + '/geo_geometryRadar.h5'
    mask_file = work_dir + '/geo_maskTempCoh.h5'   # generated with generate_mask.py geo_geometryRadar.h5 height -m 3.5 -o waterMask.h5 option
    
    ## Configuration for InSAR background: check view.py -h for more plotting options.
    cmd = 'view.py {} unwrapPhase-{} -m {} -d {} '.format(ifgram_file, date12, mask_file, geom_file)
    cmd += f"--sub-lat {plot_box[0]} {plot_box[1]} --sub-lon {plot_box[2]} {plot_box[3]} "
    cmd += '--notitle -u cm -c jet_r --nocbar --noverbose '
    return cmd

def generate_view_velocity_cmd(vel_file,  plot_box):
    cmd = 'view.py {} velocity '.format(vel_file)
    cmd += f" --sub-lat {plot_box[0]} {plot_box[1]} --sub-lon {plot_box[2]} {plot_box[3]} "
    cmd += '--notitle -u cm -c jet_r --nocbar --noverbose' 
    return cmd

def generate_view_velocity2_cmd(vel_file, mask_file, plot_box):
    cmd = 'view.py {} velocity -m {}'.format(vel_file, mask_file)
    cmd += f" --sub-lat {plot_box[0]} {plot_box[1]} --sub-lon {plot_box[2]} {plot_box[3]} "
    cmd += '--notitle -u cm -c jet_r --nocbar --noverbose' 
    return cmd
    
def get_eos_file(path):
    """gets the youngest eos5 file. Path can be: 
    MaunaLoaSenAT124
    ~/onedrive/scratch/MaunaLoaSenAT124/mintpy/S1_IW23_124_0059_0063_20180905_XXXXXXXX_N19122_N19785_W155940_W155223.he5'
    MaunaLoaSenAT124/mintpy/S1_qq.he5
    """
    if os.path.isfile(path):
        eos_file = path
    elif os.path.isfile(os.getenv('SCRATCHDIR') + '/' + path):
        eos_file = os.getenv('SCRATCHDIR') + '/' + path
    else:
        files = glob.glob(os.getenv('SCRATCHDIR') + '/' + path + '/mintpy/*.he5')
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
    
    vel_file = project_base_dir + '/' + track_dir + '/geo_velocity.h5'

    return eos_file, project_base_dir, vel_file