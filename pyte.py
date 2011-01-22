#!/usr/bin/python
#====================About===========================
#PyTe v3
#Joshua Ashby
#http://joshashby.com
#joshuaashby@joshashby.com
#2011
#By Using PyTe you agree to the Python, and Qt License's
#All Trademarks Subject to their owners
#Licensed under the Creative Commons v3 Non-Commercial License
#===================================================
#Ver .01 Alpha
#===================================================
import sys, os
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui, Qsci
from PyQt4.Qsci import QsciScintilla, QsciScintillaBase, QsciLexerPython
from editor import editor

debug = 0

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.__Dir = os.path.dirname(sys.argv[0])
        self.icons =  os.path.join(self.__Dir, 'icons/')

        self.resize(640, 480)
        self.setWindowTitle('PyTe v3')
        self.setWindowIcon(QtGui.QIcon(self.icons+'pyte.png'))


        self.mainTabWidget = QtGui.QTabWidget(self)
        self.mainTabWidget.setTabsClosable(True)
        self.mainTabWidget.setMovable(True)
        self.setCentralWidget(self.mainTabWidget)

        self.codetab()

        self.statusBar()

        closeTab = QtGui.QAction(QtGui.QIcon(self.icons+'exit.png'), 'Close Tab', self)
        closeTab.setStatusTip('Close Tab')
        self.connect(closeTab, QtCore.SIGNAL('triggered()'), self.closetab)

        newtab = QtGui.QAction(QtGui.QIcon(self.icons+'add.png'), 'Add Tab', self)
        newtab.setStatusTip('Add Tab')
        self.connect(newtab,QtCore.SIGNAL('triggered()'), self.codetab)

        self.connect(self.mainTabWidget, QtCore.SIGNAL("tabCloseRequested (int)"), self.tabClose)
        self.connect(self.mainTabWidget, QtCore.SIGNAL("currentChanged (int)"), self.tabChange)

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(newtab)
        file.addAction(closeTab)

        timer = QtCore.QTimer(self)
        QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), self.tabUpdate)
        timer.start(1000)

    def closetab(self):
        self.mainTabWidget.removeTab(self.mainTabWidget.currentIndex())
        self.getObject(self.mainTabWidget, "")

    def codetab(self):
        newEditor = editor(self, self)
        newTab = self.mainTabWidget.addTab(newEditor, QtGui.QIcon(self.icons+'tex.png'), "Code Editor")
        self.mainTabWidget.setCurrentIndex(newTab)
        self.getObject(self.mainTabWidget, "")

    def tabClose(self, tabIndex):
        self.mainTabWidget.removeTab(tabIndex)
        self.getObject(self.mainTabWidget, "")

    def tabChange(self, index):
        self.getObject(self.mainTabWidget, "")

    def tabUpdate(self):
        self.getObject(self.mainTabWidget, "")
        if debug==1:
           print self.windowTitle()

    def getObject(self, obj, indent):
        children=obj.children()
        if children==None:
           return
        for child in children:
           if (child.__class__ == editor):
                if debug==1:
                   print child
                if (child.getTitle() == ''):
                   self.setWindowTitle("PyTe v3")
                else:
                   self.setWindowTitle(child.getTitle()+" - PyTe v3")
           else:
                self.getObject(child, indent + "  ")

#start the app
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
