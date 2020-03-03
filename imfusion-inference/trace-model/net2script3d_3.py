import torch
import torch.optim as optim
import logging

from unet import UNet
from helper import loadSettings, Arguments, loadState


# scripted_gate = torch.jit.script(UNet())
# my_cell = MyCell(scripted_gate)
# traced_cell = torch.jit.script(my_cell)

class Unet3D(torch.nn.Module):

    def __init__(self, unet):
        super(Unet3D, self).__init__()
        p = torch.zeros(1, 1, 256, 256)
        self.traced_net = torch.jit.trace(unet, p)

    def forward(self, x):
        out = torch.zeros(1, 2, 5, 256, 256)
        for i in range(x.size(2)):
            im = x[:, :, i, :, :]
            pred = unet(im)
            out[:, :, i, :, :] = pred
            print(i)
        return out

settings_path = "C://Master thesis//master//2d-unet-liver-ct//configuration.json"
model_path = "C://Master thesis//master//exported-results//02222159//02222159-014.pt"

settings = loadSettings(settings_path)
args = Arguments(settings["Arguments"])

unet = UNet(**settings["2d-unet-params"])
optimizer = optim.Adam(unet.parameters())
unet, optimizer, epoch, trainLoss, validLoss = loadState(model_path, unet, optimizer, args)

# imag = torch.zeros(1, 1, 256, 256)
# traced_net = torch.jit.trace(unet, imag)
# traced_net.save("lowdose-liver-fake.pt")
# print(traced_net.code)
# print(traced_net.graph)

volu = torch.zeros(1, 1, 5, 256, 256)
unet3 = Unet3D(unet)
traced_unet3 = torch.jit.trace(unet3, volu)
traced_unet3.save("3d-TEST.pt")