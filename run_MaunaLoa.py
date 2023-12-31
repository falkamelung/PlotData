#!/usr/bin/env python
# coding: utf-8

# ## Plot Sentinel InSAR data for Mauna Loa volcano
# This notebook does multiple calls of `plot_data.py` to visualize the displacement history. For options see `plot_data.py --help`. Modify the `cmd` line to test plot options.

# In[ ]:


import os
import sys
import urllib
import glob
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LinearSegmentedColormap
from mintpy.utils import readfile, writefile, utils as ut
from mintpy.defaults.plot import *
from mintpy.objects.gps import search_gps, GPS
from mintpy.objects import sensor
from mintpy.view import prep_slice, plot_slice
from mintpy.cli import view, timeseries2velocity, reference_point, asc_desc2horz_vert, save_gdal, mask
import plot_data
get_ipython().run_line_magic('load_ext', 'jupyter_ai')
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[ ]:


get_ipython().run_cell_magic('capture', '--no-display', "\ncmd = 'plot_data.py MaunaLoaSenDT87/mintpy_5_20 MaunaLoaSenAT124/mintpy_5_20 --period 20221127-20221219 --plot-type velocity --mask-thresh 0.90 --ref-point 19.55,-155.45 --unit m --vlim -8 8 --seismicity' \nplot_data.main(cmd.split()[1:])\n")


# In[ ]:


get_ipython().run_cell_magic('capture', '--no-display', "# Loop over multiple time periods\n######################################################\n################  FINAL: NO GPS ###################### \n### Two pre-eruption and two post-eruption periods ###\n######################################################\nadd_opt = ''\ncommon_opt='MaunaLoaSenDT87/mintpy_5_20 MaunaLoaSenAT124/mintpy_5_20 --plot-type velocity --mask-thresh 0.90 --ref-point 19.55,-155.45'\n# add_opt = '--GPS --seismicity --save-gbis'\nadd_opt = '--save-gbis --seismicity'\n\ncmd_list = [  \n                 '--period 20181012-20220821 --vlim -5 5' ,\n                 '--period 20220821-20221127 --vlim -25 25',\n            #    '--period 20221127-20221219 --vlim -8 8 --unit m',\n                 '--period 20221231-20230328 --vlim -33 33',\n                 '--period 20230328-20231110 --vlim -20 20'          \n        ] \n\nfor tok in cmd_list:\n    cmd=['plot_data.py ' + common_opt + ' ' + tok + ' ' + add_opt][0]\n    print(cmd)\n    print(cmd.split()[1:])\n    plot_data.main(cmd.split()[1:])\n")


# In[ ]:


get_ipython().run_cell_magic('capture', '--no-display', "# Loop over multiple time periods\n######################################################\n### Two pre-eruption and two post-eruption periods ###\n######################################################\nadd_opt = ''\ncommon_opt='MaunaLoaSenDT87/mintpy_5_20 MaunaLoaSenAT124/mintpy_5_20 --plot-type velocity --mask-thresh 0.90 --ref-point 19.55,-155.45'\nadd_opt = '--GPS --seismicity --save-gbis'\ncmd_list = [  \n                 '--period 20181012-20220821 --vlim -5 5   --GPS-scale-fac 500  --GPS-key-length 5  --GPS-units cm/yr',\n                 '--period 20220821-20221127 --vlim -25 25 --GPS-scale-fac 1200 --GPS-key-length 20 --GPS-units cm/yr',\n            #    '--period 20221127-20221219 --vlim -8 8 --unit m',\n                 '--period 20221231-20230328 --vlim -33 33 --GPS-scale-fac 1200 --GPS-key-length 20 --GPS-units cm/yr',\n                 '--period 20230328-20231110 --vlim -20 20 --GPS-scale-fac 1200 --GPS-key-length 20 --GPS-units cm/yr'          \n        ] \n\nfor tok in cmd_list:\n    cmd=['plot_data.py ' + common_opt + ' ' + tok + ' ' + add_opt][0]\n    print(cmd)\n    print(cmd.split()[1:])\n    plot_data.main(cmd.split()[1:])\n")


# In[ ]:


get_ipython().run_cell_magic('capture', '--no-display', "# Loop over multiple time periods\n######################################################\n### Two pre-eruption and two post-eruption periods ###\n######################################################\nadd_opt = ''\ncommon_opt='MaunaLoaSenDT87/mintpy_2_8_step MaunaLoaSenAT124/mintpy_2_8_step --plot-type step --mask-thresh 0.90 --ref-point 19.474,-155.597 --plot-box 19.45:19.475,-155.60:-155.57 --vlim -4 4'\nadd_opt = '--GPS --save-gbis'\ncmd_list = [  \n            '--plot-type step --period 20201001-20210306  --vlim -4 4'\n            ] \n\nfor tok in cmd_list:\n    cmd=['plot_data.py ' + common_opt + ' ' + tok + ' ' + add_opt][0]\n    print(cmd)\n    print(cmd.split()[1:])\n    plot_data.main(cmd.split()[1:])\n")


# In[ ]:


# %%capture --no-display
# ##################################
# ### Three pre-eruption periods ###
# ###### DON'T USE #################
# ##################################
# add_opt = ''
# common_opt='MaunaLoaSenDT87/mintpy_5_20  --plot-type shaded-relief --GPS'
# cmd_list = [  
#                  '--period 20181012-20220901 --GPS-scale-fac 500  --GPS-key-length 5  --GPS-units cm/yr'   ,
#                  '--period 20220901-20221015 --GPS-scale-fac 1000 --GPS-key-length 10 --GPS-units cm/yr'   ,
#                  '--period 20221015-20221127 --GPS-scale-fac 1000 --GPS-key-length 10 --GPS-units cm/yr'   
#    ] 
    # for tok in cmd_list:
#     cmd=['plot_data.py ' + common_opt + ' ' + tok + ' ' + add_opt][0]
#     print(cmd)
#     print(cmd.split()[1:])
#     plot_data.main(cmd.split()[1:])


# In[ ]:


# %%capture --no-display
# ##################################
# ### Time series (8 periods) ###
# ###### DON'T USE #################
# ##################################
# cmd_list = [  
#                  '--period 20181012-20220901 --GPS-scale-fac 500  --GPS-key-length 5  --GPS-units cm/yr',  
#                  '--period 20220901-20221126 --GPS-scale-fac 1200 --GPS-key-length 20 --GPS-units cm/yr',
#                  '--period 20221126-20221129 --GPS-scale-fac 3000 --GPS-key-length 50 --GPS-units cm',
#             ##   '--period 20221129-20221212 --GPS-scale-fac 1000 --GPS-key-length 20 --GPS-units cm',
#             ##   '--period 20221212-20221231 --GPS-scale-fac 2000 --GPS-key-length 20 --GPS-units cm/yr',
#                  '--period 20221129-20221231 --GPS-scale-fac 1000 --GPS-key-length 20 --GPS-units cm',
#                  '--period 20221231-20230331 --GPS-scale-fac 1200 --GPS-key-length 20 --GPS-units cm/yr',
#                  '--period 20230331-20230620 --GPS-scale-fac 1200 --GPS-key-length 20 --GPS-units cm/yr'      
#         ]   
# # cmd = 'plot_data.py MaunaLoaSenDT87/mintpy_5_20  --plot-type shaded-relief --GPS'
# for tok in cmd_list:
#     cmd=['plot_data.py ' + common_opt + ' ' + tok + ' ' + add_opt][0]
#     print(cmd)
#     print(cmd.split()[1:])
#     plot_data.main(cmd.split()[1:])


# In[ ]:


get_ipython().system('plot_data.py --help')

