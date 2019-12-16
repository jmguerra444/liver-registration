# %% Inference method
import torch
import torch.optim as optim

from unet import UNet

from utils import loadSettings
from helper import Arguments

def infere(volume, model, optimizer, args):
    pass

def loadState(path, model, optmizer, args):
    
    checkpoint = torch.load(path)
    model.load_state_dict(checkpoint["model_state_dict"])
    optmizer.load_state_dict(checkpoint["optimizer_state_dict"])
    epoch = checkpoint["epoch"]
    validLoss = checkpoint["validLoss"]
    trainLoss = checkpoint["trainLoss"]

    return model, optmizer, epoch, validLoss, trainLoss


settings = loadSettings()
args = Arguments(settings["Arguments"])


path = "C:/Master thesis/master/simple-2d-unet/weights/12161153-001.pt"

unet = UNet(settings["2d-unet-params"])
optimizer = optim.Adam(unet.parameters())

unet, optimizer, epoch, trainLoss, validLoss = loadState(path, unet, optimizer, args)
