# Import modules
from utils import *

from os.path import join
from math import ceil
from random import shuffle

import nibabel
import json

class DataLoaderJSON:
    """
    DataLoaderJSON
    -----
    (Maybe: Rename as ImageManagerClass) \n
    Loads Folder data from JSON file and returns image data of X batch size uppon request.\n
    `@Param jsonFile    # Dataset configuration file` \n
    `@Param pathPRefix  # Origin of images` \n
    `@Param batch       # Number of images to be returned by getBatch, batchSize % numTraining = 0` \n
    `@Param validation  # Number of images for validation` \n
    """
    
    def __init__(self, 
                 jsonFile,
                 pathPrefix = "",
                 batchSize = 1,
                 validation = 0
                 ):
        
        self.jsonFile = jsonFile
        self.pathPrefix = pathPrefix
        self.batchSize = batchSize
        
        self.labels = {}
        self.numTest = 0
        self.numTotalTraining = 0
        self.numTrainig = 0
        self.numValidation = validation
        
        self.testImages = []
        self.trainingImages = []
        self.trainingLabels = []
        
        self.imageCounter = 0 # Last image loaded

        self.trainigDeck = [] # Queue of images to feed training proccess
        self.validationDeck = []

        self.readJSON(validation)

    def readJSON(self, validation):
        try:
            with open(self.jsonFile) as json_file:
                data = json.load(json_file)
            
            self.labels = data["labels"]
            self.numTest = data["numTest"]
            self.numTotalTraining = data["numTraining"]
            self.testImages = data["test"]
            
            # TODO refactor, do not split
            self.trainingImages = [join(self.pathPrefix, i["image"]) for i in data["training"]]
            self.trainingLabels = [join(self.pathPrefix, i["label"]) for i in data["training"]]
            
            self.numTrainig = self.numTotalTraining - self.numValidation

            print("Images have been found:")
            print(CF.green, "Training Images: ", self.numTrainig, CF.e)
            print(CF.green, "Validation Images: ", self.numValidation, CF.e)
            print(CF.green, "Test Images: ", self.numTest, CF.e)
        except:
            print("Invalid data properties")

        return True
        
    # TODO: Implement
    def getBatch(self, imageDeck = "Tr", increaseCounter = True):
        
        if (imageDeck == "Tr"):
            requestedPaths = [i for i in self.trainigDeck[self.imageCounter: self.imageCounter + self.batchSize]]        
        if (increaseCounter):
            self.imageCounter = overflowNum(self.imageCounter, self.batchSize, self.numTrainig)

        requestedImages = [nibabel.load(path[0]).get_fdata() for path in requestedPaths]
        requestedLabel = [nibabel.load(path[1]).get_fdata() for path in requestedPaths]

        return requestedImages, requestedLabel
    
    def splitTrainigData(self):
        
        if (self.numTotalTraining % self.batchSize != 0):
            raise NameError("Batch size not multiple ")

        trainIndex = 0
        for i in self.trainingImages[:self.numTrainig]:
            self.trainigDeck.append((self.trainingImages[trainIndex], self.trainingLabels[trainIndex]))
            trainIndex += 1
            
        validIndex = 0
        for i in self.trainingImages[self.numTrainig:]:
            self.validationDeck.append((self.trainingImages[validIndex], self.trainingLabels[validIndex]))
            validIndex += 1
            
        return True
        
    
    def shuffleImages(self):
        self.imageCounter = 0
        
        imageIndexes = list(range(self.numTotalTraining))
        shuffle(imageIndexes)
        
        self.trainingImages = [self.trainingImages[i] for i in imageIndexes] 
        self.trainingLabels = [self.trainingLabels[i] for i in imageIndexes] 

        return True
