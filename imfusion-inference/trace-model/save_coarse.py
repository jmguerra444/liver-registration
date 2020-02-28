import torch
import torch.optim as optim
import logging


# model_path = "C://Master thesis//master//imfusion-inference//trace-model//lowdose-liver.pt"
model_path = "C://Master thesis//master//imfusion-inference//trace-model//liver-coarse.pt"

model = torch.jit.load(model_path)

print(model.code)
# print(model.graph)