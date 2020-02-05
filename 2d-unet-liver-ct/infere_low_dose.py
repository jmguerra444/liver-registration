# %%
print("starting")
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

# modelPath = "C:/Master thesis/master/exported-results/02041952/02041952-006.pt"
modelPath = "C:/Master thesis/master/exported-results/12181327/12181327-018.pt"; 

volumePath =  "C:/Master thesis/Selected MR data/006/LOWDOSE-CT"
volume = dcmread(volumePath)

settings["2d-unet-params"]["out_channels"] = 3
size = 256         # Change this according to the size that the NET was trained with

unet = UNet(**settings["2d-unet-params"])
optimizer = optim.Adam(unet.parameters())
unet, optimizer, epoch, trainLoss, validLoss = loadState(modelPath, unet, optimizer, args)
unet.cuda()
unet.eval()

collection = []

savePrediction = True
saveMask = False
with tqdm(total = volume.shape[2]) as t:
    
    # for slice_ in range(50, voqqlume.shape[2] - 90):
    for slice_ in range(0, 78):
        
        t.set_description("Slice : {}".format(slice_))
        image_ = volume[:, :, slice_]
        
        image = np.float32(image_)
        image = tf.to_pil_image(image)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image_ = image # Save image "status" to display

        image = tf.resize(image, size = (size, size), interpolation = 2)
        image = tf.to_tensor(image)
        image = image.unsqueeze(0)
        image = image.to(args.device)
        image = Variable(image)
        
        pred = unet(image)
        pred = np.argmax(pred.cpu().detach().numpy()[0, :, :, :], 0)
        pred = resize(pred, (512, 512), preserve_range = True, order = 0)
        
        if savePrediction:
            plt.subplot(1, 2, 1)
            plt.imshow(image_)
            plt.axis('off')
            plt.subplot(1, 2, 2)
            plt.imshow(pred)
            plt.axis('off')
            plt.tight_layout()
            plt.savefig("{}/out2/{:03d}.png".format(volumePath, slice_))
        
        if saveMask:
            image_ = np.array(image_)
            mask = image_ * pred
            plt.imshow(mask)
            # plt.show()
            
            plt.figure()
            plt.imshow(image_)
            # plt.show()
            print("bp")
        # plt.show()
        
        # prediction[:, :, slice_] = pred
        
        # sl = normalizeArray(volume[:, :, slice_])
        # stack = np.hstack((sl, label * 30, pred * 30))
        # collection.append(stack)
        # plt.imshow(pred)
        # plt.show()
        t.update()

print("Donie!")



# %%
