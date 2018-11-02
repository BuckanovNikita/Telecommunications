from PyQt5.QtCore import *
from ftplib import FTP
from PyQt5.QtWidgets import *

class FileWriter(QThread):
    progress = pyqtSignal(['int'])
    end = pyqtSignal(['PyQt_PyObject'])
    bad = pyqtSignal(['PyQt_PyObject'])

    def __init__(self, path, size):
        super(FileWriter, self).__init__()
        self.buffer = b''
        self.size = size
        self.upload = 0
        self.file = open(path, 'wb')

    def __del__(self):
        self.wait()

    def add(self, t):
        self.buffer += t

    def run(self):
        while self.upload < self.size:
            if self.buffer:
                self.file.write(self.buffer)
                self.upload += len(self.buffer)
                self.buffer = b''
            QThread.msleep(100)