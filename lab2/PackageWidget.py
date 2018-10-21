from PyQt5.QtWidgets import *


class PackageWidget(QWidget):
    def __init__(self, package, parent=None):
        super(PackageWidget, self).__init__(parent)

        w = QWidget(self)
        w.setLayout(QHBoxLayout())
        label = QLabel("RAW:" + package.raw_str)
        label1 = QLabel("UTF:" + package.ascii_str)
        w.layout().addWidget(label)
        w.layout().addWidget(label1)

        layout = QVBoxLayout()
        layout.addWidget(w)
        label3 = QLabel(str(package))
        layout.addWidget(label3)
        self.setLayout(layout)
