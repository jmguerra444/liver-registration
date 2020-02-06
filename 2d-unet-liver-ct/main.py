# %% Basic setup configurations and Imports
import os
import sys
sys.path.append(os.path.abspath("../lib"))

from IPython import get_ipython
ipython = get_ipython()
if '__IPHYTHON__' in globals():
    ipython.magic('load_ext autoreload')
    ipython.magic('autoreload 1')
    ipython.magic('aimport data_loader, loss, unet, helper, utils, console')

import argparse
import json
import logging
import ast
import platform
import numpy as np

from tqdm import tqdm
from platform import node

import torch
import torch.optim as optim
from torch.utils.data import DataLoader

from data_loader import DatasetHandler as Dataset
from data_loader import DatasetOptions, dataLoader
from loss import computeDiceLoss
from unet import UNet
from run import run

from helper import Arguments, makedirs, splitDataset
from utils import loadSettings, loadFromCSV
from console import Console as con
from console import Logger

# %% Setting up Model, Dataset and Parameters
settings = loadSettings()
args = Arguments(settings["Arguments"])
makedirs(args)

logger = Logger(filename = args.logs + "/{}.log".format(args.id),
                formato = '%(message)s')

logger.warning("PROGRAM STARTED {} at {}".format(args.id, platform.node()))
logger.info("")

if torch.cuda.is_available():
    logger.info('Cuda available: {}'.format(torch.cuda.is_available()))
    logger.info('GPU : {}'.format(torch.cuda.get_device_name()))

logger.info("Making output directories")

# Define our training set
logger.info("Loading path list")
imagesPath = loadFromCSV(settings["decathlon-output-tif"] + "/images-list.csv")[0]
labelsPath = loadFromCSV(settings["decathlon-output-tif"] + "/labels-list.csv")[0]

# %%

logger.info("Oraganizing dataset")

trainImages, trainLabels, validImages, validLabels = splitDataset(args = args,
                                                                  imagesPath = imagesPath,
                                                                  labelsPath = labelsPath,
                                                                  batchSize = args.batch_size)

trainOptions = DatasetOptions(imageSize = args.image_size,
                              rotate = (-10, 10),
                              crop = False,
                              merge = True,
                              noise = True)

validOptions = DatasetOptions(imageSize = args.image_size,
                              rotate = (-10, 10),
                              crop = False,
                              merge = True,
                              noise = True)

trainDataset = Dataset(trainImages, trainLabels, trainOptions)
validDataset = Dataset(validImages, validLabels, validOptions)

loaderTrain, loaderValid = dataLoader(args, trainDataset, validDataset)

# Model
unet = UNet(**settings["2d-unet-params"])
unet.cuda()

# TODO : Make some schedule
optimizer = optim.Adam(unet.parameters(), lr = args.lr)

# %%
if __name__ == '__main__':
    
    logger.infoh("SESSION STARTED")
    logger.infoh2("""
                  batch_size : {}
                  epochs : {}
                  learning_rate : {}
                  num_workers : {}
                  image_size : {}
                  train_size : {}
                  valid_size : {}""".format(args.batch_size,
                                            args.epochs,
                                            args.lr,
                                            args.workers,
                                            args.image_size,
                                            len(trainImages),
                                            len(validImages)))
    logger.infoh2("""
                  in_channels : {}
                  out_channels : {}
                  initial_features : {}""".format(unet.in_ch,
                                                 unet.out_ch,
                                                 unet.in_feat))
    run(unet,
        loaderTrain,
        loaderValid,
        optimizer,
        logger,
        args)

# %%
