import torch
import torchvision.transforms.functional as tf
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
from helper import dcmread


vol_path = "C://Master thesis//master//imfusion-inference//trace-model//lowdose_2"
model_path = "C://Master thesis//master//imfusion-inference//trace-model//liver-coarse.pt"
model_path_ = "C://Master thesis//master//imfusion-inference//trace-model//lowdose-liver.pt"
image_path = "C://Master thesis//master//imfusion-inference//trace-model//sample.jpg"

mod = torch.jit.load(model_path)
mod_ = torch.jit.load(model_path_)
im = tf.to_tensor(np.array(imread(image_path, as_gray=True), dtype = np.float32))
vol = dcmread(vol_path)
vol = tf.to_tensor(vol)

print("k")
# pred = mod()mod.