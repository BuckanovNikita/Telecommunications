from socket import *
from IPPackage import *
from PyQt5.QtCore import *

buf_size = 64 * 1024 * 8


class RawSocket(QThread):
    packet_arrive = pyqtSignal(['PyQt_PyObject'])

    def __init__(self):
        super(RawSocket, self).__init__()
        self.sock = None
        self.name = None
        self.address = None
        self.need_init = False

    def __del__(self):
        self.wait()

    def sock_stop(self):
        self.need_init = False
        if self.sock:
            self.sock.close()
            self.sock = None

    def sock_init(self):
        self.need_init = True
        if self.sock:
            self.sock.close()
            self.sock = None

    def run(self):
        while True:
            if self.need_init:
                self.sock = socket(AF_INET, SOCK_RAW, IPPROTO_IP)
                self.name = gethostname()
                self.address = gethostbyname(self.name)
                socket.bind(self.sock, (self.address, 100))
                socket.ioctl(self.sock, SIO_RCVALL, 1)
                self.need_init = False
            while self.sock:
                try:
                    t = self.sock.recv(buf_size)
                    if t:
                        package = IPPackage(t)
                        self.packet_arrive.emit(package)
                except Exception as ex:
                    print(ex)
                    break
                QThread.msleep(1)
            QThread.msleep(1)
