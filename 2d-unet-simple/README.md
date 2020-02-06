# Simple 2D unet example

**Contains many bugs, check 2d-unet-liver-ct**

Basic liver/lesion segmentation using standard 2d unet arcgitecture, inspired from https://github.com/mateuszbuda/brain-segmentation-pytorch

## Model

A segmentation model implemented in this repository is U-Net as described in [Association of genomic subtypes of lower-grade gliomas with shape features automatically extracted by a deep learning algorithm](https://doi.org/10.1016/j.compbiomed.2019.05.002) with added batch normalization.

![unet](resources/unet.png)

## Start

1. Activate some conda enviroment
2. Install enviroment : `conda env create -f environment.yml`
3. Activate enviroment : `conda activate master-thesis`

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
loss_fnc = DiceLoss()
```
