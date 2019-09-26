from utils import *
from data_loader import *

s = loadSettings()

dataLoader = DataLoaderJSON(jsonFile = "01-dataset.json",
                            pathPrefix = s["decathlon-dataset-path"],
                            batchSize = 1, 
                            validation = 21
                            )
dataLoader.shuffleImages()
dataLoader.splitTrainigData()

image, label = dataLoader.getBatch(imageDeck = "Tr", increaseCounter = False)