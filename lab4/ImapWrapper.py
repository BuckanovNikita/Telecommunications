from PyQt5.QtCore import *
import base64
import email


class ImapWrapper(QThread):

    folders = pyqtSignal(['PyQt_PyObject'])

    def __init__(self, imap):
        super(ImapWrapper, self).__init__()
        self.imap = imap

    def __del__(self):
        self.wait()

    def run(self):
        name = []
        for t in self.imap.list()[1]:
            name.append([q.replace("\"", "").strip() for q in t.decode().split("|")][1:])
        self.folders.emit(name)

    @staticmethod
    def b64padanddecode(b):
        b += (-len(b) % 4) * '='
        return base64.b64decode(b, altchars='+,', validate=True).decode('utf-16-be')

    @staticmethod
    def imaputf7decode(s):
        lst = s.split('&')
        out = lst[0]
        for e in lst[1:]:
            u, a = e.split('-', 1)
            if u == '':
                out += '&'
            else:
                out += ImapWrapper.b64padanddecode(u)
            out += a
        return out

class ImapSelector(QThread):
    message = pyqtSignal(['PyQt_PyObject'])

    def __init__(self, imap, name):
        super(ImapSelector, self).__init__()
        self.imap = imap
        self.dir_name = name

    def __del__(self):
        self.wait()

    def run(self):
        self.imap.select(self.dir_name)
        for num in self.imap.search(None, 'ALL')[1][0].decode().split(" "):
            if num:
                status, data = self.imap.fetch(num.encode(), '(RFC822)')
                msg = email.message_from_bytes(data[0][1])
                self.message.emit(msg)