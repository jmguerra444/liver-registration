from pynput import keyboard
import time
from PyQt5.QtCore import QObject, pyqtSignal

class KeyMonitor(QObject):
    letterPressed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.listener = keyboard.Listener(on_release = self.on_release)

    def on_release(self,key):
        if type(key) == keyboard._win32.KeyCode:
            self.letterPressed.emit(key.char.lower())

    def stop_monitoring(self):
        self.listener.stop()

    def start_monitoring(self):
        self.listener.start()