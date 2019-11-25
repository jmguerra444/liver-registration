import os
import sys
sys.path.append(os.path.abspath("../lib"))

import csv
import nibabel
import numpy as np
from os.path import join

from utils import *
from console import Console as con

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

def scanTrainDataset(pathPrefix,
                    datasetSchema,
                    samples,
                    outputImageFile,
                    outputLabelFile,
                    outputIndexFile):
    """
    Creates the absolute path for every slice, stores as (num slices) niftipaths
    and another file with the slice indexes.
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
        
        # numSlices = image.shape[2]
        if (volume.shape[2] == labels.shape[2]):
            for sliceIndex in range(volume.shape[2]):
                image = volume[:, :, sliceIndex]
                label = labels[:, :, sliceIndex]
                
                ####################
                # TODO: Check that slice has label
                #####################
                
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



settings = loadSettings("configuration.json")

# Scan nifti filles and save in csv file all paths and indexes of image and label
scanTrainDataset(pathPrefix = settings["decathlon-dataset-path"],
                datasetSchema = "01-dataset.json",
                samples = 5,
                outputImageFile = settings["decathlon-scanned-image"],
                outputLabelFile = settings["decathlon-scanned-label"],
                outputIndexFile = settings["decathlon-scanned-index"])


ImagePaths = loadFromCSV(settings["decathlon-scanned-image"])[0]
LabelPaths = loadFromCSV(settings["decathlon-scanned-label"])[0]
IndexPaths = loadFromCSV(settings["decathlon-scanned-index"])[0]
con.printgr("Done!")