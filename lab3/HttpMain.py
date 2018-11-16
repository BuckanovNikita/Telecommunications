import sys
from PyQt5.QtWidgets import *
from HttpWrapper import HttpWrapper


def control():
    http_wrapper.set_text(request_field.text())
    http_wrapper.start()


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        main_window = QWidget()
        main_window.setWindowTitle('lab 3 task 4')
        main_window.setLayout(QVBoxLayout())

        request_field = QLineEdit()
        request_field.setText("https://stackoverflow.com/questions/22571259/split-a-string-into-n-equal-parts")

        start_btn = QPushButton("Send Request")
        start_btn.clicked.connect(lambda x: control())

        requests_list = QPlainTextEdit()

        progress_bar = QProgressBar()

        http_wrapper = HttpWrapper('')
        http_wrapper.progress.connect(progress_bar.setValue)
        http_wrapper.bad.connect(request_field.setText)
        http_wrapper.end.connect(requests_list.setPlainText)

        main_window.layout().addWidget(QLabel("File path"))
        main_window.layout().addWidget(request_field)
        main_window.layout().addWidget(start_btn)
        main_window.layout().addWidget(requests_list)
        main_window.layout().addWidget(progress_bar)
        main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
