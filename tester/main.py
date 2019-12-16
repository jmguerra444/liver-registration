from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QLabel,
                             QTextEdit,
                             QLineEdit,
                             QPushButton,
                             QFileDialog,
                             QComboBox,
                             QVBoxLayout,
                             QSizePolicy)

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

class Window(QWidget):
    """
    Main UI thread
    """

    def __init__(self):
        super(Window, self).__init__()
        self.setupUI()
        self.wait = WaitDialog()
        self.threads = []
        
        self.fileEdit = FileEdit(self.message)
        self.fileEdit.dropped.connect(self.fileDropped)
    
    def setupUI(self):
        
        window_x = 500
        window_y = 500
        
        self.setWindowTitle("Thesis tester")
        self.setFixedSize(window_x, window_y)
        self.setWindowIcon(QIcon('wizard.ico'))
        
        # Define Widgets
        self.label1 = QLabel()
        self.label1.setText("<i>Drop file to load</i>")
        
        self.message = QLineEdit()
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # sizePolicy.setVerticalStretch()
        self.message.resize(200, 200)
        self.message.setReadOnly(True)
        self.message.setSizePolicy(sizePolicy)
        
        self.resultArea = QTextEdit()
        self.resultArea.setReadOnly(True)
        
        # Add Widgets to window
        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.message)
        layout.addWidget(self.resultArea)
        
        self.setLayout(layout)
    
    def showWait(self):
        self.wait.show()
        
    def hideWait(self):
        self.wait.hide()
        
    def fileDropped(self, filename, filetype):
        if filetype == "none":
            self.resultArea.append('<font color = "red">file not supported</font>')
            return
        self.resultArea.append("Loading {}".format(filename))
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
app.setStyleSheet(getStyle())
window = Window()
window.show()
window.setWindowState(window.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
window.activateWindow()
app.exec()