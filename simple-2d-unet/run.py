"""
This takes args, data loader, and model
"""
import numpy as np
from tqdm import tqdm

import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.autograd import Variable

from data_loader import DatasetHandler as Dataset
from data_loader import DatasetOptions, dataLoader

from loss import DiceLoss, computeDiceLoss
from unet import UNet

from helper import Arguments
from utils import RunningAverage

from console import Console as con
from console import Logger

def run(model : UNet,
        loaderTrain : DataLoader,
        loaderValid : DataLoader,
        optimizer : optim.Adam,
        logger : Logger, 
        args : Arguments):

    best = 1
    
    with tqdm(total = args.epochs) as t:
        for epoch in range(args.epochs):
            t.set_description("Epoch {}".format(epoch))
            
            logger.info("Epoch {}:".format(epoch))
            trainLoss = train(model, loaderTrain, optimizer, args)
            validLoss = validate(model, loaderValid, args)
            
            # Add LR scheduler maybe
            
            logger.info("Train Loss {:05.4f}, Validation Loss {:05.4f}".format(trainLoss, validLoss))
            t.update()
            
            if best > validLoss:
                epochSaved = epoch
                best = validLoss
                logger.infoh("Saving model in epoch {}".format(epoch))
                torch.save({'epoch': epoch,
                            'model_state_dict': model.state_dict(),
                            'optimizer_state_dict': optimizer.state_dict(),
                            'valLoss': validLoss,
                            'trainLoss': trainLoss}, 
                            args.weights,'model.pt'))

    return validLoss

def train(model : UNet, 
          dataLoader : DataLoader,
          optmizer : optim.Adam,
          args : Arguments):
    """
    Train step for one epoch
    - A Full pass through the whole training set
    """
    # Image : AKA batch
    
    loaderTrain = dataLoader
    model.train()
    
    lossValue = RunningAverage()

    with tqdm(total = len(dataLoader)) as t:
        t.set_description('Trainig')
        
        for i, data in enumerate(loaderTrain):
            
            image, label = data
            image, label = image.to(args.device), label.to(args.device)
            image, label = Variable(image), Variable(label)
            prediction = model(image)
            loss = computeDiceLoss(label.long(), prediction)
            
            optmizer.zero_grad()
            loss.backward()
            optmizer.step()
            
            lossValue.update(loss.item())
            t.set_postfix(loss = "{:05.3f}".format(lossValue()))
            t.update()
    
    return lossValue.avg

def validate(model : UNet,
             dataLoader : DataLoader,
             args : Arguments):
    
    loaderValid = dataLoader
    model.eval()
    
    lossValue = RunningAverage()
    
    with tqdm(total = len(loaderValid)) as t:
        t.set_description('Validation')
        
        for i, data in enumerate(loaderValid):
            
            image, label = data
            image, label = image.to(args.device), label.to(args.device)
            image, label = Variable(image), Variable(label)
            prediction = model(image)
            loss = computeDiceLoss(label.long(), prediction)
            
            lossValue.update(loss.item())
    
    return lossValue.avg