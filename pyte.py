#!/usr/bin/python
#====================About===========================
#PyTe v2
#Joshua Ashby
#http://joshashby.com
#joshuaashby@joshashby.com
#2011
#
#PyTe, or Python Text Editor as he started off being named, is
#a semi advanced code editor that i have been writting for the
#past several years. He uses the PyQt4 gui library, and is meant
#to be somewhat stand alone.
#he includes a qtwebkit web browser as i have found having a
#browser and a code editor in the same window to be helpful
#
#I hold no responsibility for anything that may happen to your 
#computer if you use this program or any program written in it.
#By Using PyTe you agree to the Python, and Qt License's
#All Trademarks Subject to their owners
#Licensed under the Creative Commons v3 Non-Commercial License
#===================================================
#Ver .9 Alpha
#===================================================
import sys, os
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui, Qsci
from PyQt4.Qsci import QsciScintilla, QsciScintillaBase, QsciLexerPython, QsciLexerPerl, QsciLexerRuby, QsciLexerHTML, QsciLexerCSS, QsciLexerJavaScript, QsciLexerLua, QsciLexerPython, QsciLexerMakefile, QsciLexerCPP, QsciLexerBash, QsciLexerTeX, QsciLexerSQL
import ConfigParser

editorList = []
class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.tab_widget = QtGui.QTabWidget()
        self.__Dir = os.path.dirname(sys.argv[0])
        self.icons =  os.path.join(self.__Dir, 'icons/')

        self.resize(640, 480)
        self.setWindowTitle('PyTe v2')
        self.setWindowIcon(QtGui.QIcon(self.icons+'pyte.png'))

        self.config = ConfigParser.ConfigParser()
        self.configfile =  os.path.join(self.__Dir, 'config.cfg')
        self.config.read(self.configfile)
        self.fontfam = self.config.get('Section1', 'fontf')
        self.ecolor = self.config.get('Section1', 'ecol')
        self.mcolor = self.config.get('Section1', 'mcol')
        self.lncolor = self.config.get('Section1', 'lncol')
        self.mfcolor = self.config.get('Section1', 'mfcol')
        self.mbcolor = self.config.get('Section1', 'mbcol')

        self.font = QtGui.QFont()
        self.font.setFamily(self.fontfam)
        self.font.setFixedPitch(True)
        self.font.setPointSize(10)

        self.fm = QtGui.QFontMetrics(self.font)

        self.codelist = []
        self.tablist =[]
        self.plist = []

        self.code = len(self.codelist)
        self.tab = len(self.tablist)
        self.p = len(self.plist)

        self.code = Qsci.QsciScintilla()
        self.code.setFont(self.font)
        self.code.setMarginsFont(self.font)
        self.code.setMarginWidth(0, self.fm.width( "0000" ))
        self.code.setMarginLineNumbers(0, True)
        self.code.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        self.code.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.code.setCaretLineVisible(True)
        self.code.setCaretLineBackgroundColor(QtGui.QColor(self.ecolor))
        self.code.setMarginsBackgroundColor(QtGui.QColor(self.mcolor))
        self.code.setMarginsForegroundColor(QtGui.QColor(self.lncolor))
        self.code.setFoldMarginColors(QtGui.QColor(self.mfcolor),QtGui.QColor(self.mbcolor))
        lexer = QsciLexerPython()
        self.code.setLexer(lexer)

        self.editor = self.code

        #setup the different actions
        quit = QtGui.QAction(QtGui.QIcon(self.icons+'exit.png'), 'Exit', self)
        quit.setShortcut('Ctrl+Q')
        quit.setStatusTip('Exit')
        self.connect(quit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        exit = QtGui.QAction(QtGui.QIcon(self.icons+'exit.png'), 'Close Tab', self)
        exit.setStatusTip('Close Tab')
        self.connect(exit, QtCore.SIGNAL('triggered()'), self.closetab)

        new = QtGui.QAction(QtGui.QIcon(self.icons+'new.png'), 'New', self)
        new.setShortcut('Ctrl+N')
        new.setStatusTip('New')
        self.connect(new, QtCore.SIGNAL('triggered()'), self.new)

        openf = QtGui.QAction(QtGui.QIcon(self.icons+'open.png'), 'Open', self)
        openf.setShortcut('Ctrl+O')
        openf.setStatusTip('Open')
        self.connect(openf, QtCore.SIGNAL('triggered()'), self.openfile)

        saveas = QtGui.QAction(QtGui.QIcon(self.icons+'save.png'), 'Save As', self)
        saveas.setShortcut('Ctrl+Shft+S')
        saveas.setStatusTip('Save As')
        self.connect(saveas, QtCore.SIGNAL('triggered()'), self.saveAs)

        undo = QtGui.QAction(QtGui.QIcon(self.icons+'undo.png'), 'Undo', self)
        undo.setShortcut('Ctrl+Z')
        undo.setStatusTip('Undo')
        self.connect(undo, QtCore.SIGNAL('triggered()'), self.editor.undo)

        redo = QtGui.QAction(QtGui.QIcon(self.icons+'redo.png'), 'Redo', self)
        redo.setShortcut('Ctrl+Y')
        redo.setStatusTip('Redo')
        self.connect(redo, QtCore.SIGNAL('triggered()'), self.editor.redo)

        selectall = QtGui.QAction(QtGui.QIcon(self.icons+'selectall.png'), 'Select All', self)
        selectall.setShortcut('Ctrl+A')
        selectall.setStatusTip('Select All')
        self.connect(selectall, QtCore.SIGNAL('triggered()'), self.editor.selectAll)

        copy = QtGui.QAction(QtGui.QIcon(self.icons+'copy.png'), 'Copy', self)
        copy.setShortcut('Ctrl+C')
        copy.setStatusTip('Copy')
        self.connect(copy, QtCore.SIGNAL('triggered()'), self.editor.copy)

        paste = QtGui.QAction(QtGui.QIcon(self.icons+'paste.png'), 'Paste', self)
        paste.setShortcut('Ctrl+P')
        paste.setStatusTip('Paste')
        self.connect(paste, QtCore.SIGNAL('triggered()'), self.editor.paste)

        cut = QtGui.QAction(QtGui.QIcon(self.icons+'cut.png'), 'Cut', self)
        cut.setShortcut('Ctrl+Shift+C')
        cut.setStatusTip('Cut')
        self.connect(cut, QtCore.SIGNAL('triggered()'), self.editor.cut)

        sidebar = QtGui.QAction(QtGui.QIcon(self.icons+'sidebar.png'), 'Sidebar Color', self)
        sidebar.setStatusTip('Sidebar Color')
        self.connect(sidebar, QtCore.SIGNAL('triggered()'), self.sidebar)

        textcol = QtGui.QAction(QtGui.QIcon(self.icons+'textcol.png'), 'Line # Color', self)
        textcol.setStatusTip('Line # Color')
        self.connect(textcol, QtCore.SIGNAL('triggered()'), self.textcol)

        mbcol = QtGui.QAction(QtGui.QIcon(self.icons+'mbcol.png'), 'Margin Background Color', self)
        mbcol.setStatusTip('Margin Background Color')
        self.connect(mbcol, QtCore.SIGNAL('triggered()'), self.mbcol)

        mfcol = QtGui.QAction(QtGui.QIcon(self.icons+'mfcol.png'), 'Margin Forground Color', self)
        mfcol.setStatusTip('Margin Foreground Color')
        self.connect(mfcol, QtCore.SIGNAL('triggered()'), self.mfcol)

        ecol = QtGui.QAction(QtGui.QIcon(self.icons+'ecol.png'), 'Edit line # Color', self)
        ecol.setStatusTip('Edit line # Color')
        self.connect(ecol, QtCore.SIGNAL('triggered()'), self.ecol)

        perl = QtGui.QAction(QtGui.QIcon(self.icons+'perl.png'), 'Perl', self)
        perl.setStatusTip('Perl Lexar')
        self.connect(perl, QtCore.SIGNAL('triggered()'), self.perl)

        ruby = QtGui.QAction(QtGui.QIcon(self.icons+'ruby.png'), 'Ruby', self)
        ruby.setStatusTip('Ruby Lexar')
        self.connect(ruby, QtCore.SIGNAL('triggered()'), self.ruby)

        html = QtGui.QAction(QtGui.QIcon(self.icons+'html.png'), 'HTML', self)
        html.setStatusTip('HTML Lexar')
        self.connect(html, QtCore.SIGNAL('triggered()'), self.html)

        css = QtGui.QAction(QtGui.QIcon(self.icons+'css.png'), 'CSS', self)
        css.setStatusTip('CSS Lexar')
        self.connect(css, QtCore.SIGNAL('triggered()'), self.css)

        javascript = QtGui.QAction(QtGui.QIcon(self.icons+'javascript.png'), 'Javascript', self)
        javascript.setStatusTip('Javascript Lexar')
        self.connect(javascript, QtCore.SIGNAL('triggered()'), self.javascript)

        lua = QtGui.QAction(QtGui.QIcon(self.icons+'lua.png'), 'Lua', self)
        lua.setStatusTip('Lua Lexar')
        self.connect(lua, QtCore.SIGNAL('triggered()'), self.lua)

        python = QtGui.QAction(QtGui.QIcon(self.icons+'python.png'), 'Python', self)
        python.setStatusTip('Python Lexar')
        self.connect(python, QtCore.SIGNAL('triggered()'), self.python)

        make = QtGui.QAction(QtGui.QIcon(self.icons+'makefile.png'), 'Make', self)
        make.setStatusTip('Make Lexar')
        self.connect(make, QtCore.SIGNAL('triggered()'), self.make)

        cpp = QtGui.QAction(QtGui.QIcon(self.icons+'cpp.png'), 'CPP', self)
        cpp.setStatusTip('CPP Lexar')
        self.connect(cpp, QtCore.SIGNAL('triggered()'), self.cpp)

        bash = QtGui.QAction(QtGui.QIcon(self.icons+'bash.png'), 'Bash', self)
        bash.setStatusTip('Bash Lexar')
        self.connect(bash, QtCore.SIGNAL('triggered()'), self.bash)

        tex = QtGui.QAction(QtGui.QIcon(self.icons+'tex.png'), 'TeX', self)
        tex.setStatusTip('TeX Lexar')
        self.connect(tex, QtCore.SIGNAL('triggered()'), self.tex)

        sql = QtGui.QAction(QtGui.QIcon(self.icons+'sql.png'), 'SQL', self)
        sql.setStatusTip('SQL Lexar')
        self.connect(sql, QtCore.SIGNAL('triggered()'), self.sql)

        newtab = QtGui.QAction(QtGui.QIcon(self.icons+'add.png'), 'Add Tab', self)
        newtab.setStatusTip('Add Tab')
        newtab.connect(newtab,QtCore.SIGNAL('triggered()'), self.codetab)

        self.tab_widget = QtGui.QTabWidget()
        self.tab = QtGui.QWidget()
        self.p = QtGui.QVBoxLayout(self.tab)
        self.tab_widget.addTab(self.tab, QtGui.QIcon(self.icons+'tex.png'), "Code Editor")
        self.p.addWidget(self.code)

        self.codelist.append(self.code)
        self.tablist.append(self.tab)
        self.plist.append(self.p)

        self.tab = len(self.tablist)
        self.p = len(self.plist)

        self.tablist.append(self.tab)
        self.plist.append(self.p)

        self.setCentralWidget(self.tab_widget)

        self.statusBar()

        self.filename = ""

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(new)
        file.addAction(openf)
        file.addAction(saveas)
        file.addAction(newtab)
        file.addAction(exit)
        file.addAction(quit)
        edit = menubar.addMenu('&Edit')
        edit.addAction(undo)
        edit.addAction(redo)
        edit.addAction(selectall)
        edit.addAction(copy)
        edit.addAction(paste)
        edit.addAction(cut)
        lex = menubar.addMenu('&Lexar')
        lex.addAction(python)
        lex.addAction(perl)
        lex.addAction(ruby)
        lex.addAction(javascript)
        lex.addAction(lua)
        lex.addAction(bash)
        lex.addAction(make)
        lex.addAction(cpp)
        lex.addAction(tex)
        lex.addAction(html)
        lex.addAction(css)
        lex.addAction(sql)
        opt = menubar.addMenu('&Options')
        opt.addAction(sidebar)
        opt.addAction(textcol)
        opt.addAction(mbcol)
        opt.addAction(mfcol)
        opt.addAction(ecol)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(new)
        toolbar.addSeparator()
        toolbar.addAction(exit)
        toolbar.addAction(newtab)
        toolbar.addSeparator()
        toolbar.addAction(openf)
        toolbar.addAction(saveas)
        toolbar.addSeparator()
        toolbar.addAction(undo)
        toolbar.addAction(redo)
        toolbar.addSeparator()
        toolbar.addAction(selectall)
        toolbar.addAction(copy)
        toolbar.addAction(paste)
        toolbar.addAction(cut)

        toolbarlex = self.addToolBar('lex')
        toolbarlex.addAction(python)
        toolbarlex.addAction(perl)
        toolbarlex.addAction(ruby)
        toolbarlex.addAction(javascript)
        toolbarlex.addAction(lua)
        toolbarlex.addAction(bash)
        toolbarlex.addAction(make)
        toolbarlex.addAction(cpp)
        toolbarlex.addAction(tex)
        toolbarlex.addAction(html)
        toolbarlex.addAction(css)
        toolbarlex.addAction(sql)

        #if there is a argument passed then try to open it as a file
        if (len(sys.argv) > 1):
            fn = sys.argv[1]

            fileName = str(fn)

            try:
                f = open(fileName,'r').read()
                self.editor.setText(f)
            except:
                return

            self.setWindowTitle(fileName+" - PyTe v2")

        else:
            pass

    def closetab(self):
        self.codeli = self.tab_widget.currentIndex()
#debug        print self.codeli
        if (self.codeli == -1):
            self.codetab()
        else:
            self.tab_widget.removeTab(self.codeli)

            self.max = self.codeli + 1

    def codetab(self):
        self.code = Qsci.QsciScintilla()
        self.code.setFont(self.font)
        self.code.setMarginsFont(self.font)
        self.code.setMarginWidth(0, self.fm.width( "0000" ))
        self.code.setMarginLineNumbers(0, True)
        self.code.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        self.code.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.code.setCaretLineVisible(True)
        self.code.setCaretLineBackgroundColor(QtGui.QColor(self.ecolor))
        self.code.setMarginsBackgroundColor(QtGui.QColor(self.mcolor))
        self.code.setMarginsForegroundColor(QtGui.QColor(self.lncolor))
        self.code.setFoldMarginColors(QtGui.QColor(self.mfcolor),QtGui.QColor(self.mbcolor))
        lexer = QsciLexerPython()
        self.code.setLexer(lexer)

        self.tab = QtGui.QWidget()
        self.p = QtGui.QVBoxLayout(self.tab)
        self.tab_widget.addTab(self.tab, QtGui.QIcon(self.icons+'tex.png'), "Code Editor")
        self.p.addWidget(self.code)

        self.codelist.append(self.code)
        self.tablist.append(self.tab)
        self.plist.append(self.p)

    def sidebar(self):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)
        col = QtGui.QColorDialog.getColor()

        if col.isValid():
            self.editor.setMarginsBackgroundColor(QtGui.QColor(col.name()))
            self.config.set('Section1', 'mcol', col.name())
            with open('config.cfg', 'wb') as configfile:
                 self.config.write(configfile)

    def textcol(self):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)
        col = QtGui.QColorDialog.getColor()

        if col.isValid():
            self.editor.setMarginsForegroundColor(QtGui.QColor(col.name()))
            self.config.set('Section1', 'lncol', col.name())
            with open('config.cfg', 'wb') as configfile:
                 self.config.write(configfile)

    def mfcol(self):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)
        col = QtGui.QColorDialog.getColor()

        if col.isValid():
            self.editor.setFoldMarginColors(QtGui.QColor(col.name()),QtGui.QColor(self.mbcol))
            self.config.set('Section1', 'mfcol', col.name())
            with open('config.cfg', 'wb') as configfile:
                 self.config.write(configfile)

    def mbcol(self):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)
        col = QtGui.QColorDialog.getColor()

        if col.isValid():
            self.editor.setFoldMarginColors(QtGui.QColor(self.mfcol),QtGui.QColor(col.name()))
            self.config.set('Section1', 'mbcol', col.name())
            with open('config.cfg', 'wb') as configfile:
                 self.config.write(configfile)

    def ecol(self):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)
        col = QtGui.QColorDialog.getColor()

        if col.isValid():
            self.editor.setCaretLineBackgroundColor(QtGui.QColor(col.name()))
            self.config.set('Section1', 'ecol', col.name())
            with open('config.cfg', 'wb') as configfile:
                 self.config.write(configfile)

    def perl(self):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)
        lexer = QsciLexerPerl()
        self.editor.setLexer(lexer)

    def ruby(self):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)
        lexer = QsciLexerRuby()
        self.editor.setLexer(lexer)

    def html(self):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)
        lexer = QsciLexerHTML()
        self.editor.setLexer(lexer)

    def css(self):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)
        lexer = QsciLexerCSS()
        self.editor.setLexer(lexer)

    def javascript(self):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)
        lexer = QsciLexerJavaScript()
        self.editor.setLexer(lexer)

    def lua(self):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)
        lexer = QsciLexerLua()
        self.editor.setLexer(lexer)

    def python(self):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)
        lexer = QsciLexerPython()
        self.editor.setLexer(lexer)

    def make(self):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)
        lexer = QsciLexerMakefile()
        self.editor.setLexer(lexer)

    def cpp(self):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)
        lexer = QsciLexerCPP()
        self.editor.setLexer(lexer)

    def bash(self):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)
        lexer = QsciLexerBash()
        self.editor.setLexer(lexer)

    def tex(self):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)
        lexer = QsciLexerTeX()
        self.editor.setLexer(lexer)

    def sql(self):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)
        lexer = QsciLexerSQL()
        self.editor.setLexer(lexer)

    def new(self):
        main = MainWindow()
        main.show()
        editorList.append(main)

    def openfile(self):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)

        self.fn = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home', '')

        if self.fn.isEmpty():
            return

        self.fileName = str(self.fn)

        try:
            self.f = open(self.fileName,'r').read()
            self.editor.setText(self.f)
        except:
            return

        self.setWindowTitle(self.fileName+" - PyTe v2")

    def saveAs(self):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)

        self.fn = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '')
        try:
            self.f = open(str(self.fn),'w+r')
        except:
            return

        self.f.write(str(self.editor.text()))
        self.f.close()

    def closeEvent(self, event):
        self.codeli = self.tab_widget.currentIndex()
        self.numb = self.tab_widget.tabText(self.codeli-1)
        if (self.editor.isModified() == True):
            if (self.filename == ""):
                ret = QtGui.QMessageBox.warning(self, "PyTe",
                            "The Code has been modified.\n"
                            "Do you want to save your changes?",
                            QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
                            QtGui.QMessageBox.Cancel)
                if ret == QtGui.QMessageBox.Save:
                    self.fn = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '')
                    try:
                       self.f = open(str(self.fn),'w+r')
                    except:
                       return

                    self.f.write(str(self.editor.text()))
                    self.f.close()
                    event.accept()
                elif ret == QtGui.QMessageBox.Cancel:
                    event.ignore()
        else:
            event.accept()

#start the app
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
