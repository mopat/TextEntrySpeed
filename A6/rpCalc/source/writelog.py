#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import csv
import datetime

class WriteLog:

    def __init__(self):
        print ("create csv")


    def keystroke(self, timeStamp, key):
        print ("key:" + key)
        print (timeStamp)
        #ölol

    def buttonpress(self, timeStamp, button):

        print ("button:" + button)
        print (timeStamp)

if __name__ == '__main__':
    log = WriteLog()
