# %%
import sys
import os
sys.path.append(os.path.abspath("../lib"))

import json
import random
import numpy as np

import matplotlib.pyplot as plt
from os.path import join
from skimage import io
from imageio import imread

import torch
from torch.utils.data.dataset import Dataset
from torch.utils.data import DataLoader
from torchvision import transforms
import torchvision.transforms.functional as tf

from helper import splitDataset, Arguments
from utils import loadSettings, loadFromCSV
from console import Console as con

# %%
class DatasetOptions:
    """
    ## LoaderOptions
    ----
    Preprocessing operations for `DatasetHandler` class. This class enables, rotatiosn, data augmentations etc. etc.
    """
    def __init__(self,
                 imageSize = None,
                 rotate = None,             # Tuple with angles if you rotation desired (-20, 20)
                 crop = False,              # Weather it does crop
                 merge = True,              # Merges tumor into liver class
                 noise = False
                 ):
        self.imageSize = imageSize
        self.rotate = rotate
        self.crop = crop
        self.merge = merge
        self.noise = noise

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
    
    def __init__(self, imagesPath, labelsPath, options = DatasetOptions()):
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
        
        image = imread(self.trainImages[index]).astype(np.float32)
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

        label = tf.adjust_brightness(label, 1 / 50)
        
        # Resize
        if (self.options.imageSize != None):
            size = self.options.imageSize
            image = tf.resize(image, size = (size, size), interpolation = 2)
            label = tf.resize(label, size = (size, size), interpolation = 0)
        
            lottery = np.random.randint(0, 10) < 5
            if (self.options.rotate != None and lottery):
                angle = random.randint(*self.options.rotate)
                image = image.rotate(angle)
                label = label.rotate(angle)
            
            lottery = np.random.randint(0, 10) < 5
            if (self.options.crop and lottery):
                i, j, h, w = transforms.RandomResizedCrop.get_params(image, scale = (0.8, 1), ratio=(0.75, 1))
                image = tf.resized_crop(image, i, j, h, w, size = (size, size), interpolation = 2)
                label = tf.resized_crop(label, i, j, h, w, size = (size, size), interpolation = 0)

            lottery = np.random.randint(0, 10) < 5
            if (self.options.noise and lottery):
                ### Add some noise ###
                pass
                
        image = tf.to_tensor(image)
        # label = tf.to_tensor(label)
        label = np.expand_dims(np.array(label), 0)
        if self.options.merge:
            label[label == 2] = 1

        label = torch.from_numpy(label)
        return image, label



def dataLoader(args, trainDataset, validDataset):
    
    loaderTrain = DataLoader(trainDataset,
                             batch_size = args.batch_size,
                             shuffle = True,
                             drop_last = True,
                             num_workers = args.workers)
    
    loaderValid = DataLoader(validDataset,
                             batch_size = args.batch_size,
                             shuffle = True,
                             drop_last = False,
                             num_workers = args.workers)
    
    return loaderTrain, loaderValid
# %%
def test():
    settings = loadSettings()

    imagesPath = loadFromCSV(settings["decathlon-output-tif"] + "/images-list.csv")[0]
    labelsPath = loadFromCSV(settings["decathlon-output-tif"] + "/labels-list.csv")[0]

    args = Arguments(settings["Arguments"])
    trainImages, trainLabels, _, _ = splitDataset(args = args,
                                                imagesPath = imagesPath,
                                                labelsPath = labelsPath,
                                                batchSize = args.batch_size)
    dh = DatasetHandler(imagesPath = trainImages,
                        labelsPath = trainLabels,
                        options = DatasetOptions(imageSize = 64, rotate = (-180, 180), crop = True, merge = True))

    image, label = dh.__getitem__(700)         # Has the image as tensor
    plt.subplot(1, 2, 1)
    plt.imshow(image.numpy().squeeze())
    plt.subplot(1, 2, 2)
    plt.imshow(label.numpy().squeeze())
    print(np.unique(label))

# test()

# %%
