from PyQt5.QtWidgets import *
import socket
import sys
import struct


class IcmpPacket:
    ICMP_STRUCTURE_FMT = 'bbHHh'

    def __init__(self,
                 icmp_type,
                 icmp_code=0,
                 icmp_crc=0,
                 icmp_id=1,
                 icmp_seq=1,
                 data='',
                 ):
        self.icmp_type = icmp_type
        self.icmp_code = icmp_code
        self.icmp_crc = icmp_crc
        self.icmp_id = icmp_id
        self.icmp_seq = icmp_seq
        self.data = data
        self.raw = None
        self.create_icmp_field()

    def create_icmp_field(self):
        self.raw = struct.pack(self.ICMP_STRUCTURE_FMT,
                               self.icmp_type,
                               self.icmp_code,
                               self.icmp_crc,
                               self.icmp_id,
                               self.icmp_seq,
                               )

        self.icmp_crc = self.crc(self.raw + self.data.encode())

        self.raw = struct.pack(self.ICMP_STRUCTURE_FMT,
                               self.icmp_type,
                               self.icmp_code,
                               self.icmp_crc,
                               self.icmp_id,
                               self.icmp_seq,
                               )

    def crc(self, data):
        s = 0

        for i in range(0, len(data), 2):
            a = data[i]
            b = data[i+1]

            s = s + (a + (b << 8))

        s = s + (s >> 16)
        s = ~s & 0xffff

        return s


def generate1():
    try:
        type_ = int(icmp_type.text())
        if type_ < 0:
            raise Exception('')
    except:
        status_label.setText('Bad ICMP type')
        return

    try:
        code_ = int(icmp_code.text())
        if code_ < 0:
            raise Exception('')
    except:
        status_label.setText('Bad ICMP code')
        return

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('ICMP'))
        package = IcmpPacket(type_, code_)
        s.sendto(package.raw, (destination_ip.text(), 0))
    except Exception as msg:
        print(msg)
        status_label.setText(str(msg))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    status_label = QLabel("")

    main_window = QWidget()
    main_window.setWindowTitle('lab 2 task 4')
    main_window.setLayout(QVBoxLayout())

    start_btn = QPushButton("Generate")
    start_btn.clicked.connect(lambda x: generate1())
    main_window.layout().addWidget(start_btn)

    main_window.layout().addWidget(QLabel('Destination IP'))
    destination_ip = QLineEdit()
    main_window.layout().addWidget(destination_ip)

    main_window.layout().addWidget(QLabel('ICMP TYPE'))
    icmp_type = QLineEdit()
    main_window.layout().addWidget(icmp_type)

    main_window.layout().addWidget(QLabel('ICMP CODE'))
    icmp_code = QLineEdit()
    main_window.layout().addWidget(icmp_code)

    main_window.layout().addWidget(status_label)
    main_window.show()

    sys.exit(app.exec_())

