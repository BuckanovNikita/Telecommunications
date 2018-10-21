from IPPackage import *
import sys
from PyQt5.QtWidgets import *
from RawSocket import RawSocket
from PackageWidget import PackageWidget
import random
import string

filter_value = ''


def filter_f():
    global filter_value
    packet_list.clear()
    if proto_field.text() == '':
        filter_value = ''
        return
    try:
        filter_value = int(proto_field.text())
    except:
        if not proto_field.text() == '':
            proto_field.setText("")


def test(x):
    if packet_list.count() > 70:
        packet_list.clear()
    with open("packets/"+(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))+".txt", 'w') as f:
        f.write(str(x))
        f.write(x.raw_str)
        f.write(x.ascii_str)

    if filter_value == '' or x.protocol == filter_value:

        item = QListWidgetItem(packet_list)
        item_widget = PackageWidget(x)
        item.setSizeHint(item_widget.sizeHint())
        packet_list.addItem(item)
        packet_list.setItemWidget(item, item_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    s = RawSocket()

    main_window = QWidget()
    main_window.setWindowTitle('lab 2 task 4')
    main_window.setLayout(QVBoxLayout())

    control_panel = QWidget()
    main_window.layout().addWidget(control_panel)
    control_panel.setLayout(QVBoxLayout())
    start_btn = QPushButton("Start sniffer")
    start_btn.clicked.connect(lambda x: s.sock_init())
    control_panel.layout().addWidget(start_btn)
    stop_btn = QPushButton("Stop sniffer")
    stop_btn.clicked.connect(lambda x: s.sock_stop())
    control_panel.layout().addWidget(stop_btn)

    filter_panel = QWidget()
    filter_panel.setLayout(QHBoxLayout())
    main_window.layout().addWidget(filter_panel)
    filter_panel.layout().addWidget(QLabel("Protocol:"))
    proto_field = QLineEdit()
    main_window.layout().addWidget(proto_field)
    filter_button = QPushButton("Filter")
    main_window.layout().addWidget(filter_button)
    filter_button.clicked.connect(lambda x: filter_f())

    packet_list = QListWidget()

    main_window.layout().addWidget(packet_list)

    main_window.show()

    s.packet_arrive.connect(test)
    s.start()

    sys.exit(app.exec_())
