#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 22:01:25 2022

@author: chengyu
"""

## run all exports 
## https://janakiev.com/blog/python-shell-commands/
## http://devres.zoomquiet.top/data/20181206151644/index.html

from subprocess import Popen, PIPE
import os,sys
try:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, os.path.join(dir_path,'..'))
except:
    sys.path.insert(0, '..')
import config

if __name__ == "__main__":
    n_jobs = 50
    
    ### construct cmds 
    #chdir = "cd {}".format(config.CODE_ROOT)
    # chdir = "cd {}".format('..')
    p_path = os.path.join(config.CODE_ROOT,'export_ee_images.py')
    cmd_lines = []
    for i in range(n_jobs):
        cmd_line = "python {} -b {}".format(p_path,'{}_{}'.format(i,n_jobs))
        #cmd_line = "{}&python export_ee_images.py -b {}".format(chdir,'{}_{}'.format(i,n_jobs))
        cmd_lines.append(cmd_line)
    #%%
    ## run all 
    Ps = []
    for c in cmd_lines:
        print(c)
        Ps.append(Popen(c, shell=True))