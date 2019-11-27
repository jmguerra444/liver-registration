import sys
import os
sys.path.append(os.path.abspath("../lib"))

import random
import json
import numpy as np
import nibabel

import matplotlib.pyplot as plt
from os.path import join
from skimage import io

import torch
from torch.utils.data.dataset import Dataset
from torchvision import transforms

from utils import *
from console import Console as con
# from master.visual.viewer import SliceViewer >>> Import from sibling folder somehow

class DataLoaderManager(Dataset):
    """
    ### DataLoaderManager
    ----
    - Layer between raw image paths and torch.dataloader, this class should also handle
    required preprocessing operations.
    - For nifti image loading
    \n
    #### Params
    `Images` : List of paths that reference the images \n
    `Labels` : List of paths that refrence the labels
    """
    
    def __init__(self,
                 datasetSchema,
                 pathPrefix = "",
                 sliceIndex = 0
                 ):
        """
        Constructor for simple Image loader
        """
        self.trainImages = []                       # Full train image path
        self.trainLabels = []                       # Full train image label path
        self.sliceIndex = sliceIndex                # Slices where GT is present (not ponly background)
        
        self.imageTransforms = transforms.Compose(
            [transforms.ToTensor()])
        # Queue more image transformations here, crop, center etc. etc. 
        
        paths = readConfigurationFile(pathPrefix, "train", datasetSchema)
        self.trainImages = [path["image"] for path in paths]
        self.trainLabels = [path["label"] for path in paths]

    def __getitem__(self, index):
        
        """
        This function needs to be overriten from Dataset(torch) class
        """
        
        volume = nibabel.load(self.trainImages[index]).get_fdata()
        volumeLabel = nibabel.load(self.trainLabels[index]).get_fdata()
        
        # --------------------------------
        # Do image transformations etc etc.
        # --------------------------------
        
        image = np.float32(volume[:, :, self.sliceIndex])
        label = np.float32(volumeLabel[:, :, self.sliceIndex])
        
        imageTensor = self.imageTransforms(image)
        labelTensor = self.imageTransforms(label)
        
        return imageTensor, labelTensor
        
    def __len__(self):
        return len(self.trainImages)


def readConfigurationFile(pathPrefix, mode, datasetSchema):
    try:
        with open(datasetSchema) as cf:
            data = json.load(cf)

        train = data["training"]
        test = data["test"]
        test = [join(pathPrefix, image) for image in test]
        for i in train:
            i["image"] = join(pathPrefix, i["image"])
            i["label"] = join(pathPrefix, i["label"])

        if (mode == "train"):
            return train
        if (mode == "test"):
            return test
        
    except:
        con.printw("Invalid data properties")

def test():
    settings = loadSettings("configuration.json")
    dlm = DataLoaderManager(datasetSchema = "01-dataset.json",
                            pathPrefix = settings["decathlon-dataset-path"]
                            )

    dlm.sliceIndex = 50
    image, label = dlm.__getitem__(5)

    npimage = image.numpy()
    nplabel = label.numpy()

    plt.imshow(nplabel[0, :, :])
    plt.imshow(npimage[0, :, :])

# test()