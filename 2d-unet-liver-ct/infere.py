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
        image = tf.resize(image, size = (256, 256), interpolation = 2)
        image = tf.to_tensor(image)
        image = image.unsqueeze(0)
        image = image.to(args.device)
        image = Variable(image)
        
        pred = unet(image)
        pred = np.argmax(pred.cpu().detach().numpy()[0, :, :, :], 0)
        # pred = resize(pred, (512, 512))
        # prediction[:, :, slice_] = pred
        
        # sl = normalizeArray(volume[:, :, slice_])
        # stack = np.hstack((sl, label * 30, pred * 30))
        # collection.append(stack)
        
        plt.imshow(label)
        plt.show()
        plt.imshow(pred)
        plt.show()
        
        t.update()

s = np.asarray(collection)
s = np.transpose(s, (2, 1, 0))
viewer(s)

# %%
