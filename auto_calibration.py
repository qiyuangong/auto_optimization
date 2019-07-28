#!/usr/bin/env python3


import sys
import os
import argparse
import subprocess
import re
import shutil
import imghdr


OBJECT_DETECTION  = ["fastrcnn", "rfcn" "fasterrcnn", "ssd" "maskrcnn", "yolo"]
IMAGE_EXTENSIONS = []


def get_calibration_tool_path():
    # Search "/opt/intel/openvino" and home dir
    for path in ["/opt/intel/openvino", os.path.expanduser("~")]:
        res = find_file("calibration_tool", path)
        if res:
            return res
    # current
    raise Exception("ERROR: cannot find calibration_tool from deafult path")


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
    """
    """
    # Create anno and image dir
    val_image_path = os.path.join(image_path, "image")
    val_anno_path = os.path.join(image_path, "anno")
    val_txt = ""
    if os.path.exists(val_image_path):
        shutil.rmtree(val_image_path)
    if os.path.exists(val_anno_path):
        shutil.rmtree(val_anno_path)
    os.mkdir(val_image_path)
    os.mkdir(val_anno_path)
    for f in os.listdir(image_path):
        curr_path = os.path.join(image_path, f)
        if os.path.isfile(curr_path):
            continue
        # Move *.xml to anno
        if curr_path.endswith("xml"):
            shutil.copy(curr_path, val_anno_path)
        # Move images to image
        elif imghdr.what(curr_path) is not None:
            shutil.copy(curr_path, val_image_path)
        elif curr_path.endswith("txt"):
            val_txt = curr_path
    return val_image_path, val_anno_path, val_txt


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
    cmd_string = "%s -m %s -i %s -t %s" % (tool_path,
                                           args.model, args.input, model_type)
    if model_type == "OD":
        # TODO
        object_detection_val_prepare(args.input)
    else:
        # TODO
        cmd_string += "XXX"
    # run command
    subprocess.call(cmd_string, shell=True)
