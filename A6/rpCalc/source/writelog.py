#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import csv
import os
from datetime import datetime

# class to write log to stdout and csv if needed
class WriteLog(object):
    # log data to stdout and/or csv file
    # "C
    # k" is for keystroke
    def keystroke(self, timeStamp, key):
        # set file name
        fileName = WriteLog.fileName(WriteLog)
        # check if filename exists
        if (fileName != None):
            WriteLog.writeInCSV(self, timeStamp, key, "K", fileName)
        # log data to stdout
        log = str(timeStamp) + ", " + key + ", " + "C"
        sys.stdout.write(log)
        sys.stdout.write('\n')

    # log data to stdout and/or csv file
    # "C" is for click
    def buttonpress(self, timeStamp, button):
        # set file name
        fileName = WriteLog.fileName(WriteLog)
        # check if filename exists
        if (fileName != None):
            WriteLog.writeInCSV(self, timeStamp, button, "C", fileName)
        # log data to stdout
        log = str(timeStamp) + ", " + button + ", " + "C"
        sys.stdout.write(log)
        sys.stdout.write('\n')

    # set csv filename when paramater exists
    def fileName(self):
        # different file names to know which task has been conducted
        fileName = {
            "1": "keystroketime(K)",
            "2": "buttonclicktime(B)",
            "3": "pointingtime(P)",
            "4": "deviceswitching(H)"
        }
        if (len(sys.argv) > 1 and str(sys.argv[1]) in fileName.values()):
            return fileName[str(sys.argv[1])]  # return file name when paramater exists
        elif (len(sys.argv) > 1):
            return str(sys.argv[1])  # create own filename
        else:
            return None  # return None

    # write csv log file
    def writeInCSV(self, timestamp, event, operator, fileName):
        CSVHEADER = ["timestamp", "eventtext", "operator"]  # csv header
        row = [timestamp, event, operator]  # row to save in file
        csvFileName = fileName + ".csv"  # create full file name
        if os.path.isfile(csvFileName):
            # convert list to string
            convertedRow = ','.join(map(str, row))
            participantFile = open(csvFileName, 'a', newline="")  # open file in append mode
            participantFile.write(convertedRow)  # write row to csv
            participantFile.write('\r\n')  # write new line
        # if participant file not exists
        else:
            # create file
            with open(csvFileName, 'w', newline="") as participantFile:
                #participantFile.write('# Log created at ' + str(datetime.now()))  # created at row
                #participantFile.write('\r\n')  # write new line

                write = csv.writer(participantFile, delimiter=',')  # create csv write on file
                data = [CSVHEADER, row]  # set data: header and row
                write.writerows(data)  # write rows
