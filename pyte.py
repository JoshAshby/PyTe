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

        newEditor = editor(self, self)
        newTab = self.mainTabWidget.addTab(newEditor, QtGui.QIcon(self.icons+'pyte.png'), "Pyte v3")
        self.mainTabWidget.setCurrentIndex(newTab)

        self.statusBar()

        closeTab = QtGui.QAction(QtGui.QIcon(self.icons+'exit.png'), 'Close Tab', self)
        closeTab.setStatusTip('Close Tab')
        self.connect(closeTab, QtCore.SIGNAL('triggered()'), self.closetab)

        newtab = QtGui.QAction(QtGui.QIcon(self.icons+'add.png'), 'Add Tab', self)
        newtab.setStatusTip('Add Tab')
        self.connect(newtab,QtCore.SIGNAL('triggered()'), self.codetab)

        self.connect(self.mainTabWidget, QtCore.SIGNAL("tabCloseRequested (int)"), self.on_close_tab_requested)
        self.connect(self.mainTabWidget, QtCore.SIGNAL("currentChanged (int)"), self.on_tab_change)

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(newtab)
        file.addAction(closeTab)

        #if there is a argument passed then try to open it as a file
        if (len(sys.argv) > 1):
            fn = sys.argv[1]

            fileName = str(fn)

            try:
                self.editor.openArg(fileName)
                self.editor.title(fileName)
            except:
                return

            self.setWindowTitle(fileName+" - PyTe v3")
        else:
            pass

    def closetab(self):
        self.mainTabWidget.removeTab(self.mainTabWidget.currentIndex())

    def codetab(self):
        newEditor = editor(self, self)
        newTab = self.mainTabWidget.addTab(newEditor, QtGui.QIcon(self.icons+'tex.png'), "Code Editor")
        self.mainTabWidget.setCurrentIndex(newTab)
        self.printChildren(self.mainTabWidget, "")

    def printChildren(self, obj, indent):
        children=obj.children()
        if children==None:
           return
        for child in children:
           if (child.__class__ == editor):
                if (child.getTitle() == ''):
                   self.setWindowTitle("PyTe v3")
                else:
                   self.setWindowTitle(child.getTitle()+" - PyTe v3")

    def on_close_tab_requested(self, tabIndex):
        self.mainTabWidget.removeTab(tabIndex)

    def on_tab_change(self, index):
        self.printChildren(self.mainTabWidget, "")

#start the app
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
