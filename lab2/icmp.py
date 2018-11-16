from PyQt5.QtWidgets import *
from IcmpHeader import IcmpHeader
import socket
import sys


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
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        package = IcmpHeader(type_, code_)
        s.sendto(package.raw, (destination_ip.text(), 0))
    except Exception as msg:
        print(msg)
        status_label.setText(str(msg))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = QWidget()
    main_window.setWindowTitle('lab 2 task 4')

    start_btn = QPushButton("Generate")
    start_btn.clicked.connect(lambda x: generate1())

    destination_ip = QLineEdit()

    icmp_type = QLineEdit()

    icmp_code = QLineEdit()

    status_label = QLabel("")

    main_window.setLayout(QVBoxLayout())
    main_window.layout().addWidget(start_btn)
    main_window.layout().addWidget(QLabel('Destination IP'))
    main_window.layout().addWidget(destination_ip)
    main_window.layout().addWidget(QLabel('ICMP TYPE'))
    main_window.layout().addWidget(icmp_type)
    main_window.layout().addWidget(QLabel('ICMP CODE'))
    main_window.layout().addWidget(icmp_code)
    main_window.layout().addWidget(status_label)
    main_window.show()

    sys.exit(app.exec_())
