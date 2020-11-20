#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: Multi CRS repojector
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de



Created on Thu Nov 19 21:14:11 2020
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
"""
from argparse import ArgumentParser
from tkinter import Tk,filedialog
import os
from tqdm import tqdm
import itertools
import gdal
import ogr 
from gdal import Warp, VectorTranslate    
from utils import get_paths, make_folder
from ipywidgets import IntProgress
import geopandas as gpd


def converter(file, OUT_CRS):
    
    xt = file.split('.')[1]
    name = os.path.basename(file)
    outfile = WORK_PATH+'/'+xt+'/'+ name
    if xt in['shp','SHP','gpkg','GPKG']:
        gdf = gpd.read_file(file)
        src_crs = gdf.crs
        try:
            gdf = gdf.to_crs(OUT_CRS)
        except:
            gdf.crs = OUT_CRS
        if xt in ['gpkg','GPKG']:
            drv = "GPKG"
        else:
            drv = 'ESRI Shapefile'
        gdf.to_file(outfile, drv)
    else:
        openfile = gdal.Open(file)
        src_crs = openfile.GetSpatialRef()
        Warp(outfile, openfile, srcSRS=src_crs, dstSRS=OUT_CRS)
    


def parallel_converter(files, OUT_CRS, JOBS):
    from joblib import Parallel, delayed
    Parallel (n_jobs=JOBS)(delayed(converter)(files[i], OUT_CRS)
                            for i in range(len(files)))
    

def chunk_creator(item_list, chunksize):
    it = iter(item_list)
    while True:
        chunk = list(itertools.islice(it, chunksize))
        if not chunk:
            break
        yield chunk

def main():        
    # List all files
    extensions = set()
    all_files = get_paths(DATA_PATH, ['tiff','tif','gpkg','shp'])
    for file in all_files:
        pathname, exten = os.path.splitext(file) 
        extensions.add(exten)
    for exts in extensions:
        exts=exts.split('.')[1]
        print(exts)
        make_folder(WORK_PATH, exts)
        
    
    # Check available resources
    import psutil
    avram=psutil.virtual_memory().total >> 3
    if avram > 31 and len(all_files) <5000:
        JOBS=psutil.cpu_count(logical=True)
    elif avram > 31 and len(all_files)>5000:
        JOBS=psutil.cpu_count(logical=True)
    elif avram <=31 and len(all_files)<5000:
        JOBS=psutil.cpu_count(logical=True)
    elif avram <= 31 and len(all_files) > 5000:
        JOBS=psutil.cpu_count(logical=False)
    
    # Create chunks for parallel processing
    filerange = len(all_files)
    chunksize = round(filerange/JOBS)
    if chunksize <1:
        chunksize=1
        JOBS = filerange
    chunks = []
    for c in chunk_creator(all_files, JOBS):
        chunks.append(c)
               
   
    # Parallel processing
    with tqdm(total=len(all_files),
             desc = 'Generating files',
             unit='File') as pbar:
        
        for i in range(len(chunks)):
            files = chunks[i]    
            # print(files)
            parallel_converter(files, OUT_CRS, JOBS)
            
           
            pbar.update(JOBS)



if __name__ == "__main__":

    parser = ArgumentParser()
    
    parser.add_argument('--wdir', help='Output folder: ')
    parser.add_argument('--ddir', help='Input files folder: ')
    parser.add_argument('--crs', help='Output CRS')
        
    args = parser.parse_args()
    WORK_PATH = args.wdir
    DATA_PATH = args.ddir
    OUT_CRS = args.crs

    ## PATHS
    #WORK_PATH = '/media/gnodj/W-DATS/Projects/ANALOG-1-Miracles/test_gdaltools/results'
    if WORK_PATH is None:
        root = Tk()
        root.withdraw()
        WORK_PATH = filedialog.askdirectory(parent=root,initialdir=os.getcwd(),title="Select output folder")
        print('Output folder:', WORK_PATH)

    #DATA_PATH = '/media/gnodj/W-DATS/Projects/ANALOG-1-Miracles/test_gdaltools'        
    if DATA_PATH is None:
        root = Tk()
        root.withdraw()
        DATA_PATH = filedialog.askdirectory(parent=root,initialdir=os.getcwd(),title="Select input files folder")
        print('Input files folder:', DATA_PATH)
    
    OUT_CRS = '+proj=utm +zone=33 +datum=WGS84 +units=m +no_defs'
    if OUT_CRS is None:
        OUT_CRS = input('Type destination CRS string')
   
    main()    



