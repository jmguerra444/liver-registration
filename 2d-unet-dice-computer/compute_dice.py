# %%
import glob
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.transform import rotate

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

def avgList(list_):

    acc = 0
    for i in list_:
        acc += i
    return acc / len(list_)

def dice(im1, im2, empty_score=1.0):
    """
    Computes the Dice coefficient, a measure of set similarity.
    Parameters
    ----------
    im1 : array-like, bool
        Any array of arbitrary size. If not boolean, will be converted.
    im2 : array-like, bool
        Any other array of identical size. If not boolean, will be converted.
    Returns
    -------
    dice : float
        Dice coefficient as a float on range [0,1].
        Maximum similarity = 1
        No similarity = 0
        Both are empty (sum eq to zero) = empty_score
        
    Notes
    -----
    The order of inputs for `dice` is irrelevant. The result will be
    identical if `im1` and `im2` are switched.

    Stolen from https://gist.github.com/brunodoamaral/e130b4e97aa4ebc468225b7ce39b3137
    """

    im1 = np.asarray(im1).astype(np.bool)
    im2 = np.asarray(im2).astype(np.bool)

    if im1.shape != im2.shape:
        raise ValueError("Shape mismatch: im1 and im2 must have the same shape.")

    im_sum = im1.sum() + im2.sum()
    if im_sum == 0:
        return empty_score

    # Compute Dice coefficient
    intersection = np.logical_and(im1, im2)

    return 2. * intersection.sum() / im_sum

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
    
    print("Patient: {}, Session: {}, Dice: {}".format(patient, session, avgList(dice_)))

# %%
"""
Some description of this experiment
"""
compute_dice(patient = "006", session = "02071134", epoch = "009")
compute_dice(patient = "006", session = "02041952", epoch = "006")
compute_dice(patient = "006", session = "02071921", epoch = "010")
# compute_dice(patient = "007", session = "02071134", epoch = "009") # TODO: Segment this
# compute_dice(patient = "013", session = "02071134", epoch = "009")
# compute_dice(patient = "017", session = "02071134", epoch = "009")
# compute_dice(patient = "020", session = "02071134", epoch = "009")

print("Done!")
