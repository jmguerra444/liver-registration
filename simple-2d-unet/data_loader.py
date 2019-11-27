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
import torchvision.transforms.functional as tf

from utils import *
from helper import LoaderOptions
from console import Console as con

# %%
class DatasetHandler(Dataset):
    """
    ### DatasetHandler (from .PNG)
    ----
    - Layer between raw image paths and torch.dataloader, this class should also handle
    required preprocessing operations.
    - For PNG image loading class
    - For training only
    \n
    #### Params
    `imagesPath` : List of paths that reference the images \n
    `labelsPath` : List of paths that refrence the labels
    """
    
    def __init__(self, imagesPath, labelsPath, options = LoaderOptions()):
        """
        Constructor for simple Image loader,
        """
        
        self.trainImages = imagesPath                       # Full train image paths
        self.trainLabels = labelsPath                       # Full train label paths
        self.options = options                              # Preprocessing operations

    def __getitem__(self, index):
        """
        This function needs to be overriten from Dataset(torch) class
        """
        
        image = imread(self.trainImages[index])
        label = imread(self.trainLabels[index])
        
        imageTensor, labelTensor = self.transformations(image, label)
        
        return imageTensor, labelTensor

    def __len__(self):
        return len(self.trainImages)

    def transformations(self, image, label):
        """
        Chain of required imaged transformations inc. `.toTensor()`, does all operations according
        to LoaderOptions
        """

        image = tf.to_pil_image(image)
        label = tf.to_pil_image(label)
        
        # Do all queued operations ...
        
        # Resize
        if (self.options.imageSize != None):
            size = self.options.imageSize
            image = tf.resize(image, size = (size, size), interpolation = 2)
            label = tf.resize(label, size = (size, size), interpolation = 0)
        
        image = tf.to_tensor(image)
        label = tf.to_tensor(label)
        
        return image, label

# %%
def test_1():
    settings = loadSettings()

    # TODO : Check images loding as a list of lists
    imagesPath = loadFromCSV(settings["decathlon-output-png"] + "/images-list.csv")[0]
    labelsPath = loadFromCSV(settings["decathlon-output-png"] + "/labels-list.csv")[0]

    dh = DatasetHandler(imagesPath = imagesPath,
                        labelsPath = labelsPath,
                        options = LoaderOptions(imageSize = 64))
    image, label = dh.__getitem__(10)         # Has the image as tensor
    plt.subplot(1, 2, 1)
    plt.imshow(image.numpy().squeeze())
    plt.subplot(1, 2, 2)
    plt.imshow(label.numpy().squeeze())
    
    return image, label

image, label = test_1()