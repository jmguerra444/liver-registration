import torch
import torch.optim as optim
import logging

from unet import UNet
from helper import loadSettings, Arguments, loadState


import torch
import torch.optim as optim
import logging

from unet import UNet
from helper import loadSettings, Arguments, loadState


class Parent(torch.nn.Module):
    def __init__(self, unet):
        super(Parent, self).__init__()
        self.unet = unet

    def forward(self, ph):
        print("Doing parent")
        return self.unet(ph)

settings_path = "C://Master thesis//master//2d-unet-liver-ct//configuration.json"
model_path = "C://Master thesis//master//exported-results//02222159//02222159-014.pt"

settings = loadSettings(settings_path)
args = Arguments(settings["Arguments"])

unet = UNet(**settings["2d-unet-params"])
optimizer = optim.Adam(unet.parameters())
unet, optimizer, epoch, trainLoss, validLoss = loadState(model_path, unet, optimizer, args)

ph = torch.zeros(1, 1, 256, 256)
parent = Parent(unet)
traced_net = torch.jit.trace(parent, ph)
traced_net.save("..//model-parent.pt")
