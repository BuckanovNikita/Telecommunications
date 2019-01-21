import socket
from PyQt5.QtCore import *
from message import Message
import pickle
from Crypto.Cipher import AES
import random
import string


def key_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class SocketWrapper(QThread):

    conn_status = pyqtSignal(['QString'])
    msg_status = pyqtSignal(['QString'])
    write_to_chat = pyqtSignal(['QString'])
    msg_receive = pyqtSignal(['QString'])

    def __init__(self, server_ip, receiver_ip, port_label):
        super(SocketWrapper, self).__init__()
        self.server_socket = None
        self.need_init = False
        self.ip = server_ip
        self.receiver_ip = receiver_ip
        self.port_label = port_label
        self.my_crypto_keys = dict()
        self.others_crypto_keys = dict()

    def __del__(self):
        self.wait()

    def msg_send(self, text, info=False, encrypt=False):
        try:
            msg = Message(self.server_socket.getsockname(), self.receiver_ip.get_address(), text, info, encrypt)
        except:
            self.msg_status.emit("Connect first\n")
            return
        aes = None
        try:
            if encrypt:
                if msg.receiver_ip not in self.others_crypto_keys:
                    self.others_crypto_keys[msg.receiver_ip] = key_generator()
                    msg.crypto_key = self.others_crypto_keys[msg.receiver_ip]
                aes = AES.new(self.others_crypto_keys[msg.receiver_ip], AES.MODE_CFB, 'This is an IV456')
                msg.text = aes.encrypt(msg.text)
            self.server_socket.sendall(pickle.dumps(msg))
            self.msg_status.emit("Send success")
        except Exception as ex:
            self.msg_status.emit("Send error\n"+str(ex))
            print("Send error\n"+str(ex))
        try:
            if aes:
                aes = AES.new(self.others_crypto_keys[msg.receiver_ip], AES.MODE_CFB, 'This is an IV456')
                msg.text = str(aes.decrypt(msg.text).decode())
            self.write_to_chat.emit(str(msg))
        except Exception as ex:
            self.msg_status.emit("Send error\n"+str(ex))

    def sock_init(self):
        self.need_init = True
        if self.server_socket:
            self.server_socket.close()

    def run(self):
        while True:
            if self.need_init:
                if self.server_socket:
                    self.server_socket.close()
                try:
                    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.server_socket.bind(('0.0.0.0', int(self.port_label.text())))
                    self.conn_status.emit("Initialize connection")
                    address, port = self.ip.get_address()
                    self.conn_status.emit("Wait for connection" + address + ':' + str(port))
                    self.server_socket.connect((address, port))
                    self.conn_status.emit("Connected" + address + ':' + str(port))
                except Exception as ex:
                    self.conn_status.emit("Connection error\n" + str(ex))
            self.need_init = False
            buff_size = 1024
            data = b''
            while self.server_socket:
                try:
                    part = self.server_socket.recv(buff_size)
                except Exception as ex:
                    self.conn_status.emit("Receive error" + str(ex))
                    break
                data += part
                if len(part) < buff_size:
                    break
            if data:
                try:
                    data = pickle.loads(data)
                    if data.encrypted:
                        if data.crypto_key != "":
                            self.my_crypto_keys[data.sender_ip] = data.crypto_key
                        key = self.my_crypto_keys[data.sender_ip]
                        aes = AES.new(key, AES.MODE_CFB, 'This is an IV456')
                        data.text = str(aes.decrypt(data.text).decode())
                    self.msg_receive.emit(str(data))
                except Exception as ex:
                    self.conn_status.emit("Message unpickling error\n"+str(ex))
            QThread.msleep(100)

    def close(self):
        if self.server_socket:
            self.server_socket.close()
