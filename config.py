#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 13:43:35 2022

@author: chengyu
"""

## config 
import os
user = os.uname()[1]

if user =='chengyu-desktop':
    DATA_ROOT = '/media/chengyu/Elements1/remote_sensing/data/'
else:
    DATA_ROOT = './data'
    
    
MAJOR_STATES = [5, 17, 18, 19, 20, 27, 29, 31, 38, 39, 46]

MODIS_DATA_FOLDER = os.path.join(DATA_ROOT,'MODIS')