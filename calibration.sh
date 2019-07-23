#!/bin/bash

set -x

usage()
{
    echo "usage: You have to provide
       1. m, Path to an .xml file with a trained model, including model name and extension. (.xml),
       2. i, Path to a directory with validation images. For Classification models, the directory must contain folders named as labels with images inside or a .txt file with a list of images. For Object Detection models, the dataset must be in VOC format,
       3. subset, Number of pictures from the whole validation set tocreate the calibration dataset. Default value is 0, which stands forthe whole provided dataset,
       4. the output directory,
       5. type, Type of an inferred network ("C" by default), "C" to calibrate Classification, "OD" to calibrate Object Detection, "RawC" to collect only statistics for Classification and "RawOD" to collect only statistics for Object Detection
       6. the path of the calibration_tool
       as parameters in order. More concretely, you can run this command:
       sh calibration.sh \\
            /path/to/the/ir/xml/file \\
            /path/to/the/validation/file \\
            subset \\
            /the/output/directory \\
            type \\
            /path/to/the/calibration_tool
    exit 1
}

if [ -d "/opt/intel" ]
then 
    CALIBRATION_FILE=`find /opt/intel -name 'calibration_tool' -print | head -n 1`
else [ -d "/home/$USER/intel" ]
    CALIBRATION_FILE=`find /home/$USER/intel -name 'calibration_tool' -print | head -n 1`
fi

if [-z "$CALIBRATION_FILE"]
then
    echo "WARNING: Cannot find calibration_tool in default install path"
fi

SUBSET=-1

if [ "$#" < 2 ] || [ "$#" -gt 6 ]
then
    usage
else
    MODEL_XML="$1"
    VALIDATION_FILE="$2"
    SUBSET="$3"
    OUTPUT_DIR="$4"
    TYPE="$5"
    CALIBRATION_FILE="$6"
fi

# Set default subset number
if [ "$SUBSET" < 0 ]
then 
    SUBSET=`wc -l $VALIDATION_FILE`
fi

echo ${CALIBRATION_FILE}

${CALIBRATION_FILE} \
    -m ${MODEL_XML} \
    -i ${VALIDATION_FILE} \
    -subset ${SUBSET} \
    -output ${OUTPUT_DIR} \
    -t ${TYPE}
