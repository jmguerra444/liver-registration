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

for i in range(20):
    reqI = dataLoader.getBatch("Tr", True)
    print(reqI)