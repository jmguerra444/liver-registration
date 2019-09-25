from utils import *
from data_loader import *

s = loadSettings()

dataLoader = DataLoaderJSON(jsonFile = "01-dataset.json",
                            pathPrefix = s["decathlon-dataset-path"],
                            batch = 1, 
                            validation = 0.1
                            )
dataLoader.shuffleImages()
dataLoader.splitTrainigData()

print("Done!")