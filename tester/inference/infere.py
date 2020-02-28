# input : image
# output : prediction

import torch
import torchvision.transforms.functional as tf
from torch.autograd import Variable
from skimage.transform import resize


import numpy as np

import matplotlib.pyplot as plt
from inference.unet import UNet

def infere(image):

    ###############################
    ### MODIFY THIS ACCORDINGLY ###

    modelPath = "inference//02222159-014.pt"
    checkpoint = torch.load(modelPath)

    settings = {'in_channels': 1, 
                'initialFeatures': 32, 
                'out_channels': 2}
    ##############################

    unet = UNet(**settings)
    unet.load_state_dict(checkpoint["model_state_dict"])
    unet.cuda()
    unet.eval()

    ##############################
    ### DO SOME PREPROCESSING ####
    

    image = np.float32(image)
    image_ = image

    image = tf.to_pil_image(image)
    image = tf.resize(image, size = (256, 256), interpolation = 2)
    image = tf.to_tensor(image)
    image = image.unsqueeze(0)
    image = image.to('cuda:0')
    image = Variable(image)

    pred = unet(image)
    pred = np.argmax(pred.cpu().detach().numpy()[0, :, :, :], 0)
    pred = resize(pred, (512, 512), preserve_range = True, order = 0)

    return image_, pred

