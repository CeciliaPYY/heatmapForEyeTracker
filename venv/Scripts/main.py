#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
This is the main function to generate heatmap based on eye tracking data.
"""

import argparse
import json

from model.heatmap import Heatmap
from utils.image_utils import read_image_return_nparray, image_add_with_certain_weight, get_image_dpi, change_cmap


def load_eye_tracking_data(fname, mode='r'):
    """
    Load eye tracking data from file named fname
    :param fname: file path and name
    :param mode: read or write
    :return: eye tracking data
    """
    with open(fname, mode) as f:
        heatmap_data = json.load(f)

    return heatmap_data


def main(json_path, background_image_path, heatmap_save_path, alpha):
    """
    main function to generate heatmap
    :param json_path: json file saved eye tracking data
    :param background_image_path: background shelf image path
    :param heatmap_save_path: where to save heatmap
    :param alpha: heatmap = alpha * foreground_image + background_image
    :return: void
    """

    eye_tracking_data = load_eye_tracking_data(json_path)

    heatmap = Heatmap(original_data=eye_tracking_data)
    foreground_heatmap = heatmap.generate_heatmap()

    background_image = read_image_return_nparray(background_image_path)
    cmap = change_cmap()

    image_add_with_certain_weight(foreground_heatmap, background_image, alpha=alpha, cmap=cmap, save=heatmap_save_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(add_help=False, description="Generate Heatmap for Eye Tracking Data.")
    parser.add_argument('-h', '--help', default=argparse.SUPPRESS,
                        help='Show this help message and exit.')
    parser.add_argument('-j', '--json', type=str, default="HeatmapData.txt",
                        help='path to heatmap original data')
    parser.add_argument('-bg', '--background_image', type=str, default="./background_image.png",
                        help='path to background image')
    parser.add_argument('-a', '--alpha', type=float, default=0.4,
                        help='alpha percent to add heatmap to background image which is a float between 0 and 1')
    parser.add_argument('-o', '--output', type=str, default="./heatmap.png",
                        help='path to save heatmap image')

    args = parser.parse_args()

    main(args.json, args.background_image, args.output, args.alpha)
    print(args.output)


