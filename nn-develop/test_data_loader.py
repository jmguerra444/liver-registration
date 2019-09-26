from utils import *
from utils_visual import *
from data_loader import *

s = loadSettings()

dataLoader = DataLoaderJSON(jsonFile = "01-dataset.json",
                            pathPrefix = s["decathlon-dataset-path"],
                            batchSize = 2, 
                            validation = 21
                            )
dataLoader.shuffleImages()
dataLoader.splitTrainigData()

image, label = dataLoader.getBatch(imageDeck = "Tr", increaseCounter = False)

sliceViewer(image[0])
sliceViewer(label[0])
print("Done!")