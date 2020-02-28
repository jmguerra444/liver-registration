import torch
import torch.optim as optim
import logging

from unet import UNet
from helper import loadSettings, Arguments, loadState


settings_path = "C://Master thesis//master//2d-unet-liver-ct//configuration.json"
model_path = "C://Master thesis//master//exported-results//02222159//02222159-014.pt"


settings = loadSettings(settings_path)
args = Arguments(settings["Arguments"])

unet = UNet(**settings["2d-unet-params"])
optimizer = optim.Adam(unet.parameters())
unet, optimizer, epoch, trainLoss, validLoss = loadState(model_path, unet, optimizer, args)

ph = torch.zeros(1, 1, 256, 256)
traced_net = torch.jit.trace(unet, ph)
traced_net.save("lowdose-liver.pt")

print(traced_net.code)
print(traced_net.graph)
