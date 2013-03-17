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
import sys, os
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui
from editor import editor

debug = 0
version = "3 RC"

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.__Dir = os.path.dirname(sys.argv[0])
        self.icons =  os.path.join(self.__Dir, 'icons/')

        self.resize(800, 600)
        self.setWindowTitle('PyTe v3')
        self.setWindowIcon(QtGui.QIcon(self.icons+'pyte.png'))

        self.lexerPic = {'.py': 'python.png', '.json': 'javascript.png', '.c': 'c.png', '.rb': 'ruby.png', '.sh': 'bash.png', ' ': 'unknown.png', '.sql': 'sql.png', '.cpp': 'cpp.png', '.h': 'h.png', '.pl': 'perl.png','.html': 'html.png','.css': 'css.png','.js': 'javascript.png', '.coffee': 'javascript.png','.lua': 'lua.png','.tex': 'tex.png', '.cfg': 'text.png', '.php': 'php.png', '.txt': 'text.png', '.xml': 'html.png'}

        self.mainTabWidget = QtGui.QTabWidget(self)
        self.mainTabWidget.setTabsClosable(True)
        self.mainTabWidget.setMovable(True)
        self.setCentralWidget(self.mainTabWidget)

        self.codetab()

        self.statusBar()

        closeTab = QtGui.QAction(QtGui.QIcon(self.icons+'exit.png'), 'Close Tab', self)
        closeTab.setStatusTip('Close Tab')
        closeTab.setWhatsThis("Close Tab: Closes the current tab.")
        closeTab.setShortcut('CTRL+X')
        self.connect(closeTab, QtCore.SIGNAL('triggered()'), self.closetab)

        quit = QtGui.QAction(QtGui.QIcon(self.icons+'exit.png'), 'Exit', self)
        quit.setShortcut('Ctrl+Q')
        quit.setStatusTip('Exit')
        self.connect(quit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        newtab = QtGui.QAction(QtGui.QIcon(self.icons+'add.png'), 'Add Tab', self)
        newtab.setStatusTip('Add Code Tab')
        newtab.setShortcut('CTRL+Z')
        self.connect(newtab,QtCore.SIGNAL('triggered()'), self.codetab)

        openTab = QtGui.QAction(QtGui.QIcon(self.icons+'open.png'), 'Open', self)
        openTab.setStatusTip('Open')
        openTab.setShortcut('CTRL+O')
        self.connect(openTab,QtCore.SIGNAL('triggered()'), self.open)

        saveTab = QtGui.QAction(QtGui.QIcon(self.icons+'save.png'), 'Save', self)
        saveTab.setStatusTip('Save')
        saveTab.setShortcut('CTRL+S')
        self.connect(saveTab,QtCore.SIGNAL('triggered()'), self.save)

        saveAsTab = QtGui.QAction(QtGui.QIcon(self.icons+'save.png'), 'Save As', self)
        saveAsTab.setStatusTip('Save As')
        self.connect(saveAsTab,QtCore.SIGNAL('triggered()'), self.saveAs)

        undoTab = QtGui.QAction(QtGui.QIcon(self.icons+'undo.png'), 'Undo', self)
        undoTab.setShortcut('Ctrl+Z')
        undoTab.setStatusTip('Undo')
        self.connect(undoTab, QtCore.SIGNAL('triggered()'), self.undo)

        redoTab = QtGui.QAction(QtGui.QIcon(self.icons+'redo.png'), 'Redo', self)
        redoTab.setShortcut('Ctrl+Y')
        redoTab.setStatusTip('Redo')
        self.connect(redoTab, QtCore.SIGNAL('triggered()'), self.redo)

        selectallTab = QtGui.QAction(QtGui.QIcon(self.icons+'selectall.png'), 'Select All', self)
        selectallTab.setShortcut('Ctrl+A')
        selectallTab.setStatusTip('Select All')
        self.connect(selectallTab, QtCore.SIGNAL('triggered()'), self.selectAll)

        copyTab = QtGui.QAction(QtGui.QIcon(self.icons+'copy.png'), 'Copy', self)
        copyTab.setShortcut('Ctrl+C')
        copyTab.setStatusTip('Copy')
        self.connect(copyTab, QtCore.SIGNAL('triggered()'), self.copy)

        pasteTab = QtGui.QAction(QtGui.QIcon(self.icons+'paste.png'), 'Paste', self)
        pasteTab.setShortcut('Ctrl+P')
        pasteTab.setStatusTip('Paste')
        self.connect(pasteTab, QtCore.SIGNAL('triggered()'), self.paste)

        cutTab = QtGui.QAction(QtGui.QIcon(self.icons+'cut.png'), 'Cut', self)
        cutTab.setShortcut('Ctrl+Shift+C')
        cutTab.setStatusTip('Cut')
        self.connect(cutTab, QtCore.SIGNAL('triggered()'), self.cut)

        aboutItem = QtGui.QAction(QtGui.QIcon(self.icons+'pyte.png'), 'About PyTe', self)
        aboutItem.setStatusTip('About PyTe')
        self.connect(aboutItem, QtCore.SIGNAL('triggered()'), self.about)

        self.connect(self.mainTabWidget, QtCore.SIGNAL("tabCloseRequested (int)"), self.tabClose)
        self.connect(self.mainTabWidget, QtCore.SIGNAL("currentChanged (int)"), self.tabChange)

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(newtab)
        file.addAction(closeTab)
        file.addSeparator()
        file.addAction(openTab)
        file.addAction(saveTab)
        file.addAction(saveAsTab)
        file.addSeparator()
        file.addAction(quit)

        edit = menubar.addMenu('&Edit')
        edit.addAction(undoTab)
        edit.addAction(redoTab)
        edit.addSeparator()
        edit.addAction(copyTab)
        edit.addAction(pasteTab)
        edit.addAction(cutTab)
        edit.addAction(selectallTab)

        aboutBar = menubar.addMenu('&About')
        aboutBar.addAction(aboutItem)

        toolbar = self.addToolBar('File')
        toolbar.addAction(newtab)
        toolbar.addAction(closeTab)
        toolbar.addSeparator()
        toolbar.addAction(openTab)
        toolbar.addAction(saveTab)
        toolbar.addSeparator()
        toolbar.addAction(undoTab)
        toolbar.addAction(redoTab)
        toolbar.addSeparator()
        toolbar.addAction(copyTab)
        toolbar.addAction(pasteTab)
        toolbar.addAction(cutTab)
        toolbar.addAction(selectallTab)

        timer = QtCore.QTimer(self)
        QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), self.tabUpdate)
        timer.start(1000)

    def codetab(self):
        newEditor = editor(self, self)
        newTab = self.mainTabWidget.addTab(newEditor, QtGui.QIcon(self.icons+'pyte.png'), "Code Editor")
        self.mainTabWidget.setCurrentIndex(newTab)
        self.Tabfile(self.mainTabWidget, "", 'title')

    def tabClose(self, tabIndex):
        self.fileTest = self.Tabfile(self.mainTabWidget, "", 'closeFile')
        if debug==1:
           print self.fileTest
        if self.fileTestSave==1:
           self.mainTabWidget.removeTab(tabIndex)
           self.Tabfile(self.mainTabWidget, "", 'title')

    def closetab(self):
        self.fileTest = self.Tabfile(self.mainTabWidget, "", 'closeFile')
        if debug==1:
           print self.fileTest
        if self.fileTestSave==1:
           self.mainTabWidget.removeTab(self.mainTabWidget.currentIndex())
           self.Tabfile(self.mainTabWidget, "", 'title')

    def tabChange(self, index):
        self.Tabfile(self.mainTabWidget, "", 'title')

    def tabUpdate(self):
        self.Tabfile(self.mainTabWidget, "", 'title')
        if debug==1:
           print self.windowTitle()

    def open(self):
        self.Tabfile(self.mainTabWidget, "", 'openFile')

    def save(self):
        self.Tabfile(self.mainTabWidget, "", 'saveFile')

    def saveAs(self):
        self.Tabfile(self.mainTabWidget, "", 'saveAsFile')

    def redo(self):
        self.Tabfile(self.mainTabWidget, "", 'redoFile')

    def undo(self):
        self.Tabfile(self.mainTabWidget, "", 'undoFile')

    def cut(self):
        self.Tabfile(self.mainTabWidget, "", 'cutFile')

    def selectAll(self):
        self.Tabfile(self.mainTabWidget, "", 'selectAllFile')

    def copy(self):
        self.Tabfile(self.mainTabWidget, "", 'copyFile')

    def paste(self):
        self.Tabfile(self.mainTabWidget, "", 'pasteFile')

    def about(self):
        QtGui.QMessageBox.about(self,'PyTe v3',
            'PyTe is a Source Code Editor, <br> He can open most common language files<br> and will auto set the lexer (syntax highlighing)<br> to fit the current file type. He can open unlimited files,<br> and each tab is full independent of its neighbors<br> Version:'+version+'<br><a href="mailto:joshuaashby@joshashby.com">Josh Ashby</a><br><a href="http://joshashby.com">http://joshashby.com</a><br><a href="https://github.com/JoshAshby/PyTe">Source Code</a><br><a href="https://github.com/JoshAshby/PyTe/issues">Bug Reporting</a>')

    def Tabfile(self, obj, indent, action_type):
        children=obj.children()
        if children==None:
           return
        for child in children:
           if (child.__class__ == editor):
                if debug==1:
                   print child, max(children), len(children), children[len(children)-1]
                if (child == children[len(children)-1]):
                   if debug==1:
                      print child
                   if (action_type == 'openFile'):
                      child.openFile()
                   elif (action_type == 'saveFile'):
                      child.save()
                   elif (action_type == 'saveAsFile'):
                      child.saveAs()
                   elif (action_type == 'redoFile'):
                      child.redo()
                   elif (action_type == 'undoFile'):
                      child.undo()
                   elif (action_type == 'cutFile'):
                      child.cut()
                   elif (action_type == 'selectAllFile'):
                      child.selectAll()
                   elif (action_type == 'copyFile'):
                      child.copy()
                   elif (action_type == 'pasteFile'):
                      child.paste()
                   elif (action_type == 'closeFile'):
                      self.test = child.closeEvent()
                      if debug==1:
                         print self.test
                      self.fileTestSave = self.test
                   elif (action_type == 'title'):
                      if (child.getTitle() == ''):
                         self.setWindowTitle("PyTe v3")
                      else:
                         self.setWindowTitle(child.getFile()+" - ["+child.getTitle()+"]"+" - PyTe v3")
                         self.mainTabWidget.setTabText(self.mainTabWidget.currentIndex(),child.getFile())
                         self.mainTabWidget.setTabIcon(self.mainTabWidget.currentIndex(),QtGui.QIcon(self.icons+self.lexerPic[child.getFileType()]))
                   else:
                      pass
                else:
                   pass
           else:
                self.Tabfile(child, indent + "  ", action_type)

#start the app
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
