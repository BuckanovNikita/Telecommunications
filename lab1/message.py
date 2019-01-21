import datetime


class Message:
    def __init__(self, sender_ip, receiver_ip, text, info=False, encrypted=False, crypto_key=""):
        self.sender_ip = sender_ip
        self.receiver_ip = receiver_ip
        self.info = info
        self.encrypted = encrypted
        self.crypto_key = crypto_key
        self.send_time = datetime.datetime.now()
        self.text = text

    def __str__(self):
        return "Send from: " + str(self.sender_ip[0]) + ":" + str(self.sender_ip[1]) + "\n" + \
               "Send to: " + str(self.receiver_ip[0]) + ":" + str(self.receiver_ip[1]) + "\n" +\
               str(self.send_time)+"\n" + self.text
