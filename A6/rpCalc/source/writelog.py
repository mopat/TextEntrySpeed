#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import csv
import datetime

class WriteLog:

    def __init__(self):
        print ("create csv")
        keyStrokeTimestamps = []
        self.keyStrokeTimestamps = keyStrokeTimestamps


    def keystroke(self, oldTimestamp, timeStamp, key):
        print ("key:" + key)
        tNew = timeStamp
        tOld = oldTimestamp
        d = tNew - tOld
        print (d)

    def buttonpress(button):
        print ("button:" + button)

if __name__ == '__main__':
    log = WriteLog()
