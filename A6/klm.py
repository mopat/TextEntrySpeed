#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

class KlmCalculator:
    def __init__(self):
        klmOperators = {
        "k": 0.28,
        "p": 1.1,
        "b": 0.10,
        "h": 0.40,
        "m": 1.2
        }
        self.klmOperators = klmOperators
        self.splitLines()
        self.extractKlmShort()
        self.calculate()


    def splitLines(self):
        with open(sys.argv[1]) as f:
            lines = f.readlines()

        for i in range(len(lines)):
            lines[i] = lines[i].replace("\n", "").lower()
            self.lines = lines


    def extractKlmShort(self):
        klmShort = []
        for l in self.lines:
            strippedLine = l.split("#",1)[0].strip()
            if(strippedLine != "" and strippedLine != "\n"):
                klmShort.append(strippedLine)

        self.klmShort = klmShort

    def calculate(self):
        completionTime = 0
        multiplicator = 1

        for k in self.klmShort:
            for i in range(len(k)):
                currentChar = k[i]
                if(currentChar.isdigit()):
                    print(currentChar.isdigit())

                else:
                    completionTime += self.klmOperators[currentChar]
                    print(completionTime)



if __name__ == '__main__':
    calc = KlmCalculator()