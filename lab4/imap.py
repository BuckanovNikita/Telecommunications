import imaplib
from ImapWrapper import ImapWrapper, ImapSelector
from login_password import login, password
import base64
import sys
from PyQt5.QtWidgets import *


def imaputf7encode(s):
    s=s.replace('&','&-')
    iters=iter(s)
    unipart=out=''
    for c in s:
        if 0x20<=ord(c)<=0x7f :
            if unipart!='' :
                out+='&'+base64.b64encode(unipart.encode('utf-16-be')).decode('ascii').rstrip('=')+'-'
                unipart=''
            out+=c
        else : unipart+=c
    if unipart!='' :
        out+='&'+base64.b64encode(unipart.encode('utf-16-be')).decode('ascii').rstrip('=')+'-'
    return out


class MailWidget(QWidget):

    def __init__(self, msg, parent=None):
        super(MailWidget, self).__init__(parent)
        layout = QVBoxLayout()
        self.msg = msg
        self.name = "From: " + msg['From'].split(' ')[-1].lstrip('<').rstrip('>')
        self.name += "\nTo: "
        self.name += msg['To'].split(' ')[-1].lstrip('<').rstrip('>')
        self.name += "\nDate:" + msg['Date']
        btn = QPushButton(self.name)
        layout.addWidget(btn)
        btn.clicked.connect(self.full)
        self.setLayout(layout)

    def full(self):
        mail_edit.clear()
        for part in self.msg.walk():
            if part.get_content_type() == 'text/html':
               mail_edit.append(part.get_payload(None,True).decode())
            if part.get_content_type() == 'text/plain':
                mail_edit.append(part.get_payload())


def message_constructor(msg):
    item = QListWidgetItem(mail_list)
    item_widget = MailWidget(msg)
    item.setSizeHint(item_widget.sizeHint())
    mail_list.addItem(item)
    mail_list.setItemWidget(item, item_widget)


class FolderWidget(QWidget):
    def __init__(self, name, parent=None):
        super(FolderWidget, self).__init__(parent)
        self.name = ""
        for t in name:
            self.name += (t+"|")
        self.name = self.name[:-1]
        layout = QVBoxLayout()
        str_name = ''
        for t in name:
            str_name += ('/' + ImapWrapper.imaputf7decode(t))
        btn = QPushButton(str_name[1:])
        layout.addWidget(btn)
        self.s = None
        btn.clicked.connect(lambda x: [self.select(), self.s.start()])
        self.setLayout(layout)

    def select(self):
        mail_list.clear()
        self.s = ImapSelector(imap, self.name)
        self.s.message.connect(message_constructor)


imap = None
imap_thread = None


def create_folders(name_list):
    for t in name_list:
        item = QListWidgetItem(folder_list)
        item_widget = FolderWidget(t)
        item.setSizeHint(item_widget.sizeHint())
        folder_list.addItem(item)
        folder_list.setItemWidget(item, item_widget)


def get():
    global imap
    global imap_thread
    imap = imaplib.IMAP4_SSL(mail_server.text())
    imap.login(login, password)
    imap_thread = ImapWrapper(imap)
    imap_thread.folders.connect(lambda x: create_folders(x))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_window = QWidget()
    main_window.setWindowTitle('lab 4 task 2')
    main_window.setLayout(QVBoxLayout())

    mail_server = QLineEdit()
    mail_server.setText('imap.yandex.ru')
    subject_field = QLineEdit()
    folder_list = QListWidget()
    mail_list = QListWidget()
    mail_edit = QTextEdit()

    start_btn = QPushButton("Check")
    start_btn.clicked.connect(lambda t: [get(), imap_thread.start()])

    main_window.layout().addWidget(QLabel("Destination email:"))
    main_window.layout().addWidget(mail_server)
    main_window.layout().addWidget(start_btn)
    main_window.layout().addWidget(QLabel("Message"))
    main_window.layout().addWidget(folder_list)
    main_window.layout().addWidget(mail_list)
    main_window.layout().addWidget(mail_edit)
    main_window.show()
    sys.exit(app.exec_())