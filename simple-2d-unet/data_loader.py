# %%
import sys
import os
sys.path.append(os.path.abspath("../lib"))

import json
import numpy as np

import matplotlib.pyplot as plt
from os.path import join
from skimage import io
from imageio import imread

import torch
from torch.utils.data.dataset import Dataset
from torchvision import transforms

from utils import *
from console import Console as con

# %%
class DataLoaderManager(Dataset):
    """
    ### DataLoaderManager
    ----
    - Layer between raw image paths and torch.dataloader, this class should also handle
    required preprocessing operations.
    - For PNG image loading class
    \n
    #### Params
    `imagesPath` : List of paths that reference the images \n
    `labelsPath` : List of paths that refrence the labels
    """
    
    def __init__(self, imagesPath, labelsPath):
        """
        Constructor for simple Image loader
        """
        self.trainImages = imagesPath                       # Full train image paths
        self.trainLabels = labelsPath                       # Full train label paths
        
        self.imageTransforms = transforms.Compose(
            [transforms.ToTensor()]
            )
        # Queue more image transformations here, crop, center etc. etc. 

    def __getitem__(self, index):
        
        """
        This function needs to be overriten from Dataset(torch) class
        """
        
        image = imread(self.trainImages[index])
        label = imread(self.trainLabels[index])
        
        imageTensor = self.imageTransforms(image)
        labelTensor = self.imageTransforms(label)
        
        return imageTensor, labelTensor
        
    def __len__(self):
        return len(self.trainImages)

# %%
settings = loadSettings("configuration.json")

# TODO : Check images loding as a list of lists
imagesPath = loadFromCSV(settings["decathlon-output-png"] + "/images-list.csv")[0]
labelsPath = loadFromCSV(settings["decathlon-output-png"] + "/labels-list.csv")[0]

dlm = DataLoaderManager(imagesPath = imagesPath,
                        labelsPath = labelsPath)

image = dlm.__getitem__(10)
label = dlm.__getitem__(10)
# %%
