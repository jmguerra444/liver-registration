import os


class Arguments:
    """
    ## Arguments
    ----
    - Only hyperparameter related arguments, batch size, learning rate, epochs etc etc.
    - DataLoading parameters in DataLoaderManager class
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
                 image_size = 256
                 ):
        
        if args == "None":
            self.batch_size = batch_size
            self.epochs = epochs
            self.lr = lr
            self.device = device
            self.workers = workers
            self.weights = weights
            self.logs = logs
            self.image_size = image_size
        else:
            self.batch_size = args["batch_size"]
            self.epochs = args["epochs"]
            self.lr = args["lr"]
            self.device = args["device"]
            self.workers = args["workers"]
            self.weights = args["weights"]
            self.logs = args["logs"]
            self.image_size = args["image_size"]

        self.vis_images = vis_images
        self.vis_freq = vis_freq

def makedirs(args):
    os.makedirs(args.weights, exist_ok=True)
    os.makedirs(args.logs, exist_ok=True)
