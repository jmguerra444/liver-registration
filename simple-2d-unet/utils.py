import sys
import os
sys.path.append(os.path.abspath("../lib"))

import json
import csv
import ast
import numpy as np
from datetime import datetime

from console import Console as con

class RunningAverage():
    """
    A simple class that maintains the running average of a quantity
    
    Example:
    ```
    loss_avg = RunningAverage()
    loss_avg.update(2)
    loss_avg.update(4)
    loss_avg() = 3
    ```
    """
    def __init__(self):
        self.steps = 0
        self.total = 0
    
    def update(self, val):
        self.total += val
        self.steps += 1
        self.avg = self.total/float(self.steps)
    
    def __call__(self):
        return self.total/float(self.steps)

def loadSettings(filename = "configuration.json"):
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

def exec(function, a, b):
    """
    Executes pair operations

        def power(a):
            return a * a

        a2, b2 = exec(power, 5, 4)
        print(a2, b2)
        
        >>> 25 16
    """
    out_a = function(a)
    out_b = function(b)
    return out_a, out_b

def normalizeSample(sample):
    """
    Normalizes a numpy array from 0 to 1
    """
    return (sample - np.min(sample))/(np.max(sample) - np.min(sample))

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

def now():
    time_ = datetime.now()
    time_str = time_.strftime("%d%m%H%M")
    return time_str