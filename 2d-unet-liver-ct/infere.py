"""
Inference script giving a high resolution nifti volume path, label and model

!!! Change the size and output channles is required
"""


# %% Inference method
import os
import sys
import numpy as np
sys.path.append(os.path.abspath("../lib"))

import nibabel
from tqdm import tqdm
from skimage.transform import resize
import matplotlib.pyplot as plt

import torch
import torch.optim as optim
import torchvision.transforms.functional as tf
from torch.autograd import Variable

from unet import UNet

from utils import loadSettings, normalizeArray
from helper import Arguments

from visual import viewer

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


model_path = "C:/Master thesis/master/exported-results/12181327/12181327-004.pt"
volume_path =  "C:/Master thesis/master/data/medical-decathlon/imagesTr/liver_85.nii.gz"
label_path = "C:/Master thesis/master/data/medical-decathlon/labelsTr/liver_85.nii.gz"


volume = np.array(nibabel.load(volume_path).get_fdata(), dtype = np.float32)
labels = np.array(nibabel.load(label_path).get_fdata(), dtype = np.float32)
prediction = np.zeros_like(labels)

#### CHANGE THIS IS NEEDED ####
settings["2d-unet-params"]["out_channels"] = 3
size = 256
###############################

unet = UNet(**settings["2d-unet-params"])
optimizer = optim.Adam(unet.parameters())
unet, optimizer, epoch, trainLoss, validLoss = loadState(model_path, unet, optimizer, args)
unet.cuda()
unet.eval()

collection = []
with tqdm(total = volume.shape[2]) as t:
    
    # for slice_ in range(50, volume.shape[2] - 90):
    for slice_ in range(440, 445):
        
        t.set_description("Slice : {}".format(slice_))
        image = volume[:, :, slice_]
        label = labels[:, :, slice_]
        
        image = tf.to_pil_image(image)
        image_ = image # Save image "status" to display

        image = tf.resize(image, size = (size, size), interpolation = 2)
        image = tf.to_tensor(image)
        image = image.unsqueeze(0)
        image = image.to(args.device)
        image = Variable(image)
        
        pred = unet(image)
        pred = np.argmax(pred.cpu().detach().numpy()[0, :, :, :], 0)
        pred = resize(pred, (512, 512), preserve_range = True, order = 0)

        plt.figure(figsize = (16, 8))
        plt.subplot(1, 3, 1)
        plt.imshow(image_, vmin = -100, vmax = 400)
        plt.axis('off')

        plt.subplot(1, 3, 2)
        plt.imshow(label, vmin = 0, vmax = 2)
        plt.axis('off')
        
        plt.subplot(1, 3, 3)
        plt.imshow(pred, vmin = 0, vmax = 2)
        plt.axis('off')
        
        plt.tight_layout()
        plt.tight_layout()
        plt.show()

        t.update()

# %%
