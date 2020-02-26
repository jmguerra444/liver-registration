import json
import platform
from datetime import datetime


import torch

def loadSettings(filename = "configuration.json"):
    """
    Loads configuration settings for this session from configuration.json
    """
    try:
        thisComputer = platform.node()
        with open(filename) as json_file:
            data = json.load(json_file)
        return data[thisComputer]
    except:
        print("Not valid configuration file")
        return

class Arguments:
    """
    ## Arguments
    ----
    Only hyperparameter related arguments, batch size, learning rate, epochs etc etc.
    DataLoading parameters in DataLoaderManager class
    \n
    Params
    - batch_size
    - epochs
    - lr
    - device
    - workers
    - weights
    - logs
    - graphs
    - image_size
    - train : % Images from available train set to use
    - validation : % Of images from selected train to use for dataset split
    """
    def __init__(self,
                 args = "None",
                 batch_size = 16,
                 epochs = 10,
                 lr = 0.001,
                 device = "cuda:0",
                 workers = 4,
                 vis_images = 200,
                 vis_freq = 10,
                 weights = "./weights",
                 logs = "./logs",
                 graphs = "./graphs",
                 image_size = 256,
                 train = 1,
                 validation = 0.1
                 ):
        
        if args == "None":
            self.batch_size = batch_size
            self.epochs = epochs
            self.lr = lr
            self.device = device
            self.workers = workers
            self.weights = weights
            self.logs = logs
            self.graphs = graphs
            self.image_size = image_size
            self.train = train
            self.validation = validation
            
        else:
            self.batch_size = args["batch_size"]
            self.epochs = args["epochs"]
            self.lr = args["lr"]
            self.device = args["device"]
            self.workers = args["workers"]
            self.weights = args["weights"]
            self.logs = args["logs"]
            self.graphs = args["graphs"]
            self.image_size = args["image_size"]
            self.train = args["train"]
            self.validation = args["validation"]

        self.id = now()
        self.vis_images = vis_images
        self.vis_freq = vis_freq

def now():
    time_ = datetime.now()
    time_str = time_.strftime("%m%d%H%M")
    return time_str


def loadState(path, model, optmizer, args):
    
    checkpoint = torch.load(path)
    model.load_state_dict(checkpoint["model_state_dict"])
    optmizer.load_state_dict(checkpoint["optimizer_state_dict"])
    epoch = checkpoint["epoch"]
    validLoss = checkpoint["validLoss"]
    trainLoss = checkpoint["trainLoss"]

    return model, optmizer, epoch, validLoss, trainLoss