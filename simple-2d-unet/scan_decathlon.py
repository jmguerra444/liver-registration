# %%
# Imports and stuff

import os
import sys
sys.path.append(os.path.abspath("../lib"))

import csv
import nibabel
import numpy as np
from os.path import join
from imageio import imwrite

from utils import *
from utils import normalizeSample
from console import Console as con

#%%
def readConfigurationFile(pathPrefix, mode, datasetSchema):
    """
    Builds absolute image paths from configuration files
    """
    try:
        with open(datasetSchema) as cf:
            data = json.load(cf)

        train = data["training"]
        test = data["test"]
        test = [join(pathPrefix, image) for image in test]
        for i in train:
            i["image"] = join(pathPrefix, i["image"])
            i["label"] = join(pathPrefix, i["label"])

        if (mode == "train"):
            return train
        if (mode == "test"):
            return test
        
    except:
        con.printw("Invalid data properties")

def loadFromCSV(filename):
    """
    Loads a list from .CSV file
    """
    output = []
    with open(filename, 'r') as file:
        r = csv.reader(file)
        output = list(r)
    return output

# %%
def scanTrainDataset(pathPrefix,
                    datasetSchema,
                    samples,
                    outputImageFile,
                    outputLabelFile,
                    outputIndexFile,
                    onlyWithLabel):
    """
    Creates the absolute path for every slice, stores as (num slices) niftipaths
    and another file with the slice indexes.
    `onlyWithLabel` to save only the paths that contain a label
    """
    paths = readConfigurationFile(pathPrefix, "train", datasetSchema)
    absoluteImagePath = []
    absoluteLabelPath = []
    absoluteIndexes = []
    
    if (samples == "ALL"):
        samples = len(paths)
    
    con.printbl("Scanning...")
    for sample in paths[0: samples]:
        volume = np.array(nibabel.load(sample["image"]).get_fdata(), dtype = np.float32)
        labels = np.array(nibabel.load(sample["label"]).get_fdata(), dtype = np.float32)
                                                                     
        if (volume.shape[2] == labels.shape[2]):
            for sliceIndex in range(volume.shape[2]):
                image = volume[:, :, sliceIndex]
                label = labels[:, :, sliceIndex]

                hasLabel = np.any(label != 0)
                if (hasLabel and onlyWithLabel):
                    absoluteImagePath.append(sample["image"])
                    absoluteLabelPath.append(sample["label"])
                    absoluteIndexes.append(sliceIndex)
                    

                if (not onlyWithLabel):
                    absoluteImagePath.append(sample["image"])
                    absoluteLabelPath.append(sample["label"])
                    absoluteIndexes.append(sliceIndex)
                    
        print("Unique labels", np.unique(labels))
        print("Finished :", sample["image"])
    
    con.printbl("Saving list...")
    with open(outputImageFile, "w", newline = '') as file:
        wr = csv.writer(file, quoting = csv.QUOTE_ALL)
        wr.writerow(absoluteImagePath)

    with open(outputLabelFile, "w", newline = '') as file:
        wr = csv.writer(file, quoting = csv.QUOTE_ALL)
        wr.writerow(absoluteLabelPath)

    with open(outputIndexFile, "w", newline = '') as file:
        wr = csv.writer(file, quoting = csv.QUOTE_ALL)
        wr.writerow(absoluteIndexes)
    
    return True

# %% 
def saveAsPNG(outputDirectory,
              imagePaths, 
              labelPaths, 
              indexes):
    
    """
    Takes all the volumes in the absolute image/label path and saves them as PNG image
    """
    
    path = ""
    volume = np.zeros((1,1))
    labels = np.zeros((1,1))
    imageFilenames = []
    labelFilenames = []
    
    for index in range(len(imagePaths)):
        imagePath = imagePaths[index]
        s = int(indexes[index])                     # The slice index
        
        if (imagePath != path):
            path = imagePath
            con.printbl("Doing {}".format(path))
            
            volume = np.array(nibabel.load(path).get_fdata(), dtype = np.float32)
            labels = np.array(nibabel.load(labelPaths[index]).get_fdata(), dtype = np.float32)
            volume = normalizeSample(volume)        # In range [0 1]
            
            
        image = np.uint8((volume[:, :, s]) * 255)   # Range [0 255]
        label = np.uint8((labels[:, :, s]) * 50)    # Increase constrst on labels (visually), TODO : Remove
        
        imageFilename = "{}/image/image{:06d}.png".format(outputDirectory, index)
        labelFilename = "{}/label/label{:06d}.png".format(outputDirectory, index)
        
        imwrite(imageFilename, image)
        imwrite(labelFilename, label)
        
        imageFilenames.append(imageFilename)
        labelFilenames.append(labelFilename)
        #####################
        # MAYBE :  Do some image operations
        #####################
        
    listImagesFilename = "{}/images-list.csv".format(outputDirectory)
    listLabelsFilename = "{}/labels-list.csv".format(outputDirectory)
    
    with open(listImagesFilename, "w", newline = '') as file:
        wr = csv.writer(file, quoting = csv.QUOTE_ALL)
        wr.writerow(imageFilenames)

    with open(listLabelsFilename, "w", newline = '') as file:
        wr = csv.writer(file, quoting = csv.QUOTE_ALL)
        wr.writerow(labelFilenames)
    return 0


#%% Load folder settings
settings = loadSettings("configuration.json")

#%%
# Scan nifti filles and save in csv file all paths and indexes of image and label
scanTrainDataset(pathPrefix = settings["decathlon-dataset-path"],
                datasetSchema = "01-dataset.json",
                samples = 10,
                outputImageFile = settings["decathlon-scanned-image"],
                outputLabelFile = settings["decathlon-scanned-label"],
                outputIndexFile = settings["decathlon-scanned-index"],
                onlyWithLabel = True)
#%%
imagePaths = loadFromCSV(settings["decathlon-scanned-image"])[0]
labelPaths = loadFromCSV(settings["decathlon-scanned-label"])[0]
indexPaths = loadFromCSV(settings["decathlon-scanned-index"])[0]

con.printgr("Saving slices")
saveAsPNG(settings["decathlon-output-png"],
          imagePaths,
          labelPaths,
          indexPaths)

con.printgr("Done!")

# %%

# USE THIS

# c:\Master thesis\master\simple-2d-unet\scan_decathlon.py:32: DeprecationWarning: `imsave` is deprecated!
# `imsave` is deprecated in SciPy 1.0.0, and will be removed in 1.2.0.
# Use ``imageio.imwrite`` instead.
#   if (mode == "train"):