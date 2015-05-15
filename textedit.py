# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import datetime
import re

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QLCDNumber, QSlider,
                             QVBoxLayout)


class TextEntry(QtWidgets.QTextEdit):
    def __init__(self, example_text, speed_widget):
        super(TextEntry, self).__init__()
        self.speed_widget = speed_widget
        self.numbers = []
        self.template_doc = ""
        self.setHtml(example_text)
        self.prev_content = ""
        self.generate_template()
        self.render_template()
        self.initUI()

        keyPressedTimestamps = []
        self.keyPressedTimestamps = keyPressedTimestamps
        # connect signal to slot
        self.textChanged.connect(self.on_text_changed)


    def initUI(self):
        self.setGeometry(0, 0, 400, 400)
        self.setWindowTitle('TextEntrySpeed')
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setMouseTracking(True)
        self.show()

    def on_text_changed(self):
        self.keyPressedTimestamps.append(datetime.datetime.now())
        self.start = self.keyPressedTimestamps[0]
        keyPressedArrayLength = len(self.keyPressedTimestamps)
        if (keyPressedArrayLength > 1):
            # complete speed
            self.end = self.keyPressedTimestamps[keyPressedArrayLength - 1]
            timeDifferenceComplete = self.end - self.start
            timeDifferenceCompleteInMs = timeDifferenceComplete.seconds * 1000 + timeDifferenceComplete.microseconds / 1000
            keystrokesPerSecondComplete =  len(self.keyPressedTimestamps) / (timeDifferenceCompleteInMs/1000)
            # cpm
            keystrokesPerMinuteComplete = keystrokesPerSecondComplete * 60
            # wpm
            wordsPerMinuteComplete = keystrokesPerMinuteComplete / 5


            # timeDifferenceCurrent = self.keyPressedTimestamps[keyPressedArrayLength - 1] - self.keyPressedTimestamps[
             #    keyPressedArrayLength - 2]
            # timeDifferenceInMsCurrent = timeDifferenceCurrent.seconds * 1000 + timeDifferenceCurrent.microseconds / 1000
            # keystrokesPerSecondCurrent = 1000 / timeDifferenceInMsCurrent
            # CPM
            # keystrokesPerMinuteCurrent = keystrokesPerSecondCurrent * 60
            # WPM
            # wordsPerMinuteCurrent = keystrokesPerMinuteCurrent / 5
            # print(wordsPerMinute)
            self.speed_widget.setValues(wordsPerMinuteComplete)

    def getCurrentValue(self, value):
        currentValue = value
        return currentValue

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
            content = re.sub(" " + str(numbers[num_id]), " <a href='%d'>$%d$</a>" % (num_id, num_id), content, count=1)
        self.template_doc = content


def main():
    app = QtWidgets.QApplication(sys.argv)
    speed_widget = SpeedWidget()
    text_entry = TextEntry("", speed_widget)

    sys.exit(app.exec_())


class SpeedWidget(QtWidgets.QWidget):
    def __init__(self):
        super(SpeedWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.lcd = QLCDNumber(self)
        vbox = QVBoxLayout()
        vbox.addWidget(self.lcd)
        self.setLayout(vbox)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Words per Minute')
        self.value = 0
        self.show()

    def setValues(self, complete):
        complete = int(complete)
        self.complete = complete
        self.lcd.display(self.complete)

if __name__ == '__main__':
    main()
