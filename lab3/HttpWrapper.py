from PyQt5.QtCore import *
import requests


class HttpWrapper(QThread):
    progress = pyqtSignal(['int'])
    end = pyqtSignal(['PyQt_PyObject'])
    bad = pyqtSignal(['PyQt_PyObject'])

    def __init__(self, text):
        super(HttpWrapper, self).__init__()
        self.text = text

    def __del__(self):
        self.wait()

    def set_text(self, text):
        self.text = text

    def run(self):
        try:
            self.progress.emit(0)
            result = b''
            try:
                response = requests.get(self.text, stream=True)
            except:
                self.bad.emit('')
                return
            total_length = response.headers.get('content-length')
            if total_length is None:
                result = response.content
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    result += data
                    done = int(50 * dl / total_length)
                    self.progress.emit(done)
            self.end.emit(result.decode('utf-8'))
            self.progress.emit(100)
        except Exception as e:
            print(e)
