
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal
import datetime
import re

class SuperText(QtWidgets.QTextEdit):

    def __init__(self, example_text):
        super(SuperText, self).__init__()
        self.numbers=[]
        self.template_doc = ""
        self.setHtml(example_text)
        self.prev_content = ""
        self.generate_template()
        self.render_template()
        self.initUI()

        keyPressedTimestamps = []
        self.keyPressedTimestamps = keyPressedTimestamps
        self.keyPressedTimestamps.append(datetime.datetime.now())
        # connect signal to slot
        self.textChanged.connect(self.on_text_changed)


    def initUI(self):
        self.setGeometry(0, 0, 400, 400)
        self.setWindowTitle('TextEntrySpeed')
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setMouseTracking(True)
        self.show()

    def timestamp(self):
        return QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.ISODate)

    def on_text_changed(self):
        # Number_of_keystroke / time_in_second * 60 * percentages_of_accurate_word
        self.keyPressedTimestamps.append(datetime.datetime.now())
        keyPressedArrayLength = len(self.keyPressedTimestamps)
        timeDifference = self.keyPressedTimestamps[keyPressedArrayLength-1] - self.keyPressedTimestamps[keyPressedArrayLength-2]
        timeDifferenceInMs = timeDifference.seconds*1000 + timeDifference.microseconds/1000
        print(timeDifferenceInMs)

    def change_value(self, val_id, amount):
        self.numbers[int(str(val_id))] += amount / 120
        self.render_template()

    def render_template(self):
        cur = self.textCursor()
        doc = self.template_doc
        for num_id, num in enumerate(self.numbers):
            doc = doc.replace('$' + str(num_id) + '$', '%d' % (num))
        self.setHtml(doc)
        self.setTextCursor(cur)

    def generate_template(self):
        content = str(self.toPlainText())
        numbers = list(re.finditer(" -?[0-9]+", content))
        numbers = [int(n.group()) for n in numbers]
        self.numbers = numbers
        if len(numbers) == 0:
            self.template_doc = content
            return
        for num_id in range(len(numbers)):
            content = re.sub(" " + str(numbers[num_id])  , " <a href='%d'>$%d$</a>" % (num_id, num_id), content, count=1)
        self.template_doc = content

def main():
    app = QtWidgets.QApplication(sys.argv)
    super_text = SuperText("")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
