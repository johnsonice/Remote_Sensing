#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  5 14:20:09 2022

@author: huang
"""
## export data from ee

import ee
#import ssl
import time,sys
#from pathlib import Path
import numpy as np
import pandas as pd
#from .utils import load_clean_yield_data as load

def _append_im_band(current, previous):
    # Transforms an Image Collection with 1 band per Image into a single Image with items as bands
    # Author: Jamie Vleeshouwer

    # Rename the band
    previous = ee.Image(previous)
    current = current.select([0, 1, 2, 3, 4, 5, 6])
    # Append it to the result (Note: only return current item on first element/iteration)
    return ee.Algorithms.If(
        ee.Algorithms.IsEqual(previous, None),
        current,
        previous.addBands(ee.Image(current)),
    )


def _export_one_image(processed_img,folder,name,region=None,
                      scale=None,crs=None,crsTransform=None,
                      fileFormat='GeoTIFF',maxPixels=1e13,log_interval=10):
    
    args = {
        'image': processed_img.toFloat(),
        'description': name,
        'folder':folder,   ## it will create a folder an dump the image there 
        #'fileNamePrefix':"{}/{}".format(prefix,fname),
        'fileFormat':fileFormat,
        'maxPixels':maxPixels,
        }
    if scale:
        args['scale']=scale
    if crs:
        args['crs']=crs
    if crsTransform:
        args['crsTransform']=crsTransform
    if region:
        args['region']=region
    
    
    # Export the image, specifying scale and region.
    task = ee.batch.Export.image.toDrive(**args)
    task.start()
    
    timelapse = 0
    while task.active():
      #print('Working {}, {}s '.format(name,timelapse),end='\r')
      b = 'Working on {}, time used: {}s '.format(name,timelapse)
      sys.stdout.write("\r" + str(b))
      time.sleep(log_interval)
      timelapse += log_interval

    print('{} status: {}'.format(name,task.status()['state']))
    return task.status()

def _get_test_image():
    l8 = ee.ImageCollection('LANDSAT/LC08/C01/T1')
    countries = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017");
    Country = countries.filter(ee.Filter.eq("country_co","BF")); #try the bahamas
    landsat = l8.filterDate('2019-01-01', '2019-10-31') \
                .filterBounds(Country) 
    ## this is a cloud masking method in EE
    composite = ee.Algorithms.Landsat.simpleComposite(**{
      'collection': landsat,
      'asFloat': True
    })
    
    return composite,Country

def _get_regions():
    region = ee.FeatureCollection("TIGER/2018/Counties")
    # turn the strings into numbers, see
    # https://developers.google.com/earth-engine/datasets/catalog/TIGER_2018_Counties
    def county_to_int(feature):
        return feature.set("COUNTYFP", ee.Number.parse(feature.get("COUNTYFP")))
    
    def state_to_int(feature):
        return feature.set("STATEFP", ee.Number.parse(feature.get("STATEFP")))
    
    region = region.map(county_to_int)
    region = region.map(state_to_int)
    
    return region

def export():
    
    return None

#%%

if __name__ == "__main__":
    

    ee.Initialize()
    TEST = False
    
    if TEST:
        test_img,region = _get_test_image()
        projection = test_img.select(0).projection().getInfo();
        crs = projection['crs']
        crsTransform = projection['transform']
        folder = 'GEE_Test'
        name = 'test'
        
        status = _export_one_image(test_img,folder,name,
                          region=region.geometry(),scale=None,
                          crs=crs,crsTransform=crsTransform,
                          fileFormat='GeoTIFF',maxPixels=1e13,
                          log_interval=10)
        if status['state']!= 'COMPLETED':
            raise Exception('test download failed, check script!')
        
    
    #%%
    folder_name = 'GEE_Resources_Crop_Yield'
    locations_filepath="data/yield_data.csv"
    collection_id="MODIS/061/MOD09A1"
    scale=500
    MAJOR_STATES = [5, 17, 18, 19, 20, 27, 29, 31, 38, 39, 46]
    #%%
    imgcoll = ee.ImageCollection(collection_id) \
        .filterBounds(ee.Geometry.Rectangle(-106.5, 50, -64, 23)) \
        .filterDate("2002-12-31", "2016-8-4")
    # Get the number of images.
    count = imgcoll.size()
    print('Count: ', str(count.getInfo())+'\n')
    #%%
    img = imgcoll.iterate(_append_im_band)
    img = ee.Image(img)
    print(len(img.getInfo()['bands']))
    print(count.getInfo()*7)
    
    projection = img.select(['sur_refl_b01', 'sur_refl_b04', 'sur_refl_b03']).projection().getInfo()
    crs = projection['crs']
    crsTransform = projection['transform']
    region = _get_regions() ## get use state and county vector file 
    #%%
    df = pd.read_csv(locations_filepath) ## get yield data 
    county_data = np.unique(df[["State ANSI", "County ANSI"]].values, axis=0)
    county_data = [i for i in county_data if not pd.isna(i[1])] 
    if MAJOR_STATES:
        county_data = [i for i in county_data if i[0] in MAJOR_STATES] 
        
    #%%
    results = []
    for state_id, county_id in county_data:
        fname = "{}_{}".format(int(state_id), int(county_id))
        file_region = region.filterMetadata(
            "COUNTYFP", "equals", int(county_id)
            ).filterMetadata("STATEFP", "equals", int(state_id))
        
        file_region = ee.Feature(file_region.first())
        processed_img = img.clip(file_region)
        # Export the image, specifying scale and region.
        try:
            status = _export_one_image(processed_img,folder_name,fname,
                              region=file_region.geometry(),scale=scale,
                              crs=crs,crsTransform=crsTransform,
                              fileFormat='GeoTIFF',maxPixels=1e13,
                              log_interval=10)
            
        except Exception as e:
            print(e)
            status = 'error'
            
        results.append(status)
        
    
    print('Finished : {} files'.format(len(results)))
        
            
            
        
