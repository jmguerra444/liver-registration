# Script to convert bad models into traced modeles, used for evaluation,
# Hardcode model name into script

import torch
import torch.optim as optim
import logging

from unet import UNet
from helper import loadSettings, Arguments, loadState


settings_path = "C://Master thesis//master//2d-unet-liver-ct//configuration.json"
# model_path = "C://Master thesis//master//exported-results//02091448//02091448-005.pt" # 1
# model_path = "C://Master thesis//master//exported-results//02071921//02071921-010.pt" # 2
model_path = "C://Master thesis//master//exported-results//02081335//02081335-010.pt" # 4


settings = loadSettings(settings_path)
args = Arguments(settings["Arguments"])

unet = UNet(**settings["2d-unet-params"])
optimizer = optim.Adam(unet.parameters())
unet, optimizer, epoch, trainLoss, validLoss = loadState(model_path, unet, optimizer, args)

ph = torch.zeros(1, 1, 256, 256)
traced_net = torch.jit.trace(unet, ph)

# README : This notation means, nature of model, amount of noise, and rotations
# torch.jit.save(traced_net, "bad-lowdose-0.pt")
# torch.jit.save(traced_net, "bad-lowdose-1.pt")
# torch.jit.save(traced_net, "bad-lowdose-2.pt")
torch.jit.save(traced_net, "bad-lowdose-4.pt")


# [1] 02091448-005.pt : (256, 256) (2) No noise, small rotations (-5, 5)
# [4] 02081335-010.pt : (256, 256) (2) 50% Data with increased noise, with much more rotations and crops
# [2] 02071921-010.pt : (256, 256) (2) 50% Data with increased noise
# [] 02071134-009.pt : (256, 256) (2) Trained with little no crop, rotations(10°), labeled + 30% non-labeled, 30% corrupted with noise images
# [] 02041952-006.pt : (512, 512) (2) Trained using crop and rotations(180°) with labeled + 30% non-labeled
# [0] 12181327-018.pt : (256, 256) (3) Trained using the plain decathlon set only with labeled images

# [3] [EL BUENO] 02222159-014.pt : (256, 256) (2) Noise on30% of the images, rotations on 10%, no crop, uses 30% of images with no labe