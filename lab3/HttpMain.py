import sys
from PyQt5.QtWidgets import *
from HttpWrapper import HttpWrapper


def control():
    http_wrapper.setText(request_field.text())
    http_wrapper.start()

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        main_window = QWidget()
        main_window.setWindowTitle('lab 3 task 4')
        main_window.setLayout(QVBoxLayout())

        main_window.layout().addWidget(QLabel("File path"))
        request_field = QLineEdit()
        request_field.setText("https://stackoverflow.com/questions/22571259/split-a-string-into-n-equal-parts")
        main_window.layout().addWidget(request_field)

        start_btn = QPushButton("Send Request")

        main_window.layout().addWidget(start_btn)

        requests_list = QPlainTextEdit()
        main_window.layout().addWidget(requests_list)

        progress_bar = QProgressBar()
        main_window.layout().addWidget(progress_bar)

        main_window.show()
        http_wrapper = HttpWrapper('')
        http_wrapper.progress.connect(progress_bar.setValue)
        http_wrapper.bad.connect(request_field.setText)
        http_wrapper.end.connect(requests_list.setPlainText)
        start_btn.clicked.connect(lambda x: control())
        sys.exit(app.exec_())
    except Exception as e:
        print(e)