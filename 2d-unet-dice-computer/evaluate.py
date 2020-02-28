# %%
import glob
import numpy as np
import matplotlib.pyplot as plt

from statistics import stdev, mean
from skimage.io import imread
from skimage.transform import rotate

from dice import dice

def volread(path, fix_position = False):
    """
    Stolen from: https://stackoverflow.com/a/3207973/7474885
    """
    fileList = glob.glob("{}/*.*".format(path))

    images = []
    for file_ in fileList:
        image = imread(file_)
        images.append(image)
    return images

def compute_dice(patient, session, epoch):

    # In image format
    predPath = "C:/Master thesis/master/exported-results/000_LOW_DOSE_INFERENCE/{}/{}-{}/mask/".format(patient, session, epoch)
    manuPath = "C:/Master thesis/master/2d-unet-dice-computer/LD_MANUAL/{}/".format(patient)

    pred = volread(predPath)
    manu = volread(manuPath)

    pred.reverse()

    dice_ = []
    for slice_ in range(len(manu)):
        slicePred = pred[slice_]
        sliceManu = manu[slice_]
        
        dice_.append(dice(sliceManu, slicePred))
        # print(avgList(dice_))

        if False:
            plt.figure(figsize = (16, 8))

            plt.subplot(1, 2, 1)
            plt.imshow(slicePred)
            
            plt.subplot(1, 2, 2)
            plt.imshow(sliceManu)
            
            plt.tight_layout()
            # plt.show()
            plt.close('all')
    
    print("Patient: {}, Session: {}, Dice: {:.3f}".format(patient, session, mean(dice_)))
    return mean(dice_)

# %%
"""
Some description of this experiment
02091448-005.pt
"""

patients = [
            "006", 
            "007", 
            "013", 
            "017", 
            "020", 
            "021"
            ]
models = [
          ("02041952", "006"), 
          ("02071134", "009"), 
          ("02071921", "010"), 
          ("02081335", "010"), 
          ("02091448", "005"),
          ("02222159", "014"),
         ]


for m in models:
    dices_models = []
    dices_patients = [0] * len(patients)

    i = 0 
    for p in patients:
        d = compute_dice(patient = p, session = m[0], epoch = m[1])
        dices_models.append(d)
        dices_patients[i] = dices_patients[i] + d
        i += 1
    print ("Average : {:.3f}".format(mean(dices_models)))
    print ("Deviation : {:.3f}".format(stdev(dices_models)))
    print ("\n\n")

for i in range(len(dices_patients)):
    r = dices_patients[i] / len(models)
    print("Patient : {}, mean dice : {:.3f}".format(patients[i], r))
print("Done!")
