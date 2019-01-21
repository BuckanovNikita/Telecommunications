from PyQt5.QtWidgets import *


class IPWidget(QWidget):
    def __init__(self, text, parent=None):
        super(IPWidget, self).__init__(parent)
        self.setParent(parent)
        self.setLayout(QHBoxLayout())

        self.ip_val = [127, 0, 0, 1]
        self.port_val = 1270

        self.layout().addWidget(QLabel(text))

        self.ip_fields = [QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()]
        for i, t in enumerate(self.ip_fields):
            t.setText(str(self.ip_val[i]))
            self.layout().addWidget(t)

        self.layout().addWidget(QLabel(':'))

        self.port_field = QLineEdit()
        self.port_field.setText(str(self.port_val))
        self.layout().addWidget(self.port_field)

    def get_address(self):
        if self.port_field.text().isdigit() and 1024 < int(self.port_field.text()) < 100000:
            self.port_val = int(self.port_field.text())
        else:
            raise ValueError
        for i, t in enumerate(self.ip_fields):
            if t.text().isdigit() and int(i == 0) <= int(t.text()) <= 255:
                self.ip_val[i] = int(t.text())
            else:
                raise ValueError
        return str(self.ip_val[0])+'.'+str(self.ip_val[1])+'.'+str(self.ip_val[2])+'.'+str(self.ip_val[3]),\
            self.port_val
