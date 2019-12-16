# !/usr/bin/env python
# -*- coding:utf-8 -*-
from PyQt5.QtCore import (Qt, pyqtSignal)

from PyQt5.QtWidgets import (QApplication,
                             QMessageBox,
                             QWidget,
                             QLabel,
                             QLineEdit,
                             QTextEdit,
                             QVBoxLayout)

from PyQt5.QtGui import QIcon

import sys
import os


class FileEdit(QLineEdit):
    
    dropped = pyqtSignal(str, str)
    
    def __init__(self, parent):
        super(FileEdit, self).__init__(parent)

        self.setDragEnabled(True)
        self.resize(500, 1000)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        
        data = event.mimeData()
        urls = data.urls()
        
        if urls and urls[0].scheme() == 'file':
            filepath = str(urls[0].path())[1:]
            print(filepath)
            
            # any file type here
            if filepath[-6:] == "nii.gz" or filepath[-6:] == "NII.GZ":
                self.dropped.emit(filepath, "nii")
                return
            if filepath[-4:] == ".png" or filepath[-4:] == ".PNG":
                self.dropped.emit(filepath, "png")
                return

            if filepath[-4:] == ".log" or filepath[-4:] == ".LOG":
                self.dropped.emit(filepath, "log")
                return

            self.dropped.emit(filepath, "none")


class WaitDialog(QWidget):
    
    def __init__(self):
        super(WaitDialog, self).__init__()
        self.setupUI()
        
    def setupUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(200, 200)
        
        self.label1 = QLabel()

        self.label1.setText("""
                            <center>
                                <font size="18">
                                    ⏱
                                    <br>
                                    Please wait
                                </font>
                            </center>
                            """)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        self.setLayout(layout)


def getStyle():
    
    style = '''
            QWidget {
                font-family: "Consolas";
                }
            '''
    
    return style