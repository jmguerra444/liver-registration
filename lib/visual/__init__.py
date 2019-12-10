import numpy as np
import matplotlib.pyplot as plt
from math import ceil

class SliceView(object):
    def __init__(self, ax, X):
        self.ax = ax
        ax.set_title("Use scroll wheel to navigate images")
        self.X = X  
        rows, cols, self.slices = X.shape
        self.ind = self.slices * 7 // 10
        self.im = ax.imshow(self.X[:, :, self.ind], vmin = np.min(X), vmax = np.max(X))
        self.update()

    def onscroll(self, event):
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        self.im.set_data(self.X[:, :, self.ind])
        self.ax.set_ylabel('slice %s' % self.ind)
        self.im.axes.figure.canvas.draw()

def viewer(X, my_title = ''):
    """
    viewer
    -----------
    Natigate through slices of 3 Dimension numpy arrays. Usage:
    
        >>> import visual
        >>> from numpy import random
        >>> A = random.rand(100,100,100)
        >>> visual.viewer(A)
    """
    fig, ax = plt.subplots()
    tracker = SliceView(ax, X)
    fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
    if (my_title != ''):
        plt.suptitle(my_title , fontsize = 18, y = 0.98)
        plt.title("Press [Q] to exit ", color="grey", style='italic')
        
    plt.show()
    while True:
        if plt.waitforbuttonpress():
            break
    plt.close(fig)

def collage(images, cols = 2, save = False, filename = "", show = False):
    """
    Saves in this order
    \n
     [0 1] \t
     [2 3] \t
     [4 5] \t
     ...   \t
    - images : List of images to be saved
    - cols : Cols to save
    - save : Saves collage into filename
    - filename
    - displays collage
    
    Example :
    \n
     a = [np.random.random((64,64)),
          np.random.random((64,64)),
          np.random.random((64,64))]

     filename = "C:/Users/Jorgue Guerra/Desktop/example.png"

     collage(a, cols = 2, save = True, filename = filename)
    """
    # TODO : Hide axis
    
    rows = ceil(len(images) / 2)
    
    fig = plt.figure()
    for i, image in enumerate(images):
        fig.add_subplot(rows, cols, i + 1).imshow(image)
    
    if save:
        fig.savefig(filename)
    
    if show:
        plt.show(fig)

a = [np.random.random((64,64)),
     np.random.random((64,64)),
     np.random.random((64,64))]

filename = "C:/Users/Jorgue Guerra/Desktop/example.png"

collage(a, cols = 2, save = True, filename = filename)