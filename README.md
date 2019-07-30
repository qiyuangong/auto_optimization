# Auto_Optimization
OpenVINO automatic optimization and caliberation. Actually, auto-convert and auto-caliberation are possible for most common used TensorFlow models. But, this script may encounter error for some customized models.

## Requirements

1. Python & TensorFlow
2. OpenVINO

## Auto Calibration
Assume you have OpenVINO IR model (converted from Caffe or TensorFlow), and you want to convert it into `int8` model. Herein OpenVINO `int8` IR promises higher performance than IR model by wsacrificing a few precision (1% by default).




## References
1. [OpenVINO](https://software.intel.com/en-us/openvino-toolkit) 
2. [Analytics-Zoo](https://github.com/intel-analytics/analytics-zoo)
3. [TensorFlow](https://www.tensorflow.org/)

