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
        
        self.clsButton.clicked.connect(self.mainText.clear)
        
        self.model = "None"
        
    def setupUI(self):
        self.setWindowTitle("Tester")
        self.setFixedSize(465, 651)
        self.setWindowIcon(QIcon('wizard.ico'))
        
        
        self.dropLabel.setStyleSheet("""
                                     color : #4A2B75;
                                     """)
        pass
    
    def showWait(self):
        self.wait.show()
        
    def hideWait(self):
        self.wait.hide()
        
    def fileDropped(self, filename, filetype):
        if filetype == "none":
            self.appendText("File not supported", "red")
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
            message = "Loaded image, Shape : {}, Min : {}, Max : {}".format(data.shape, data.min(), data.max())
            self.appendText(message, "blue")
            plt.imshow(data)
            plt.axis('off')
            plt.show()
        
        if datatype == "nii":
            message = "Loaded volume, Shape : {}, Min : {}, Max : {}".format(data.shape, data.min(), data.max())
            self.appendText(message, "blue")
            viewer(data)
            
        if datatype == "log":
            log_reader(data)
    
    def appendText(self, text, color = "black"):
        self.mainText.append("""
                             <font color = "{}">
                             {}
                             </font>
                             """.format(color, text))

    
app = QApplication([])
window = Window()
window.setStyleSheet(getStyle())
window.show()
window.setWindowState(window.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
window.activateWindow()
app.exec_()