# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:16:25 2020

@author: azan
"""
import os
import sys
import json
import datetime
import numpy as np
import skimage.draw

class BalloonDataset():
    def load_balloon(self, dataset_dir, subset):
            """Load a subset of the Balloon dataset.
            dataset_dir: Root directory of the dataset.
            subset: Subset to load: train or val
            """
            # Add classes. We have only one class to add.
            self.add_class("KaleWeek", 1, "KaleWeek2")
            self.add_class("KaleWeek", 2, "KaleWeek3")
            
    
            # Train or validation dataset?
            assert subset in ["train", "val"]
            dataset_dir = os.path.join(dataset_dir, subset)
    
            # Load annotations
            # VGG Image Annotator (up to version 1.6) saves each image in the form:
            # { 'filename': '28503151_5b5b7ec140_b.jpg',
            #   'regions': {
            #       '0': {
            #           'region_attributes': {},
            #           'shape_attributes': {
            #               'all_points_x': [...],
            #               'all_points_y': [...],
            #               'name': 'polygon'}},
            #       ... more regions ...
            #   },
            #   'size': 100202
            # }
            # We mostly care about the x and y coordinates of each region
            # Note: In VIA 2.0, regions was changed from a dict to a list.
            annotations = json.load(open(os.path.join(dataset_dir, "via_region_data.json")))
            annotations = list(annotations.values())  # don't need the dict keys
    
            # The VIA tool saves images in the JSON even if they don't have any
            # annotations. Skip unannotated images.
            annotations = [a for a in annotations if a['regions']]
    
            # Add images
            for a in annotations:
                # Get the x, y coordinaets of points of the polygons that make up
                # the outline of each object instance. These are stores in the
                # shape_attributes (see json format above)
                # The if condition is needed to support VIA versions 1.x and 2.x.
                if type(a['regions']) is dict:
                    polygons = [r['shape_attributes'] for r in a['regions'].values()]
                else:
                    polygons = [r['shape_attributes'] for r in a['regions']] 
    
                #Get the name of the class id
                objects = [s['region_attributes'] for s in a['regions']]
    
                num_ids=[]
                for n in objects:
                    #print(n)
                    #print(type(n))
                    try:
                        if n['KaleWeek']=='KaleWeek2':
                            num_ids.append(1)
                        elif n['KaleWeek']=='KaleWeek3':
                            num_ids.append(2)
                    except:
                        pass
            	
            #num_ids = [int(n['object_name']) for n in objects]
    
                # load_mask() needs the image size to convert polygons to masks.
                # Unfortunately, VIA doesn't include it in JSON, so we must read
                # the image. This is only managable since the dataset is tiny.
                image_path = os.path.join(dataset_dir, a['filename'])
                image = skimage.io.imread(image_path)
                print("Im path:")
                print(image_path)
                os.system("pause")
                height, width = image.shape[:2]
    
                self.add_image(
                    "KaleWeek",
                    image_id=a['filename'],  # use file name as a unique image id
                    path=image_path,
                    width=width, height=height,
                    polygons=polygons,
                    num_ids=num_ids)
            
if __name__ == "__main__":
    load_balloon("../../dataset\Kale", "train")