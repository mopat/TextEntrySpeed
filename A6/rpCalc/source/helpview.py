#!/usr/bin/env python3

#****************************************************************************
# helpview.py, provides a window for viewing an html help file
#
# Copyright (C) 2014, Douglas W. Bell
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License, either Version 2 or any later
# version.  This program is distributed in the hope that it will be useful,
# but WITTHOUT ANY WARRANTY.  See the included LICENSE file for details.
#*****************************************************************************

import os.path
import sys
import webbrowser
from PyQt5 import QtCore, QtGui, QtWidgets


class HelpView(QtWidgets.QMainWindow):
    """Main window for viewing an html help file.
    """
    def __init__(self, path, caption, icons, parent=None):
        """Helpview initialize with text.
        """
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_QuitOnClose, False)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setStatusBar(QtWidgets.QStatusBar())
        self.textView = HelpViewer(self)
        self.setCentralWidget(self.textView)
        path = os.path.abspath(path)
        if sys.platform.startswith('win'):
            path = path.replace('\\', '/')
        self.textView.setSearchPaths([os.path.dirname(path)])
        self.textView.setSource(QtCore.QUrl('file:///{0}'.format(path)))
        self.resize(520, 440)
        self.setWindowTitle(caption)
        tools = self.addToolBar('Tools')
        self.menu = QtWidgets.QMenu(self.textView)
        self.textView.highlighted[str].connect(self.showLink)

        backAct = QtGui.QAction('&Back', self)
        backAct.setIcon(icons['helpback'])
        tools.addAction(backAct)
        self.menu.addAction(backAct)
        backAct.triggered.connect(self.textView.backward)
        backAct.setEnabled(False)
        self.textView.backwardAvailable.connect(backAct.setEnabled)

        forwardAct = QtGui.QAction('&Forward', self)
        forwardAct.setIcon(icons['helpforward'])
        tools.addAction(forwardAct)
        self.menu.addAction(forwardAct)
        forwardAct.triggered.connect(self.textView.forward)
        forwardAct.setEnabled(False)
        self.textView.forwardAvailable.connect(forwardAct.setEnabled)

        homeAct = QtGui.QAction('&Home', self)
        homeAct.setIcon(icons['helphome'])
        tools.addAction(homeAct)
        self.menu.addAction(homeAct)
        homeAct.triggered.connect(self.textView.home)

        tools.addSeparator()
        tools.addSeparator()
        findLabel = QtWidgets.QLabel(' Find: ', self)
        tools.addWidget(findLabel)
        self.findEdit = QtWidgets.QLineEdit(self)
        tools.addWidget(self.findEdit)
        self.findEdit.textEdited.connect(self.findTextChanged)
        self.findEdit.returnPressed.connect(self.findNext)

        self.findPreviousAct = QtGui.QAction('Find &Previous', self)
        self.findPreviousAct.setIcon(icons['helpprevious'])
        tools.addAction(self.findPreviousAct)
        self.menu.addAction(self.findPreviousAct)
        self.findPreviousAct.triggered.connect(self.findPrevious)
        self.findPreviousAct.setEnabled(False)

        self.findNextAct = QtGui.QAction('Find &Next', self)
        self.findNextAct.setIcon(icons['helpnext'])
        tools.addAction(self.findNextAct)
        self.menu.addAction(self.findNextAct)
        self.findNextAct.triggered.connect(self.findNext)
        self.findNextAct.setEnabled(False)

    def showLink(self, text):
        """Send link text to the statusbar.
        """
        self.statusBar().showMessage(text)

    def findTextChanged(self, text):
        """Update find controls based on text in text edit.
        """
        self.findPreviousAct.setEnabled(len(text) > 0)
        self.findNextAct.setEnabled(len(text) > 0)

    def findPrevious(self):
        """Command to find the previous string.
        """
        if self.textView.find(self.findEdit.text(),
                              QtWidgets.QTextDocument.FindBackward):
            self.statusBar().clearMessage()
        else:
            self.statusBar().showMessage('Text string not found')

    def findNext(self):
        """Command to find the next string.
        """
        if self.textView.find(self.findEdit.text()):
            self.statusBar().clearMessage()
        else:
            self.statusBar().showMessage('Text string not found')


class HelpViewer(QtWidgets.QTextBrowser):
    """Shows an html help file.
    """
    def __init__(self, parent=None):
        QtWidgets.QTextBrowser.__init__(self, parent)

    def setSource(self, url):
        """Called when user clicks on a URL.
        """
        name = url.toString()
        if name.startswith('http'):
            webbrowser.open(name, True)
        else:
            QtWidgets.QTextBrowser.setSource(self, QtCore.QUrl(name))

    def contextMenuEvent(self, event):
        """Init popup menu on right click"".
        """
        self.parentWidget().menu.exec_(event.globalPos())
