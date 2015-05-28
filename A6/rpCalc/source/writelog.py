#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import csv
import datetime
import os

class WriteLog:

    def keystroke(timeStamp, key):
        print ("key:" + key)
        print (timeStamp)
        print (timeStamp, key)
        WriteLog.writeInCSV(timeStamp, key, "K")
        #ölol

    def buttonpress(timeStamp, button):

        print ("button:" + button)
        print (timeStamp, button)
        WriteLog.writeInCSV(timeStamp, button, "B")

    def writeInCSV(timestamp, event, operator):
        CSVHEADER = ["timestamp", "event", "operator"]
        row = [timestamp, event, operator]

        if os.path.isfile("1.csv"):
            # convert list to string
            convertedRow = ','.join(map(str, row))
            participantFile = open("1.csv", 'a', newline="")  # open file in append mode
            participantFile.write(convertedRow)  # write row to csv
            participantFile.write('\r\n')  # write new line
        # if participant file not exists
        else:
            # create file
            with open("1.csv", 'w', newline="") as participantFile:
                participantFile.write('# Log created at ' + str(datetime.datetime.now()))  # created at row
                participantFile.write('\r\n')  # write new line

                write = csv.writer(participantFile, delimiter=',')  # create csv write on file
                data = [CSVHEADER, row]  # set data: header and row
                write.writerows(data)  # write rows

