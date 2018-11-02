from PyQt5.QtCore import *
from ftplib import FTP
import datetime
from FileWriter import FileWriter
from PyQt5.QtWidgets import *

class FtpWrapper(QThread):
    progress = pyqtSignal(['int'])
    end = pyqtSignal([])
    bad = pyqtSignal(['PyQt_PyObject'])

    def __init__(self, server_name, file_name, path):
        super(FtpWrapper, self).__init__()
        self.file_name = file_name
        self.server_name = server_name
        self.path = path
        self.size = 0
        self.get = 0

    def __del__(self):
        self.wait()

    def setText(self, text):
        self.text = text

    def write(self, block):
        self.get += len(block)
        done = int(100*self.get / self.size)
        self.progress.emit(done)
        open(self.path + '/' + self.file_name, 'ab').write(block)

    def run(self):
        msg = 'Server: ' + self.server_name + '\n' + \
              'path: ' + self.path + '/' + self.file_name + '\n' + \
              'time: ' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + '\n'
        try:
            self.bad.emit('Wait for connection to '+ self.server_name)
            ftp = FTP(self.server_name)
            self.bad.emit('Wait for connected to ' + self.server_name)
        except Exception as ex:
            msg +=ex
            return
        try:
            ftp.login()
            self.size = ftp.size(self.file_name)
            open(self.path + '/' + self.file_name, 'wb').write(b'')
            ftp.retrbinary('RETR ' + self.file_name, self.write)
            msg = 'Success:\n' + msg
        except Exception as ex:
            msg += ex
            return

        finally:
            self.bad.emit(msg)
            self.end.emit()
            ftp.close()