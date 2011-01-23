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
#Ver .5 Alpha
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

        self.resize(800, 800)
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

        openTab = QtGui.QAction(QtGui.QIcon(self.icons+'open.png'), 'Open', self)
        openTab.setStatusTip('Open')
        self.connect(openTab,QtCore.SIGNAL('triggered()'), self.open)

        saveTab = QtGui.QAction(QtGui.QIcon(self.icons+'save.png'), 'Save', self)
        saveTab.setStatusTip('save')
        self.connect(saveTab,QtCore.SIGNAL('triggered()'), self.save)

        saveAsTab = QtGui.QAction(QtGui.QIcon(self.icons+'save.png'), 'Save As', self)
        saveAsTab.setStatusTip('Save As')
        self.connect(saveAsTab,QtCore.SIGNAL('triggered()'), self.saveAs)

        self.connect(self.mainTabWidget, QtCore.SIGNAL("tabCloseRequested (int)"), self.tabClose)
        self.connect(self.mainTabWidget, QtCore.SIGNAL("currentChanged (int)"), self.tabChange)

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(newtab)
        file.addAction(openTab)
        file.addAction(saveTab)
        file.addAction(saveAsTab)
        file.addAction(closeTab)

        toolbar = self.addToolBar('File')
        toolbar.addAction(newtab)
        toolbar.addAction(closeTab)
        toolbar.addSeparator()
        toolbar.addAction(openTab)
        toolbar.addAction(saveTab)
        toolbar.addAction(saveAsTab)

        timer = QtCore.QTimer(self)
        QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), self.tabUpdate)
        timer.start(1000)

    def codetab(self):
        newEditor = editor(self, self)
        newTab = self.mainTabWidget.addTab(newEditor, QtGui.QIcon(self.icons+'pyte.png'), "Code Editor")
        self.mainTabWidget.setCurrentIndex(newTab)
        self.getTitle(self.mainTabWidget, "")

    def tabClose(self, tabIndex):
        self.mainTabWidget.removeTab(tabIndex)
        self.getTitle(self.mainTabWidget, "")
    def closetab(self):
        self.mainTabWidget.removeTab(self.mainTabWidget.currentIndex())
        self.getTitle(self.mainTabWidget, "")

    def tabChange(self, index):
        self.getTitle(self.mainTabWidget, "")
    def tabUpdate(self):
        self.getTitle(self.mainTabWidget, "")
        if debug==1:
           print self.windowTitle()

    def getTitle(self, obj, indent):
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
                self.getTitle(child, indent + "  ")

    def open(self):
        self.Tabfile(self.mainTabWidget, "", 'openFile')

    def save(self):
        self.Tabfile(self.mainTabWidget, "", 'saveFile')

    def saveAs(self):
        self.Tabfile(self.mainTabWidget, "", 'saveAsFile')

    def Tabfile(self, obj, indent, action_type):
        children=obj.children()
        if children==None:
           return
        for child in children:
           if (child.__class__ == editor):
                if debug==1:
                   print child
                if (action_type == 'openFile'):
                   child.openFile()
                elif (action_type == 'saveFile'):
                   child.save()
                elif (action_type == 'saveAsFile'):
                   child.saveAs()
           else:
                if (action_type == 'openFile'):
                   self.Tabfile(child, indent + "  ", 'openFile')
                elif (action_type == 'saveFile'):
                   self.Tabfile(child, indent + "  ", 'saveFile')
                elif (action_type == 'saveAsFile'):
                   self.Tabfile(child, indent + "  ", 'saveAsFile')

#start the app
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
