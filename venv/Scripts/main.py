#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import time

from model.heatmap import Heatmap
from utils.image_utils import read_image_return_nparray, resize_image_innparray, image_add_with_certain_weight, images_add_with_certain_weight

def load_eye_tracking_data(fname='../HeatMapData_exact9.txt', mode='r'):
    with open(fname, mode) as f:
        heatmap_data = json.load(f)

    return heatmap_data

if __name__ == "__main__":

    startTimeStamp = int(round(time.time() * 1000))
    print("starting: {}".format(time.ctime()))

    eye_tracking_data = load_eye_tracking_data()
    heatmap = Heatmap(original_data=eye_tracking_data)
    foreground_heatmap = heatmap.generate_heatmap()
    background_image = read_image_return_nparray('../images/shelf_goods5.jpg')
    # resized_background_image = resize_image_innparray(background_image, heatmap.width, heatmap.height)
    image_add_with_certain_weight(foreground_heatmap, background_image, alpha=0.5, save='../images/exact/heatmap9_alpha0.5_num1_kernel100.png')

    endTimeStamp = int(round(time.time() * 1000))
    print("Ending: {}".format(time.ctime()))
    print("Time Duration is {}".format(endTimeStamp - startTimeStamp))


