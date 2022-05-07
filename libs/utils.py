#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 14:13:22 2022

@author: chengyu
"""

## utils 

import os,sys
import more_itertools as mit
import pandas as pd

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


def batch_data(seq,batch_size=None,n_batches=None):
    if batch_size and n_batches:
        raise Exception('batchsie and n batchs can not both be true')
    
    if batch_size:
        batches = list(mit.chunked(seq,batch_size))
    
    if n_batches:
        batches = [list(c) for c in mit.divide(n_batches,seq)]

    return batches 

if __name__ == "__main__":
    p = '/media/chengyu/Elements1/remote_sensing/data/MODIS'
    fs = get_all_files(p)
    #%%
    test_df = pd.DataFrame(zip(range(100),range(100)))
    batches = batch_data(test_df.values,2)