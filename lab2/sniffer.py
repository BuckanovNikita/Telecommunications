import sys
from PyQt5.QtWidgets import *
from RawSocket import RawSocket
from PackageWidget import PackageWidget
import random
import string

filter_value = ''


def filter():
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


def on_packet_arrive(x):
    if packet_list.count() > 70:
        packet_list.clear()

    with open("packets/" + (''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))) + ".txt",
              'w') as f:
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
    control_panel.setLayout(QVBoxLayout())

    start_btn = QPushButton("Start sniffer")
    start_btn.clicked.connect(lambda x: s.sock_init())

    stop_btn = QPushButton("Stop sniffer")
    stop_btn.clicked.connect(lambda x: s.sock_stop())

    control_panel.layout().addWidget(start_btn)
    control_panel.layout().addWidget(stop_btn)

    filter_panel = QWidget()
    filter_panel.setLayout(QHBoxLayout())
    filter_panel.layout().addWidget(QLabel("Protocol:"))

    proto_field = QLineEdit()

    filter_button = QPushButton("Filter")
    filter_button.clicked.connect(lambda x: filter())

    packet_list = QListWidget()

    main_window.layout().addWidget(control_panel)
    main_window.layout().addWidget(filter_panel)
    main_window.layout().addWidget(proto_field)
    main_window.layout().addWidget(filter_button)
    main_window.layout().addWidget(packet_list)
    main_window.show()

    s.packet_arrive.connect(on_packet_arrive)
    s.start()

    sys.exit(app.exec_())
