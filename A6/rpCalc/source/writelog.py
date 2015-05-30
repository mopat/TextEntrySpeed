#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import csv
import os
from datetime import datetime

class WriteLog:



    def keystroke(timeStamp, key):
        fileName = WriteLog.fileName(WriteLog)
        WriteLog.writeInCSV(timeStamp, key, "K", fileName)
        row = [timeStamp, key, "K"]
        sys.stdout.write('\n')

    def buttonpress(timeStamp, button):
        fileName = WriteLog.fileName(WriteLog)
        WriteLog.writeInCSV(timeStamp, button, "C", fileName)
        row = [timeStamp, button, "C"]
        sys.stdout.write(str(row))
        sys.stdout.write('\n')

    def fileName(self):
        fileName = {
            "1": "keystroketime(K)",
            "2": "buttonclicktime(B)",
            "3": "pointingtime(P)",
            "4": "deviceswitching(H)"
        }
        if(len(sys.argv) > 1):
            return fileName[str(sys.argv[1])]
        else:
            return "log"

    def writeInCSV(timestamp, event, operator, fileName):
        CSVHEADER = ["timestamp", "eventtext", "operator"]
        row = [timestamp, event, operator]
        csvFileName = fileName + ".csv"
        if os.path.isfile(csvFileName):
            # convert list to string
            convertedRow = ','.join(map(str, row))
            participantFile = open(csvFileName, 'a', newline="")  # open file in append mode
            participantFile.write(convertedRow)  # write row to csv
            participantFile.write('\r\n')  # write new line
            row = []
        # if participant file not exists
        else:
            # create file
            with open(csvFileName, 'w', newline="") as participantFile:
                #participantFile.write('# Log created at ' + str(datetime.now()))  # created at row
                #participantFile.write('\r\n')  # write new line

                write = csv.writer(participantFile, delimiter=',')  # create csv write on file
                data = [CSVHEADER, row]  # set data: header and row
                write.writerows(data)  # write rows
                row = []
