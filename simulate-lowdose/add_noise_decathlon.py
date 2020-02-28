# Takes the scan file of medical decathlon and simulates "lowdose-CT" to 30% of the cases

import sys
import csv
import ast

from tqdm import tqdm
from numpy.random import randint
from add_noise import saveLowDose

filename = sys.argv[1]
# filename = "C:/Master thesis/master/data/medical-decathlon-tif/images-list.csv"
print(filename)

def loadFromCSV(filename):
    """
    Loads a list from .CSV file
    """
    output = []
    with open(filename, 'r') as file:
        r = csv.reader(file)
        output = list(r)
    return output

def unpack(paths):
    """
    Takes the split of the list that contains the lists os volume slices
    """
    images = []
    for volume in paths: 
        volumeList = ast.literal_eval(volume)
        for slice_ in volumeList: 
            images.append(slice_)
    return images

imagesList = loadFromCSV(filename)[0]
imagesList = unpack(imagesList)

counter = 0
with tqdm(total = len(imagesList)) as t:
    for image in imagesList:
        counter += 1
        t.set_description("Slice : {}".format(counter))

        lottery = randint(0, 10)
        if lottery < 4:
            saveLowDose(image, image)
        
        t.update()

print("Done!")