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
        plt.suptitle(my_title, fontsize = 18, y = 0.98)
        plt.title("Press [Q] to exit ", color="grey", style='italic')
        
    plt.show()
    while True:
        if plt.waitforbuttonpress():
            break
    plt.close(fig)