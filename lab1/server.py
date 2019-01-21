import sys
import socket
import pickle
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ClientSocket(QThread):
    def __init__(self, sock, address, signal):
        super(ClientSocket, self).__init__()
        self.client_socket = sock
        self.signal = signal
        self.address = address

    def __del__(self):
        self.wait()

    @pyqtSlot()
    def start_(self):
        self.start()

    def run(self):
        buff_size = 1024  # 4 KiB
        while True:
            data = b''
            try:
                while True:
                    part = self.client_socket.recv(buff_size)
                    data += part
                    if len(part) < buff_size:
                        break
                if data:
                    try:
                        data = pickle.loads(data)
                    except Exception as ex:
                        self.signal.emit("Message format not supported\n"+str(ex))
                    if not data.info:
                        try:
                            if s_sock.connected[data.receiver_ip]:
                                s_sock.connected[data.receiver_ip].sendall(pickle.dumps(data))
                        except Exception as ex:
                            pass
                    else:
                        try:
                            data.text = "Connected now:"
                            for t in s_sock.connected:
                                data.text = data.text + str(t) + "\n"
                                data.receiver_ip = data.sender_ip
                                data.sender_ip = self.client_socket.getsockname()
                            self.client_socket.sendall(pickle.dumps(data))
                        except Exception as ex:
                            self.signal.emit("new\n" + str(ex))
            except Exception as ex:
                self.signal.emit("Disconnect"+str(self.address))
                if self.address in s_sock.connected:
                    del s_sock.connected[self.address]
                break


class ServerSocket(QThread):

    state_change_signal = pyqtSignal(['QString'])
    run_signal = pyqtSignal()
    need_restart = pyqtSignal()

    def __init__(self, max_connections=2):
        super(ServerSocket, self).__init__()
        self.state_change_signal.connect(status_label.setText)
        self.connected = dict()
        self.listener = None
        self.started = False
        self.max_connections = max_connections

    def __del__(self):
        self.wait()

    def restart(self):
        try:
            self.stop()
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if 1024 < int(port_field.text()) < 100000 and 0 < int(max_conn_field.text()) < 100:
                self.listener.bind(("0.0.0.0", int(port_field.text())))
                self.max_connections = int(max_conn_field.text())
            else:
                raise ValueError
            self.listener.listen(self.max_connections)
            self.state_change_signal.emit("Listening on:" + str(self.listener.getsockname()) +
                                          "\nMax connections" + str(self.max_connections))
        except Exception as ex:
            self.state_change_signal.emit("Listening error:" + str(ex))

    def stop(self):
        try:
            if self.listener:
                try:
                    self.listener.close()
                except Exception as ex:
                    pass
            for t in self.connected:
                try:
                    self.connected[t].close()
                except Exception as ex:
                    pass
            self.listener = None
            self.state_change_signal.emit('Не подключено')
        except Exception as ex:
            pass

    def run(self):
        while True:
            try:
                client_sock, address = self.listener.accept()
                self.connected[address] = client_sock
                c = ClientSocket(client_sock, address, self.state_change_signal)
                self.run_signal.connect(c.start_)
                self.run_signal.emit()
                self.run_signal.disconnect(c.start_)
            except Exception as ex:
                QThread.msleep(100)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = QWidget()
    main_window.setLayout(QHBoxLayout())

    status_label = QLabel('Not connected')

    port_field = QLineEdit()

    max_conn_field = QLineEdit()
    max_conn_field.setText("5")

    port_field.setText("1270")

    connect_btn = QPushButton("Start listening")
    disconnect_btn = QPushButton("Stop listening")

    s_sock = ServerSocket()
    s_sock.start()
    connect_btn.clicked.connect(s_sock.restart)
    disconnect_btn.clicked.connect(s_sock.stop)

    main_window.layout().addWidget(status_label)
    main_window.layout().addWidget(status_label)
    main_window.layout().addWidget(port_field)
    main_window.layout().addWidget(QLabel("Max connections: "))
    main_window.layout().addWidget(max_conn_field)
    main_window.layout().addWidget(connect_btn)
    main_window.layout().addWidget(disconnect_btn)

    main_window.show()

    sys.exit(app.exec_())