# Simple 2D unet example

Basic liver/lesion segmentation using standard 2d unet arcgitecture

## Model

A segmentation model implemented in this repository is U-Net as described in [Association of genomic subtypes of lower-grade gliomas with shape features automatically extracted by a deep learning algorithm](https://doi.org/10.1016/j.compbiomed.2019.05.002) with added batch normalization.

![unet](resources/unet.png)

```python
# Blocks
block :
    conv2d
    batch_normalization
    relu
    conv2d
    batch_normalization
    relu

# Params
kernel_size = 3
padding = 1

```

