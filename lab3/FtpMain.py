import sys
from PyQt5.QtWidgets import *
from FtpWrapper import FtpWrapper

pool = []


def control():
    for t in pool:
        if t.isFinished():
            pool.remove(t)
    try:
        ftp = FtpWrapper(ftp_field.text(), request_field.text(), QFileDialog().getExistingDirectory())
        w = QWidget()
        w.setLayout(QHBoxLayout())
        w.layout().addWidget(QLabel(ftp.server_name + '/' + ftp.file_name + ':'))
        p = QProgressBar()
        w.layout().addWidget(p)
        main_window.layout().addWidget(w)
        ftp.progress.connect(p.setValue)
        ftp.bad.connect(lambda x: status_list.addItem(QListWidgetItem(x)))
        ftp.end.connect(w.close)
        pool.append(ftp)
    except:
        return


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        main_window = QWidget()
        main_window.setWindowTitle('lab 3 task 4')
        main_window.setLayout(QVBoxLayout())

        ftp_field = QLineEdit()
        ftp_field.setText('speedtest.tele2.net')

        request_field = QLineEdit()
        request_field.setText("50MB.zip")

        start_btn = QPushButton("Send Request")

        status_list = QListWidget()

        start_btn.clicked.connect(lambda x: [control(), pool[-1].start()])

        main_window.layout().addWidget(QLabel("Request:"))
        main_window.layout().addWidget(request_field)
        main_window.layout().addWidget(ftp_field)
        main_window.layout().addWidget(start_btn)
        main_window.layout().addWidget(status_list)
        main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
