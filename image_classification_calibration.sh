#!/bin/bash

set -x

usage()
{
    echo "usage: You have to provide
       1. m, Path to an .xml file with a trained model, including model name and extension. (.xml),
       2. i, Path to a directory with validation images. For Classification models, the directory must contain folders named as labels with images inside or a .txt file with a list of images. For Object Detection models, the dataset must be in VOC format,
       3. subset, Number of pictures from the whole validation set tocreate the calibration dataset. Default value is 0, which stands forthe whole provided dataset,
       4. the output directory,
       5. the path of the calibration_tool
       as parameters in order. More concretely, you can run this command:
       sh calibration.sh \\
            /path/to/the/ir/xml/file \\
            /path/to/the/validation/file \\
            subset \\
            /the/output/directory \\
            /path/to/the/calibration_tool"
    exit 1
}

if [ -d "$HOME/inference_engine_samples_build/intel64/Release" ]
then
    CALIBRATION_FILE="$HOME/inference_engine_samples_build/intel64/Release/calibration_tool"
fi

if [ -z "$CALIBRATION_FILE" ] && [ -z "$5" ]
then
    echo "Error: Cannot find calibration_tool in default install path"
    exit
fi

SUBSET=0

if [ "$#" -lt 2 ] || [ "$#" -gt 5 ]
then
    usage
    exit
else
    MODEL_XML="$1"
    VALIDATION_FILE="$2"
fi

if [ ! -z "$3" ]
then
    SUBSET="$3"
fi

if [ ! -z "$4" ]
then
    OUTPUT_DIR="$4"
fi

if [ ! -z "$5" ] && [ -z "$CALIBRATION_FILE" ]
then
    CALIBRATION_FILE="$5"
fi

echo "Using ${CALIBRATION_FILE}"

CMD="-t C -m ${MODEL_XML} -i ${VALIDATION_FILE}"

# Set default subset number
if [ "$SUBSET" -gt 0 ]
then 
    CMD="${CMD} -subset ${SUBSET}"
fi

if [ ! -z "$OUTPUT_DIR" ]
then
    CMD="${CMD} -output ${OUTPUT_DIR}"
fi

${CALIBRATION_FILE} ${CMD}
