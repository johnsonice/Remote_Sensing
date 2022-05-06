#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 14:13:22 2022

@author: chengyu
"""

## utils 

import os#,sys

def get_all_files(f_path,ext=None,name_only=False):
    res = []
    for root, dirs, files in os.walk(f_path):
        for file in files:
            if name_only:
                fp = file
            else:
                fp = os.path.join(root, file)
                
            if ext:
                if file.endswith(ext):
                     res.append(fp)
            else:
                res.append(fp)
    
    return res 

if __name__ == "__main__":
    p = '/media/chengyu/Elements1/remote_sensing/data/MODIS'
    fs = get_all_files(p)