"""
This takes args, data loader, and model
"""
import os

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.autograd import Variable

from data_loader import DatasetHandler as Dataset
from data_loader import DatasetOptions, dataLoader

from loss import computeDiceLoss
from unet import UNet

from helper import Arguments
from utils import RunningAverage, normalizeArray

from console import Console as con
from console import Logger
from visual import grid, collage

savesPerEpoch = 30

def run(model : UNet,
        loaderTrain : DataLoader,
        loaderValid : DataLoader,
        optimizer : optim.Adam,
        logger : Logger, 
        args : Arguments):

    best = 1
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience = 8, verbose = True)
    with tqdm(total = args.epochs) as t:
        for epoch in range(args.epochs):
            t.set_description("Epoch {}".format(epoch))
            
            logger.info("---Epoch {}---".format(epoch), c = False)
            trainLoss = train(model, loaderTrain, optimizer, args, logger)
            validLoss = validate(model, loaderValid, args, logger)
            scheduler.step(validLoss, epoch)
            
            # Test and save some Images
            test(model, args, loaderValid, 3, epoch)
            plt.close("all")
            # Add LR scheduler maybe
            logger.info("[E]: Epoch : {}, Train Loss {:05.4f}, Validation Loss {:05.4f}".format(epoch, trainLoss, validLoss))
            
            t.update()
            if best > validLoss:
                best = validLoss
                logger.infoh2("Saving model in epoch {}".format(epoch))
                torch.save({'epoch': epoch,
                            'model_state_dict': model.state_dict(),
                            'optimizer_state_dict': optimizer.state_dict(),
                            'validLoss': validLoss,
                            'trainLoss': trainLoss}, 
                            args.weights + "/{}-{:03d}.pt".format(args.id, epoch))

    return validLoss

def train(model : UNet, 
          dataLoader : DataLoader,
          optmizer : optim.Adam,
          args : Arguments,
          logger):
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
            loss, dices = computeDiceLoss(label.long(), prediction)
            optmizer.zero_grad()
            loss.backward()
            optmizer.step()
            
            lossValue.update(loss.item())
            
            if i % int(len(dataLoader) / savesPerEpoch) == 0:
                logger.info("[L]: {}".format(lossValue()), c = False)

            t.set_postfix(loss = "{:05.6f}".format(lossValue()))
            t.update()
    
    return lossValue.avg

def validate(model : UNet,
             dataLoader : DataLoader,
             args : Arguments,
             logger):
    """
    Validation
    """
    loaderValid = dataLoader
    model.eval()
    
    lossValue = RunningAverage()
    d1_Value = RunningAverage()
    d2_Value = RunningAverage()
    d3_Value = RunningAverage()
    
    with tqdm(total = len(loaderValid)) as t:
        t.set_description('Validation')
        for i, data in enumerate(loaderValid):
            image, label = data
            image, label = image.to(args.device), label.to(args.device)
            image, label = Variable(image), Variable(label)
            prediction = model(image)
            loss, dices = computeDiceLoss(label.long(), prediction)
            
            lossValue.update(loss.item())
            d1_Value.update(dices[0].item())
            d2_Value.update(dices[1].item())
            d3_Value.update(dices[2].item())
            
            if i % int(len(dataLoader) / savesPerEpoch) == 0:
                logger.info("[V]: {}".format(lossValue()), c = False)
                logger.info("[D1]: {}".format(d1_Value()), c = False)
                logger.info("[D2]: {}".format(d2_Value()), c = False)
                logger.info("[D3]: {}".format(d3_Value()), c = False)
            
            t.set_postfix(loss = "{:05.6f}".format(lossValue()))
            t.update()
    
    return lossValue.avg

def test(model : UNet,
         args : Arguments,
         loader,
         samples,
         epoch):
    """
    Just a visual check of model's output
    """
    
    model.eval()
    collection = []
    
    for i, data in enumerate(loader):
        
        if i == samples:
            break
        
        image, label = data
        image, label = image.to(args.device), label.to(args.device)
        image, label = Variable(image), Variable(label)
        prediction = model(image)
        
        image = image.cpu().detach().numpy()[0, 0, :, :]
        label = label.cpu().detach().numpy()[0, 0, :, :]
        labelMap = np.argmax(prediction.cpu().detach().numpy()[0, :, :, :], 0)
        
        collection.append(normalizeArray(image))
        collection.append(normalizeArray(label))
        collection.append(normalizeArray(labelMap))

    path = "{}/{}".format(args.graphs, args.id)
    os.makedirs(path, exist_ok = True)
    filename = "{}/{}-{:03d}.png".format(path, args.id, epoch)
    
    grid(collection, cols = 3, save = True, filename = filename)
    
    return labelMap

def randomSampler(loader):
    # OBSOLETE
    """
    Returns random sample (batch) from loaded
    """
    image = iter(loader).next()[0]
    label = iter(loader).next()[1]
    
    return image, label
