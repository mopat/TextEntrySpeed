#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys


class WriteLog:
    def __init__(self):
        print ("create csv")

    def keystroke(key):
        print ("key:" + key)

    def buttonpress(button):
        print ("button:" + button)



if __name__ == '__main__':
    log = WriteLog()
