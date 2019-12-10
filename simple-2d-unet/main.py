# %% Basic setup configurations
import os
import sys
sys.path.append(os.path.abspath("../lib"))

# from miscellaneous import isnotebook
# if (isnotebook()):
#     %load_ext autoreload
#     %autoreload 1
#     %aimport data_loader, loss, unet, helper, utils, console

from IPython import get_ipython
ipython = get_ipython()
if '__IPHYTHON__' in globals():
    ipython.magic('load_ext autoreload')
    ipython.magic('autoreload 1')
    ipython.magic('aimport data_loader, loss, unet, helper, utils, console')

# %% Load external modules
import argparse
import json
import logging
import ast

import numpy as np
from tqdm import tqdm

import torch
import torch.optim as optim
from torch.utils.data import DataLoader

from data_loader import DatasetHandler as Dataset
from data_loader import DatasetOptions
from data_loader import dataLoader
from loss import DiceLoss, computeDiceLoss
from unet import UNet

from train import train1
from run import run

from helper import *
from utils import loadSettings, loadFromCSV
from console import Console as con
from console import Logger

# %% Setup
settings = loadSettings()

args = Arguments(settings["Arguments"])

if torch.cuda.is_available():
    print('cuda available: ', torch.cuda.is_available())
    print('gpu: ', torch.cuda.get_device_name())

logger = Logger(args.logs + "/info.log")

# %% Make folders for log and weights
print("Making output directories")
makedirs(args)

# Define our training set
print("Loading path list")
imagesPath = loadFromCSV(settings["decathlon-output-png"] + "/images-list.csv")[0]
labelsPath = loadFromCSV(settings["decathlon-output-png"] + "/labels-list.csv")[0]

# %%

def unpack(paths):
    """
    Takes the split of the list that contains the lists os volume slices
    """
    images = []
    for volume in paths: 
        volumeList = ast.literal_eval(volume)
        for slice_ in volumeList: 
            images.append(slice_)
    return images

split = 2           # AKA num validations
# TODO : Make random split

trainImages = unpack(imagesPath[split:])
trainLabels = unpack(labelsPath[split:])
trainDataset = Dataset(trainImages, trainLabels, DatasetOptions(imageSize = args.image_size))

validImages = unpack(imagesPath[:split])
validLabels = unpack(labelsPath[:split])
validDataset = Dataset(validImages, validLabels, DatasetOptions(imageSize = args.image_size))


loaderTrain, loaderValid = dataLoader(args, trainDataset, validDataset)

# Model
unet = UNet(in_channels = 1,
            out_channels = 2,
            initialFeatures = 32)
unet.cuda()


# Optmizer
optimizer = optim.Adam(unet.parameters(), lr = args.lr)

# %%
if __name__ == '__main__':
    
    logger.infoh("Session started")
    logger.infoh2("batch_size : {}, epochs : {} learning_rate : {}, train_size : {}, valid_size : {}".format(args.batch_size,
                                                                                                            args.epochs,
                                                                                                            args.lr,
                                                                                                            len(trainImages),
                                                                                                            len(validImages)))
    logger.infoh2("in_channels : {}, out_channels : {}, initial_features : {}".format(unet.in_ch,
                                                                                    unet.out_ch,
                                                                                    unet.in_feat))
    run(unet,
        loaderTrain,
        loaderValid,
        optimizer,
        logger,
        args)

# %%
