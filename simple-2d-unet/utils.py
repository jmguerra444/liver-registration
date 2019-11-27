import sys
import os
sys.path.append(os.path.abspath("../lib"))

import json
import csv
import numpy as np

from console import Console as con

def loadSettings(filename):
    """
    Loads configuration settings for this session from configuration.json
    """
    try:
        thisComputer = os.environ['COMPUTERNAME']
        with open(filename) as json_file:
            data = json.load(json_file)
        return data[thisComputer]
    except:
        con.printw("Not valid configuration file")
        return

def loadFromCSV(filename):
    """
    Loads a list from .CSV file
    """
    output = []
    with open(filename, 'r') as file:
        r = csv.reader(file)
        output = list(r)
    return output


def normalizeSample(sample):
    """
    Normalizes a numpy array from 0 to 1
    """
    return (sample - np.min(sample))/(np.max(sample) - np.min(sample))