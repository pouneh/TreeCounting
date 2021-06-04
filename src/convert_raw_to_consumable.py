# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 15:04:11 2021

@author: sparky
"""

import os
from pathlib import Path
import glob
import csv
from PIL import Image


project_root = Path('..')

def draw_annotations_on_image(annotations, image):
    pass

def get_annotation_list_for_image(image_path):
    #parse out geo_index from image path
    #parse out site from image path
    pathcomponents = image_path.split('_')
    site = pathcomponents[1]
    geo_index = pathcomponents[3] + "_" + pathcomponents[4]
    primary_annotations = get_confidence_and_boxes(site)
    return primary_annotations[geo_index]


def get_annotation_list_for_geosite(geosite= "535000_4971000", site = "YELL"):
    primary_annotations = get_confidence_and_boxes(site)
    return primary_annotations[geosite]
    
    
def get_image_list(site):
    imageFileList = glob.glob(f'{project_root}\\data\\images\\*{site}*.tif')
    return imageFileList
    
def get_confidence_and_boxes(site):
    #{ key=geo_index, value =[tuple with confidence, and bounding box coordinates]}
    result = {}
    csv_annotation = glob.glob(f'{project_root}\\{site.upper()}*.csv')
    if len(csv_annotation) == 0:
        # download the CSV
        print("Lost file")
        return
    if len(csv_annotation) > 1:
        print (f"Ambiguous annotations for {site}")
        return
    

    with open(csv_annotation[0], mode='r') as infile:
        reader = csv.reader(infile)
        next(reader)
        for row in reader:
            result.setdefault(row[10],[]) 
            result[row[10]] += [(float(row[5]), float(row[1]), float(row[2]), float(row[3]), float(row[4]))]
    return result

def yolov5Annotation(geosite, geositeAnnotationList):
    geoX, geoY = geosite.split("_")
    geoX = int(geoX)
    geoY = int(geoY)
    
    
    result = []
    utm_units = 1000.0
    for row in geositeAnnotationList:
        left = row[1] - geoX
        right = row[3] - geoX
        top = utm_units - (row[2] - geoY)
        bottom = utm_units - (row[4] - geoY)

        s_left = left/utm_units
        s_right = right/utm_units
        s_top = top/utm_units
        s_bottom = bottom/utm_units
        result += [( (s_left+s_right)/2,
                    (s_top + s_bottom)/2,
                    s_right - s_left,
                    s_top - s_bottom)]
        
    return result

        
def writeAnnotationToFile(yoloAnnotationList, outputPath):
    #output = Path("..\\data\\labels\\valid\\2019_YELL_2_535000_4971000_image.txt")
    #output = Path("..\\data\\labels\\train\\2019_YELL_2_535000_4971000_image.txt")
    txt = "0 {w_c:.8f} {h_c:.8f} {w:.8f} {h:.8f}\n"
    with open(outputPath, 'a') as f:
        for row in yoloAnnotationList:
            f.write(txt.format(w_c=row[0], h_c=row[1], w=row[2], h=row[3]))
    pass

def setup_yolo_directories():
    #import os
    paths =["..\\yolov5",
            "..\\data\\images",
            "..\\data\\images\\train",
            "..\\data\\images\\valid",
            "..\\data\\labels\\train",
            "..\\data\\labels\\valid"
        ]
    for directory in paths:
        if not os.path.exists(directory):
            os.makedirs(directory)
            
            
def convert_tif_to_jpg(tifpath, jpgpath):
    Image.MAX_IMAGE_PIXELS = None
    with Image.open(tifpath) as im:
        im.save(jpgpath)

def test(site = 'yell'):
    images = get_image_list(site)
    primary_annotation = get_confidence_and_boxes(site)
    
    #image_path = "C:\Users\spark\Desktop\TreeCounting\data\images\2019_YELL_2_535000_4971000_image.tif"
    return get_annotation_list_for_image(images[0])
