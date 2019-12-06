# %% Basic setup configurations
import os
import sys
sys.path.append(os.path.abspath("../lib"))

from miscellaneous import isnotebook
if (isnotebook()):
    %load_ext autoreload
    %autoreload 1
    %aimport data_loader, loss, unet, helper, utils, console

# %% Load external modules
import argparse
import json
import logging

import numpy as np
from tqdm import tqdm

import torch
import torch.optim as optim
from torch.utils.data import DataLoader

from data_loader import DatasetHandler as Dataset
from data_loader import DatasetOptions
from data_loader import dataLoader
from loss import DiceLoss
from unet import UNet

from helper import *
from utils import loadSettings, loadFromCSV
from console import Console as con
from console import Logger

# %% Setup
settings = loadSettings()

args = Arguments(
    batch_size = 1,         #CH
    epochs = 2,
    lr = 0.001,
    workers = 0,            #CH
    vis_images = 200,
    vis_freq = 10,
    weights = "./weights",
    logs = "./logs",
    image_size = 64,
    device = torch.device("cpu" if not torch.cuda.is_available() else "cuda:0")
    )

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
split = 100
trainImages = imagesPath[split:]
trainLabels = labelsPath[split:]
trainDataset = Dataset(trainImages, trainLabels, DatasetOptions(imageSize = args.image_size))

validImages = imagesPath[:split]
validLabels = labelsPath[:split]
validDataset = Dataset(validImages, validLabels, DatasetOptions(imageSize = args.image_size))

logger.infoh("batch_size : {}, epochs : {} learning_rate : {}, train_size : {}, valid_size : {}".format(
    args.batch_size, args.epochs, args.lr, len(trainImages), len(validImages)))

# %% Define dataset andarchitecture
loaderTrain, loaderValid = dataLoader(args, trainDataset, validDataset)
loaders = {"train" : loaderTrain,
           "valid" : loaderValid}
# Model
architecture = {"in_channels" : 1,
                "out_channels" : 1,
                "initial_features" : 32}
unet = UNet(architecture["in_channels"],
            architecture["out_channels"],
            architecture["initial_features"])
unet.cuda()

logger.info("in_channels : {}, out_channels : {}, initial_features : {}".format(architecture["in_channels"],
                                                                                architecture["out_channels"],
                                                                                architecture["initial_features"]))
# Loss
diceLoss = DiceLoss()

# Optmizer
optimizer = optim.Adam(unet.parameters(), lr = args.lr)

# %% Train

def train(args : Arguments,
          loaders : dict,
          optimizer : optim.Adam,
          diceLoss : DiceLoss,
          logger : Logger
          ):
    
    step = 0
    bestValidation = 0.0
    lossTrain = []
    lossValidation = []
    
    for epoch in tqdm(range(args.epochs), total = args.epochs):
        for phase in ["train", "valid"]:
                
                if phase == "train":
                    unet.train()
                else:
                    unet.eval()
                
                validationPred = []
                validationTrue = []
                
                for i, data in enumerate(loaders[phase]):
                    if phase == "train":
                        step += 1
                    x, y_true = data
                    x, y_true = x.to(args.device), y_true.to(args.device)
                    
                    optimizer.zero_grad()
                    
                    with torch.set_grad_enabled(phase == "train"):
                        y_pred = unet(x)
                        
                        loss = diceLoss(y_pred, y_true)
                        
                        if phase == "valid":
                            
                            lossValidation.append(loss.item())
                            logger.info(loss.item())
                            y_pred_np = y_pred.detach().cpu().numpy()
                            validation_pred.extend([y_pred_np[s] for s in range(y_pred_np.shape[0])])
                            
                            y_true_np = y_true.detach().cpu().numpy()
                            validation_true.extend([y_true_np[s] for s in range(y_true_np.shape[0])])
                            
                        if phase == "train":
                            lossTrain.append(loss.item())
                            loss.backward()
                            optimizer.step()
                    
                    # Print every 10 steps
                    if phase == "train" and (step + 1) % 10 == 0:
                        # Write loss summary, check brain example
                        logger.infoh("loss : {}".format(lossTrain[-1:]))
                        
                if phase == "valid":
                    pass
                    # Do some dice score comparissons

# Señor, te pido devotamente que esta función corra sin problema amén.
if __name__ == '__main__':
    train(args, loaders, optimizer, diceLoss, logger)

# %% 

# TODO : Refactor to train/test/validation methods to runSession()

# def train():
#     unet.train()
#     with tqdm(total = len(loaderTrain)) as t:
#         t.set_description("Training"):
#             for i, 