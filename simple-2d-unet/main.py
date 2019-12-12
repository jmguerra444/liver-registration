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
import numpy as np

from tqdm import tqdm

import torch
import torch.optim as optim
from torch.utils.data import DataLoader

from data_loader import DatasetHandler as Dataset
from data_loader import DatasetOptions
from data_loader import dataLoader
from loss import computeDiceLoss
from unet import UNet
from run import run

from helper import *
from utils import loadSettings, loadFromCSV, unpack
from console import Console as con
from console import Logger

# %% Setting up Model, Dataset and Parameters
settings = loadSettings()
args = Arguments(settings["Arguments"])

logger = Logger(filename = args.logs + "/{}.log".format(args.id),
                formato = '%(message)s')

logger.warning("PROGRAM STARTED {}".format(args.id))
logger.info("")

if torch.cuda.is_available():
    logger.info('Cuda available: {}'.format(torch.cuda.is_available()))
    logger.info('GPU : {}'.format(torch.cuda.get_device_name()))

logger.info("Making output directories")
makedirs(args)

# Define our training set
logger.info("Loading path list")
imagesPath = loadFromCSV(settings["decathlon-output-png"] + "/images-list.csv")[0]
labelsPath = loadFromCSV(settings["decathlon-output-png"] + "/labels-list.csv")[0]

split = 2           # AKA num validations
# TODO : Make random split

logger.info("Oraganizing dataset")
trainImages = unpack(imagesPath[split:])
trainLabels = unpack(labelsPath[split:])
trainDataset = Dataset(trainImages, trainLabels, DatasetOptions(imageSize = args.image_size))

validImages = unpack(imagesPath[:split])
validLabels = unpack(labelsPath[:split])
validDataset = Dataset(validImages, validLabels, DatasetOptions(imageSize = args.image_size))

loaderTrain, loaderValid = dataLoader(args, trainDataset, validDataset)

# Model
unet = UNet(in_channels = 1,
            out_channels = 3,
            initialFeatures = 32)
unet.cuda()
# TODO : hacer esto
# Optmizer
optimizer = optim.Adam(unet.parameters(), lr = args.lr)

# %%
if __name__ == '__main__':
    
    logger.infoh("SESSION STARTED")
    logger.infoh2("""
                  batch_size : {}
                  epochs : {}
                  learning_rate : {}
                  train_size : {}
                  valid_size : {}""".format(args.batch_size,
                                            args.epochs,
                                            args.lr,
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
