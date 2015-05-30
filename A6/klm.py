#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys


class KlmCalculator:
    def __init__(self):
        # operator values of Card, Moran, Newell and Kieras
        CMNKOperators = {
            "k": 0.28,
            "p": 1.1,
            "b": 0.10,
            "h": 0.40,
            "m": 1.2
        }
        # own values
        ownOperators = {
            "k": 0.192991,
            "p": 0.928450,
            "b": 0.152912,
            "h": 0.304982,
            "m": 1.1
        }
        # set operators to object
        self.CMNKOperators = CMNKOperators
        self.ownOperators = ownOperators
        # split lines, extract important data and calculate
        self.splitLines()
        self.extractKlmShort()
        self.calculate()

    # split lines
    def splitLines(self):
        with open(sys.argv[1]) as f:
            lines = f.readlines()  # read lines and save

        # loop to get usable data
        for i in range(len(lines)):
            # remove new lines
            lines[i] = lines[i].replace("\n", "").lower()
            # add to object
            self.lines = lines

    # extract data to calculate
    def extractKlmShort(self):
        klmShort = []
        # loop to get the klm short and remove empty lines
        for l in self.lines:
            # split at # and remove whitespaces
            strippedLine = l.split("#", 1)[0].strip()
            # check if line is empty and append to array for calculation
            if (strippedLine != "" and strippedLine != "\n"):
                klmShort.append(strippedLine)
        # add to object
        self.klmShort = klmShort

    # calculate times
    def calculate(self):
        completionTimeCMNK = 0
        completionTimeOwn = 0
        multiplicator = ""

        # loops for calculation
        for k in self.klmShort:
            for i in range(len(k)):
                currentChar = k[i]
                # if char is digit then add number to multiplicator for later calculation
                if (currentChar.isdigit()):
                    multiplicator = str(multiplicator) + str(currentChar)
                # if currentchar is no digit then calculate the time and add them to the created vars
                else:
                    # set multiplicator to 1 if empty string for proper calculation
                    if (multiplicator == ""):
                        multiplicator = 1
                    # part time and complete time for Card, Moran, Newell and Kieras operator values
                    partTimeCMNK = int(multiplicator) * self.CMNKOperators[currentChar]
                    completionTimeCMNK = completionTimeCMNK + partTimeCMNK

                    # part time and complete time for own operator values
                    partTimeOwn = int(multiplicator) * self.ownOperators[currentChar]
                    completionTimeOwn = completionTimeOwn + partTimeOwn

                    # reset multiplicator to empty
                    multiplicator = ""
        # round completion times two decimals
        completionTimeCMNK = round(completionTimeCMNK, 2)
        completionTimeOwn = round(completionTimeOwn, 2)

        #print out results
        print("Time for complete task with Card, Moran, Newell and Kieras operator values: ")
        print(str(completionTimeCMNK))

        print("Time for complete task with own operator values: ")
        print(str(completionTimeOwn))


if __name__ == '__main__':
    calc = KlmCalculator()
