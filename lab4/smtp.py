import smtplib as smtp
import sys
from PyQt5.QtWidgets import *
from login_password import login, password

def send():
    server = None
    try:
        message = 'From: {}\nTo: {}\nSubject: {}\n\n{}\n.'.format(email,
                                                                  destination_field.text(),
                                                                  subject_field.text(),
                                                                  mail_field.toPlainText())
        server = smtp.SMTP_SSL('smtp.yandex.com')
        server.set_debuglevel(1)
        server.ehlo(email)
        server.login(email, password)
        server.auth_plain()
        server.sendmail(email, destination_field.text(), message)
        server.quit()
        mail_field.clear()
        subject_field.clear()
    except:
        if server:
            server.quit()

if __name__ == '__main__':
    email = login
    dest_email = 'buckanov32@gmail.com'

    try:
        app = QApplication(sys.argv)
        main_window = QWidget()
        main_window.setWindowTitle('lab 4 task 2')
        main_window.setLayout(QVBoxLayout())

        destination_field = QLineEdit()
        destination_field.setText('buckanov32@gmail.com')
        subject_field = QLineEdit()
        mail_field = QTextEdit()

        start_btn = QPushButton("Send mail")
        start_btn.clicked.connect(send)

        main_window.layout().addWidget(QLabel("Destination email:"))
        main_window.layout().addWidget(destination_field)
        main_window.layout().addWidget(QLabel("Subject"))
        main_window.layout().addWidget(subject_field)
        main_window.layout().addWidget(QLabel("Message"))
        main_window.layout().addWidget(mail_field)
        main_window.layout().addWidget(start_btn)
        main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
