#!/usr/bin/env python3


import sys
import os
import argparse
import subprocess


OBJECT_DETECTION  = []


def get_calibration_tool_path():
    if os.path.exists("/opt/intel"):
        calibration_tool = os.path.abspath
    return calibration_tool


def get_model_type(model_path):
    return "C"

def filter_annotations_out(image_path):
    return ""


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', required=True, help="Required. OpenVINO IR path, *.xml")
    parser.add_argument('-i', '--input', required=True, help="Required. Path to a directory with \
        validation images. For Classification models, the directory must contain \
            folders named as labels with images inside or a .txt file with a list \
                of images. For Object Detection models, the dataset must be in \
                    VOC format.")
    parser.add_argument('-s', '--subset', help="Number of pictures from the whole \
        validation set tocreate the calibration dataset. Default value is 0, \
            which stands forthe whole provided dataset", default=0)
    parser.add_argument('-o', '--output', help="Output Path for calibrated model")
    parser.add_argument('-t', '--type', help="Type of an inferred network (C by default)\
        C to calibrate Classification network and write the calibrated network to IR\
        OD to calibrate Object Detection network and write the calibrated network to IR\
        RawC to collect only statistics for Classification network and write statistics to IR. With this option, a model is not calibrated.\
        RawOD to collect only statistics for Object Detection network and write statistics to IR.")
    
    args = parser.parse_args()
    
    tool_path = get_calibration_tool_path()

    model_type = "C"
    if args.type is None:
        model_type = get_model_type(args.model)
    cmd_string = "%s -m %s -i %s -t %s" % (tool_path, args.model, args.input, model_type)
    


    subprocess.call(cmd_string, shell=True)
