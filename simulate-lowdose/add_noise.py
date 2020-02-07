# %% Rad transform

import numpy as np

from skimage.io import imread, imsave
from skimage.transform import radon, iradon
from skimage.transform import rotate, resize

def normalize(sample):

    """
    - Substracts minima
    - Normalizes a numpy array from 0 to 1
    """
    minima = np.min(sample)             # To restore scale
    maxima = np.max(sample)
    out = (sample - np.min(sample))/(np.max(sample) - np.min(sample))
    return out, minima, maxima

def restore(sample, minima, maxima):
    out = (sample * (maxima - minima)) + minima
    return out

def simulateLowdose(image):
    """
    Simulates low dose scan from high resolution 2D CT highscan image, based on:\n
    https://www.ncbi.nlm.nih.gov/pubmed/26543245 \n
    Params
    - image: input image as array
    Returns
    - reconstructedNoise: reconstructed image with noise
    """

    size = image.shape
    image, minima, maxima = normalize(image)
    image = resize(image, (256, 256), anti_aliasing = True, preserve_range = True, order = 1)

    parameters = {"lam" : 1e5, "mi" : 0, "sd" : 30 / (maxima - minima)}
    theta = np.linspace(0., 180., max(image.shape), endpoint = False)
    sinogram = radon(image, theta = theta, circle = True)

    sinogramNoise = np.copy(sinogram)

    for i in range(0, sinogram.shape[0]):
        proj = sinogramNoise[:, i]
        proj = proj / 100                   # Bacause come weird overflow error

        proj = parameters["lam"] * np.exp(-proj)
        P = np.random.poisson(proj)
        G = parameters["sd"] * np.random.randn(len(proj)) + parameters["mi"]
        projNoise = np.log(parameters["lam"] / (P + 0.1))       # Poisson noise
        projNoise = projNoise + G                               # Gaussian noise
        sinogramNoise[:, i] = projNoise

    reconstructionNoise = iradon(sinogramNoise * 100, theta=theta, circle=True)
    # reconstructionNoise, _, _ = normalize(reconstructionNoise) 
    reconstructionNoise = restore(reconstructionNoise, minima, maxima)
    reconstructionNoise = resize(reconstructionNoise, size, anti_aliasing = True, preserve_range = True, order = 1)
    return reconstructionNoise, sinogram, sinogramNoise


def saveLowDose(filename_in, filename_out):
    image = imread(filename_in)
    imageNoise, _, _ = simulateLowdose(image)
    imageNoise = imageNoise.astype(np.int16)
    imsave(filename_out, imageNoise)

def test(filename_):

    import matplotlib.pyplot as plt
    filename = filename_
    image = imread(filename, as_gray = True)

    print("Adding noise to {}".format(filename))

    imageNoise, sinogram, sinogramNoise = simulateLowdose(image)
    imageNoise = imageNoise.astype(np.int16)

    imsave("to convert_2/{}_noise{}".format(filename,".tif"), imageNoise)

    fig, axes = plt.subplots(1, 3, figsize=(8, 8))
    axes[0].axis("off")
    axes[0].set_title("Original")
    axes[0].imshow(image, cmap = plt.cm.Greys_r, vmin = -100, vmax = 400)

    axes[1].axis("off")
    axes[1].set_title("Noisy FBP reconstruction")
    axes[1].imshow(imageNoise, cmap = plt.cm.Greys_r, vmin = -100, vmax = 400)

    axes[2].set_title("Comparison over the 200th projection")
    axes[2].plot(sinogramNoise[:, 200] * 100, 'r')
    axes[2].plot(sinogram[:, 200], 'g')

    fig.tight_layout()
    fig.tight_layout()
    fig.tight_layout()

    plt.show()

# test("test1.tif")
# test("test2.tif")
# test("test3.tif")

# %%
