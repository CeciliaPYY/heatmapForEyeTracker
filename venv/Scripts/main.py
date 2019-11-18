#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import json
import time

from model.heatmap import Heatmap
from utils.image_utils import read_image_return_nparray, image_add_with_certain_weight, get_image_dpi


def load_eye_tracking_data(fname, mode='r'):
    with open(fname, mode) as f:
        heatmap_data = json.load(f)

    return heatmap_data


def main(json_path, background_image_path, heatmap_save_path, alpha):

    eye_tracking_data = load_eye_tracking_data(json_path)

    heatmap = Heatmap(original_data=eye_tracking_data)
    foreground_heatmap = heatmap.generate_heatmap()

    background_image = read_image_return_nparray(background_image_path)

    image_add_with_certain_weight(foreground_heatmap, background_image, alpha=alpha, save=heatmap_save_path)


if __name__ == "__main__":

    split_line = '=' * 100
    print(split_line)
    startTimeStamp = int(round(time.time() * 1000))
    print("  *** Begin : %s ***" % time.ctime())

    parser = argparse.ArgumentParser(add_help=False, description="Generate Heatmap for Eye Tracking Data.")
    parser.add_argument('-h', '--help', default=argparse.SUPPRESS,
                        help='Show this help message and exit.')
    parser.add_argument('-j', '--json', type=str, default="HeatmapData.txt",
                        help='path to heatmap original data')
    parser.add_argument('-bg', '--background_image', type=str, default="./background_image.png",
                        help='path to background image')
    parser.add_argument('-a', '--alpha', type=float, default=0.5,
                        help='alpha percent to add heatmap to background image which is a float between 0 and 1')
    parser.add_argument('-o', '--output', type=str, default="./heatmap.png",
                        help='path to save heatmap image')

    args = parser.parse_args()

    main(args.json, args.background_image, args.output, args.alpha)

    endTimeStamp = int(round(time.time() * 1000))
    print('  *** End : %s ***\n\n' % time.ctime())
    print("Time Duration is {}".format(endTimeStamp - startTimeStamp))


