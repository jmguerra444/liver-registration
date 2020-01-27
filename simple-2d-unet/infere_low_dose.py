# %% Inference method
import os
import sys
import numpy as np
from PIL import Image
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
from miscellaneous import dcmread

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

# %%
settings = loadSettings()
args = Arguments(settings["Arguments"])


modelPath = "C:/Master thesis/master/exported-results/12181327/12181327-004.pt"
volumePath =  "C:/Users/Jorgue Guerra/Desktop/test_low_dose"

volume = dcmread(volumePath)

unet = UNet(**settings["2d-unet-params"])
optimizer = optim.Adam(unet.parameters())
unet, optimizer, epoch, trainLoss, validLoss = loadState(modelPath, unet, optimizer, args)
unet.cuda()
unet.eval()

collection = []
with tqdm(total = volume.shape[2]) as t:
    
    # for slice_ in range(50, voqqlume.shape[2] - 90):
    for slice_ in range(20, 70, 10):
        
        t.set_description("Slice : {}".format(slice_))
        image_ = volume[:, :, slice_]
        
        image = np.float32(image_)
        image = tf.to_pil_image(image)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image = tf.resize(image, size = (256, 256), interpolation = 2)
        image_ = image # Save image "status" to display
        
        image = tf.to_tensor(image)
        image = image.unsqueeze(0)
        image = image.to(args.device)
        image = Variable(image)
        
        pred = unet(image)
        pred = np.argmax(pred.cpu().detach().numpy()[0, :, :, :], 0)
        pred = resize(pred, (512, 512))
        
        plt.subplot(1, 2, 1)
        plt.imshow(image_)
        plt.subplot(1, 2, 2)
        plt.imshow(pred)
        plt.show()
        
        # prediction[:, :, slice_] = pred
        
        # sl = normalizeArray(volume[:, :, slice_])
        # stack = np.hstack((sl, label * 30, pred * 30))
        # collection.append(stack)
        # plt.imshow(pred)
        # plt.show()
        t.update()

print("Donie!")
# s = np.asarray(collection)
# s = np.transpose(s, (2, 1, 0))
# viewer(s)

# %%
