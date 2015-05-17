# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import datetime
import re
import os
import csv

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
        # count log rows
        self.logCounter = 0
        # array to save the pressed keys timestamps
        keyPressedTimestamps = []
        self.keyPressedTimestamps = keyPressedTimestamps
        self.keyPressedTimestamps.append(datetime.datetime.now())
        # array for all wpms
        allWPMs = []
        self.allWPMs = allWPMs
        # array for all CPMs
        allCPMs = []
        self.allCPMs = allCPMs
        # connect signal to slot
        self.textChanged.connect(self.onTextChanged)
        # header and row for csv array
        self.CSV_HEADER = []
        self.row = []

    def initUI(self):
        self.setGeometry(0, 0, 400, 400)
        self.setWindowTitle('TextEntrySpeedTest')
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setMouseTracking(True)
        self.show()

    # slot for text changed signal
    def onTextChanged(self):
        self.keyPressedTimestamps.append(datetime.datetime.now())
        self.start = self.keyPressedTimestamps[0]
        keyPressedArrayLength = len(self.keyPressedTimestamps)
        # prevent outliers
        if (keyPressedArrayLength > 0):
            # complete speed
            self.end = self.keyPressedTimestamps[keyPressedArrayLength - 1]
            timeDifferenceComplete = self.end - self.start
            self.totalTime = timeDifferenceComplete
            timeDifferenceCompleteInMs = timeDifferenceComplete.seconds * 1000 + timeDifferenceComplete.microseconds / 1000
            keystrokesPerSecondComplete = len(self.keyPressedTimestamps) / (timeDifferenceCompleteInMs/1000)
            # cpm
            keystrokesPerMinuteComplete = keystrokesPerSecondComplete * 60
            # append current cpm to allCPMs
            self.allCPMs.append(keystrokesPerMinuteComplete)
            # wpm
            wordsPerMinuteComplete = keystrokesPerMinuteComplete / 5
            # append current wpm to allWPMs
            self.allWPMs.append(wordsPerMinuteComplete)
            # the time difference between the last two keypresses
            timeDifferenceLastTwoKeyPresses = self.keyPressedTimestamps[keyPressedArrayLength - 1] - self.keyPressedTimestamps[keyPressedArrayLength - 2]
            timeDifferenceLastTwoKeyPressesInMS = timeDifferenceLastTwoKeyPresses.seconds * 1000 + timeDifferenceLastTwoKeyPresses.microseconds / 1000

            self.logCounter = self.logCounter + 1
            self.writeLog(keystrokesPerMinuteComplete, wordsPerMinuteComplete, timeDifferenceLastTwoKeyPressesInMS)
            self.speed_widget.setValues(wordsPerMinuteComplete)

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

    def writeLog(self, cpm, wpm, timeDifferenceLastTwoKeyPresses):
        participantNumber = 1
        participantFileName = 'participant' + str(participantNumber) + '.csv'
        # log text
        self.CSV_HEADER.append('registered_text')
        self.row.append(str(self.toPlainText()).replace("\n", "").replace("\t", "").replace("\r", ""))  # replace new line, tabs and new rows from csv row
        # log pressed key
        pressedKey = str(self.toPlainText())[len(self.toPlainText()) - 1].replace("\n", "").replace("\t", "").replace("\r", "")  # replace new line, tabs and new rows from csv row
        self.CSV_HEADER.append('pressed_key')
        self.row.append(pressedKey)
        # log timestamps
        self.CSV_HEADER.append('timestamp')
        self.row.append(self.keyPressedTimestamps[self.logCounter - 1])
        # log total time
        self.CSV_HEADER.append('total_time')
        self.row.append(self.totalTime)
        # log time difference between last two key presses
        self.CSV_HEADER.append('time_difference')
        self.row.append(timeDifferenceLastTwoKeyPresses)
        # log wpm
        self.CSV_HEADER.append('wpm')
        self.row.append(wpm)
        # log average wpm
        averageWPM = sum(self.allWPMs) / float(len(self.allWPMs))
        self.CSV_HEADER.append('average_wpm')
        self.row.append(averageWPM)
        # log cpm
        self.CSV_HEADER.append('cpm')
        self.row.append(cpm)
        # log average wpm
        averageCPM = sum(self.allCPMs) / float(len(self.allCPMs))
        self.CSV_HEADER.append('average_wpm')
        self.row.append(averageCPM)
        # log number of pressed characters
        self.CSV_HEADER.append('num_chars')
        self.row.append(self.logCounter)

        if os.path.isfile(participantFileName):
            # convert list to string
            convertedRow = ','.join(map(str, self.row))
            participantFile = open(participantFileName, 'a', newline="")  # open file in append mode
            participantFile.write(convertedRow)  # write row to csv
            participantFile.write('\r\n')  # write new line
            participantFile.close()  # close file
        # if participant file not exists
        else:
            # create file
            with open(participantFileName, 'w', newline="") as participantFile:
                participantFile.write('# Log created at ' + str(datetime.datetime.now()))  # created at row
                participantFile.write('\r\n')  # write new line

                write = csv.writer(participantFile, delimiter=',')  # create csv write on file
                data = [self.CSV_HEADER, self.row]  # set data: header and row
                write.writerows(data)  # write rows
        self.CSV_HEADER = []  # reset CSV header
        self.row = []  # reset row


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
        self.setWindowTitle('WordspPerMinute')
        self.value = 0
        self.show()

    # set lcd display value
    def setValues(self, wpm):
        complete = int(wpm)
        self.lcd.display(complete)

if __name__ == '__main__':
    main()
