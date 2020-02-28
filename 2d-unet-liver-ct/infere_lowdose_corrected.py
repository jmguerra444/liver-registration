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
from skimage.io import imsave
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

def loadState(path, model, optmizer, args):
    
    checkpoint = torch.load(path)
    model.load_state_dict(checkpoint["model_state_dict"])
    optmizer.load_state_dict(checkpoint["optimizer_state_dict"])
    epoch = checkpoint["epoch"]
    validLoss = checkpoint["validLoss"]
    trainLoss = checkpoint["trainLoss"]

    return model, optmizer, epoch, validLoss, trainLoss


# Define experiment params

def infere(p):
    settings = loadSettings()
    args = Arguments(settings["Arguments"])

    modelPath = "C:/Master thesis/master/exported-results/{}/{}-{}.pt".format(p["session"], p["session"], p["epoch"])
    volumePath =  "C:/Master thesis/Selected MR data/{}/LOWDOSE-CT".format(p["patient"])
    resultsPath_side = "C:/Master thesis/master/exported-results/000_LOW_DOSE_INFERENCE/{}/{}-{}/side/".format(p["patient"], p["session"], p["epoch"])
    resultsPath_mask = "C:/Master thesis/master/exported-results/000_LOW_DOSE_INFERENCE/{}/{}-{}/mask/".format(p["patient"], p["session"], p["epoch"])
    os.makedirs(resultsPath_side, exist_ok = True)
    os.makedirs(resultsPath_mask, exist_ok = True)

    volume = dcmread(volumePath) # TODO: Latter make this also return the metadata so we can keep dims
                                 # For whatever reason, this returns the image rotated
    settings["2d-unet-params"]["out_channels"] = p["channels"]

    unet = UNet(**settings["2d-unet-params"])
    optimizer = optim.Adam(unet.parameters())
    unet, optimizer, epoch, trainLoss, validLoss = loadState(modelPath, unet, optimizer, args)
    unet.cuda()
    unet.eval()

    savePrediction = True
    saveMask = False
    with tqdm(total = volume.shape[2]) as t:
        
        # for slice_ in range(50, voqqlume.shape[2] - 90):
        for slice_ in range(0, volume.shape[2]):
            
            t.set_description("Slice : {}".format(slice_))
            image_ = volume[:, :, slice_]
            
            image = np.float32(image_)
            image = tf.to_pil_image(image)
            image = image.rotate(90)   # vtk loads the image rotated for some reason.. like wtf brah
            image_ = image # Save image "status" to display

            image = tf.resize(image, size = (p["size"], p["size"]), interpolation = 2)
            image = tf.to_tensor(image)
            image = image.unsqueeze(0)
            image = image.to(args.device)
            image = Variable(image)
            
            pred = unet(image)
            pred = np.argmax(pred.cpu().detach().numpy()[0, :, :, :], 0)
            pred = resize(pred, (512, 512), preserve_range = True, order = 0)
            
            image_ = np.asarray(image_)

            imsave("{}/{:03d}.png".format(resultsPath_mask, slice_), np.uint8(pred))
            
            if savePrediction:

                plt.figure(figsize = (16, 8))

                plt.subplot(1, 2, 1)
                plt.imshow(image_, vmin = -100, vmax = 400)
                plt.axis('off')

                plt.subplot(1, 2, 2)
                plt.imshow(pred, vmin = 0, vmax = 2)
                plt.axis('off')

                plt.tight_layout()
                plt.tight_layout()
                plt.savefig("{}/{:03d}.png".format(resultsPath_side, slice_))
            
            if saveMask:
                image_ = np.array(image_)
                mask = image_ * pred
                plt.imshow(mask)
                # plt.show()
                
                plt.figure()
                plt.imshow(image_)
                # plt.show()

            t.update()

# %%
"""
02091448-005.pt : (256, 256) (2) No noise, small rotations (-5, 5)
02081335-010.pt : (256, 256) (2) 50% Data with increased noise, with much more rotations and crops
02071921-010.pt : (256, 256) (2) 50% Data with increased noise
02071134-009.pt : (256, 256) (2) Trained with little no crop, rotations(10°), labeled + 30%, 30% corrupted with noise images
02041952-006.pt : (512, 512) (2) Trained using crop and rotations(180°) with labeled + 30% non-labeled
12181327-018.pt : (256, 256) (3) Trained using the plain decathlon set only with labeled images


CORRECTED
02222159-014.pt : (256, 256) (2) Noise on30% of the images, rotations on 10%, no crop, uses 30% of images with no label

"""

# # New Patient
# infere({"size" : 256, "channels" : 2, "session" : "02091448", "epoch" : "005", "patient" : "021"})
# infere({"size" : 256, "channels" : 2, "session" : "02081335", "epoch" : "010", "patient" : "021"})
# infere({"size" : 256, "channels" : 2, "session" : "02071921", "epoch" : "010", "patient" : "021"})
# infere({"size" : 256, "channels" : 2, "session" : "02071134", "epoch" : "009", "patient" : "021"})
# infere({"size" : 512, "channels" : 2, "session" : "02041952", "epoch" : "006", "patient" : "021"})
# infere({"size" : 256, "channels" : 3, "session" : "12181327", "epoch" : "018", "patient" : "021"})

# New Model
# infere({"size" : 256, "channels" : 2, "session" : "02222159", "epoch" : "014", "patient" : "006"})
infere({"size" : 256, "channels" : 2, "session" : "02222159", "epoch" : "014", "patient" : "007"})
infere({"size" : 256, "channels" : 2, "session" : "02222159", "epoch" : "014", "patient" : "013"})
infere({"size" : 256, "channels" : 2, "session" : "02222159", "epoch" : "014", "patient" : "017"})
infere({"size" : 256, "channels" : 2, "session" : "02222159", "epoch" : "014", "patient" : "020"})
infere({"size" : 256, "channels" : 2, "session" : "02222159", "epoch" : "014", "patient" : "021"})

# %%
