import os
from random import shuffle

from utils import now, unpack

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

def makedirs(args):
    os.makedirs(args.weights, exist_ok=True)
    os.makedirs(args.logs, exist_ok=True)
    os.makedirs(args.graphs, exist_ok=True)

def splitDataset(args, imagesPath, labelsPath, batchSize):
    
    validation = args.validation
    train = args.train
    
    if train < 1:
        split = int(len(imagesPath) * train)
        imagesPath = imagesPath[:split]
    
    assert len(unpack(imagesPath)) == len(unpack(labelsPath))
    assert batchSize > 0
    
    split =  int(((len(imagesPath)) * validation))
    
    # Shuffle
    indexes = list(range(len(imagesPath)))
    shuffle(indexes)
    
    trainImages = [imagesPath[i] for i in indexes[split:]]
    trainLabels = [labelsPath[i] for i in indexes[split:]]
    
    validImages = [imagesPath[i] for i in indexes[:split]]
    validLabels = [labelsPath[i] for i in indexes[:split]]
    
    
    trainImages = unpack(trainImages)
    trainLabels = unpack(trainLabels)
    
    validImages = unpack(validImages)
    validLabels = unpack(validLabels)
    
    # Delete to make size % batch == 0
    residual = len(trainImages) % batchSize
    if residual > 0:
        trainImages = trainImages[:-residual]
        trainLabels = trainLabels[:-residual]

    residual = len(validImages) % batchSize
    if residual > 0:
        validImages = validImages[:-residual]
        validLabels = validLabels[:-residual]
    
    assert len(trainImages) % batchSize == 0
    assert len(validImages) % batchSize == 0
    
    return trainImages, trainLabels, validImages, validLabels