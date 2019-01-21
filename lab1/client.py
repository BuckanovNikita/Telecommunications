import sys

from socketwrapper import SocketWrapper
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ip_widget import IPWidget


def test(msg, own=False):
    list_item = QListWidgetItem()
    list_item.setText(msg)
    if own:
        list_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
    msg_list.addItem(list_item)
    msg_field.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QWidget()
    main_window.setWindowTitle('lab 1 task 4')
    main_window.setLayout(QVBoxLayout())

    server_ip = IPWidget("Server IP:", main_window)

    receiver_ip = IPWidget("Receiver IP:", main_window)

    instance_panel = QWidget()
    instance_panel.setLayout(QHBoxLayout())

    port_field = QLineEdit()

    server_socket = SocketWrapper(server_ip, receiver_ip, port_field)
    server_socket.start()

    conn_panel = QWidget()
    conn_panel.setLayout(QHBoxLayout())

    conn_btn = QPushButton("Connect")
    conn_btn.clicked.connect(server_socket.sock_init)

    disconnect_btn = QPushButton("Disconnect")
    disconnect_btn.clicked.connect(server_socket.close)

    user_list_btn = QPushButton("User list")
    user_list_btn.clicked.connect(lambda x: server_socket.msg_send("", True))

    status_label = QLabel("not connected")
    server_socket.conn_status.connect(status_label.setText)

    msg_list = QListWidget()

    msg_panel = QWidget()
    msg_panel.setLayout(QHBoxLayout())

    msg_field = QTextEdit()

    msg_send_btn = QPushButton("Send")
    msg_send_btn.clicked.connect(lambda x: server_socket.msg_send(msg_field.toPlainText()))

    encrypt_btn = QPushButton("Send encrypt")
    encrypt_btn.clicked.connect(lambda x: server_socket.msg_send(msg_field.toPlainText(), False, True))

    msg_status = QLabel()
    server_socket.msg_status.connect(msg_status.setText)

    server_socket.write_to_chat.connect(lambda x: test(x, True))
    server_socket.msg_receive.connect(test)

    main_window.layout().addWidget(server_ip)
    main_window.layout().addWidget(receiver_ip)
    main_window.layout().addWidget(instance_panel)

    instance_panel.layout().addWidget(QLabel("Listen port:"))
    instance_panel.layout().addWidget(port_field)

    main_window.layout().addWidget(conn_panel)

    conn_panel.layout().addWidget(conn_btn)
    conn_panel.layout().addWidget(disconnect_btn)
    conn_panel.layout().addWidget(user_list_btn)

    conn_panel.layout().addWidget(status_label)

    main_window.layout().addWidget(msg_list)
    main_window.layout().addWidget(msg_panel)

    msg_panel.layout().addWidget(msg_field)
    msg_panel.layout().addWidget(msg_send_btn)
    msg_panel.layout().addWidget(encrypt_btn)

    main_window.layout().addWidget(msg_status)

    main_window.show()
    sys.exit(app.exec_())
