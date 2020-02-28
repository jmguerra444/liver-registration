from PyQt5.QtCore import (QThread,
                          pyqtSignal)

import nibabel
import numpy as np
from imageio import imread
import pydicom

from viewer import viewer

class LoadingThread(QThread):

    loaded = pyqtSignal(object, str)
    
    def __init__(self, filename, filetype):
        super(LoadingThread, self).__init__()
        self.filename = filename
        self.filetype = filetype

    def run(self):

        if self.filetype == "nii":
            data = np.array(nibabel.load(self.filename).get_fdata())
            
        if self.filetype in ["png", "tif"]:
            data = np.asarray(imread(self.filename))
        
        if self.filetype == "log":
            data = self.filename
        
        if self.filetype == "dcm":
            d = pydicom.dcmread(self.filename)
            data = d.pixel_array + d.RescaleIntercept
        
        self.loaded.emit(data, self.filetype)

