#!/bin/bash

set -x

usage()
{
    echo "usage: You have to provide
       1. m, Path to an .xml file with a trained model, including model name and extension. (.xml),
       2. i, Path to a directory with validation images. For Classification models, the directory must contain folders named as labels with images inside or a .txt file with a list of images. For Object Detection models, the dataset must be in VOC format,
       3. the path of the calibration_tool
       4. type, Type of an inferred network ("C" by default), "C" to calibrate Classification, "OD" to calibrate Object Detection, "RawC" to collect only statistics for Classification and "RawOD" to collect only statistics for Object Detection
       5. the output directory,
       6. subset, Number of pictures from the whole validation set tocreate the calibration dataset. Default value is 0, which stands forthe whole provided dataset,
       as parameters in order. More concretely, you can run this command:
       sh calibration.sh \\
            /path/to/the/ir/xml/file \\
            /path/to/the/validation/file \\
            /path/to/the/calibration_tool \\
            type \\
            subset \\
            /the/output/directory \\
    exit 1
}

if [ "$#" -ne 6 ]
then
    usage
else
    MODEL_XML="$1"
    VALIDATION_FILE="$2"
    CALIBRATION_FILE="$3"
    TYPE="$4"
    SUBSET="$5"
    OUTPUT_DIR="$6"
fi


echo ${CALIBRATION_FILE}


${CALIBRATION_FILE} \
    -m ${MODEL_XML} \
    -i ${VALIDATION_FILE} \
    -t ${TYPE} \
    -subset ${SUBSET} \
    -output ${OUTPUT_DIR}

