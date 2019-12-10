
"""
DEPRECATED AND REIMPLEMENTED IN run.py
"""

# TODO : Delete unnecesary modules

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

from helper import *
from utils import loadSettings, loadFromCSV
from console import Console as con
from console import Logger


# %% Train

def train1(args : Arguments,
          loaders : dict,
          optimizer : optim.Adam,
          logger : Logger,
          unet : UNet
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
                        loss = computeDiceLoss(y_true.long(), y_pred)
                        
                        if phase == "valid":
                            pass
                            # lossValidation.append(loss.item())
                            # logger.info(loss.item())
                            # y_pred_np = y_pred.detach().cpu().numpy()
                            # validation_pred.extend([y_pred_np[s] for s in range(y_pred_np.shape[0])])
                            
                            # y_true_np = y_true.detach().cpu().numpy()
                            # validation_true.extend([y_true_np[s] for s in range(y_true_np.shape[0])])
                            
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
