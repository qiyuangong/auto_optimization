#!/usr/bin/env python3


import sys
import os
import argparse
import subprocess
import re


OBJECT_DETECTION  = ["fastrcnn", "rfcn" "fasterrcnn", "ssd" "maskrcnn", "yolo"]


def get_calibration_tool_path():
    # Search "/opt/intel/openvino" and home dir
    for path in ["/opt/intel/openvino", os.path.expanduser("~")]:
        res = find_file("calibration_tool", path)
        if res:
            return res


def find_file(name, path):
    if not os.path.exists(path):
        return None
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def get_model_type(model_path):
    regex = re.compile('[^a-zA-Z]')
    alpha_path = regex.sub('', model_path)
    for od_model in OBJECT_DETECTION:
        if od_model in alpha_path:
            return "OD"
    return "C"


def object_detection_val_prepare(image_path):
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
    if model_type == "OD":
        # TODO
        object_detection_val_prepare(args.input)
    else:
        # TODO
        cmd_string += "XXX"
    subprocess.call(cmd_string, shell=True)
