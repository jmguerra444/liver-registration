from PyQt5 import uic
from PyQt5.QtWidgets import (QMainWindow, QWidget, QApplication)
from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5.QtGui import QIcon

import nibabel
import time
import numpy as np
import matplotlib.pyplot as plt

from widgets import FileEdit, WaitDialog, getStyle
from process import LoadingThread
from log_reader import log_reader

from viewer import viewer

class Window(QMainWindow):
    
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('window.ui', self)
        self.setupUI()
        self.wait = WaitDialog()
        self.threads = []
        
        self.fileEdit = FileEdit(self.dropLabel)
        self.fileEdit.dropped.connect(self.fileDropped)
        
    def setupUI(self):
        self.setWindowTitle("Tester")
        self.setFixedSize(465, 651)
        self.setWindowIcon(QIcon('wizard.ico'))
        pass
    
    def showWait(self):
        self.wait.show()
        
    def hideWait(self):
        self.wait.hide()
        
    def fileDropped(self, filename, filetype):
        if filetype == "none":
            self.mainText.append('<font color = "red">file not supported</font>')
            return
        self.mainText.append("Loading {}".format(filename))
        self.showWait()
        
        thread = LoadingThread(filename, filetype)
        thread.loaded.connect(self.display)
        thread.start()
        self.threads.append(thread)
    
    def display(self, data, datatype):
        self.hideWait()
        
        if datatype == "png":
            # plt.imshow(np.mean(data, 2))
            plt.imshow(data)
            plt.axis('off')
            plt.show()
        
        if datatype == "nii":
            viewer(data)

        if datatype == "log":
            log_reader(data)
    
app = QApplication([])
window = Window()
window.setStyleSheet(getStyle())
window.show()
window.setWindowState(window.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
window.activateWindow()
app.exec_()