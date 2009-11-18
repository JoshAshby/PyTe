#!/usr/bin/python
#====================About===========================
#PyTe v2
#Joshua Ashby
#http://joshashby.com
#joshuaashby@joshashby.com
#2009
#I hold no responsibility for anything that may happen to your 
#computer if you use this program or any program written in it.
#By Using PyTe you agree to the Python, and Qt License's
#All Trademarks Subject to their owners
#Licensed under the Creative Commons v3 Non-Commercial License
#===================================================
#Ver .1 Beta
#===================================================
import sys, os
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui, Qsci
from PyQt4.Qsci import QsciScintilla, QsciScintillaBase, QsciLexerPython, QsciLexerPerl, QsciLexerRuby, QsciLexerHTML, QsciLexerCSS, QsciLexerJavaScript, QsciLexerLua, QsciLexerPython, QsciLexerMakefile, QsciLexerCPP, QsciLexerBash, QsciLexerTeX, QsciLexerSQL
from PyQt4.QtWebKit import *
import ConfigParser

editorList = []
class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        #window size, default title, and icon
        self.resize(640, 480)
        self.setWindowTitle('PyTe v2')
        self.setWindowIcon(QtGui.QIcon('icons/pyte.png'))

        #sets up the Scintilla
        self.editor = Qsci.QsciScintilla()

        #reads the config file to get the colors
        self.config = ConfigParser.ConfigParser()
        self.config.read('config.cfg')
        self.fontfam = self.config.get('Section1', 'fontf')
        self.ecolor = self.config.get('Section1', 'ecol')
        self.mcolor = self.config.get('Section1', 'mcol')
        self.lncolor = self.config.get('Section1', 'lncol')
        self.mfcolor = self.config.get('Section1', 'mfcol')
        self.mbcolor = self.config.get('Section1', 'mbcol')
        self.webbar = self.config.get('Section1', 'webbar')

        #define the font to use
        self.font = QtGui.QFont()
        self.font.setFamily(self.fontfam)
        self.font.setFixedPitch(True)
        self.font.setPointSize(10)
        #the font metrics here will help
        #building the margin width later
        self.fm = QtGui.QFontMetrics(self.font)

        #set the default font of the editor
        #and take the same font for line numbers
        self.editor.setFont(self.font)
        self.editor.setMarginsFont(self.font)

        #Line numbers
        #conventionnaly, margin 0 is for line numbers
        self.editor.setMarginWidth(0, self.fm.width( "0000" ))
        self.editor.setMarginLineNumbers(0, True)

        #Folding visual : we will use boxes
        self.editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)

        #Braces matching
        self.editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        #Editing line color
        self.editor.setCaretLineVisible(True)
        self.editor.setCaretLineBackgroundColor(QtGui.QColor(self.ecolor))

        #Margins colors
        #line numbers margin
        self.editor.setMarginsBackgroundColor(QtGui.QColor(self.mcolor))
        self.editor.setMarginsForegroundColor(QtGui.QColor(self.lncolor))

        #folding margin colors (foreground,background)
        self.editor.setFoldMarginColors(QtGui.QColor(self.mfcolor),QtGui.QColor(self.mbcolor))

        #Choose a lexer
        lexer = QsciLexerPython()
        lexer.setDefaultFont(self.font)
        self.editor.setLexer(lexer)

        #setup the different actions
        exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        new = QtGui.QAction(QtGui.QIcon('icons/new.png'), 'New', self)
        new.setShortcut('Ctrl+N')
        new.setStatusTip('New')
        self.connect(new, QtCore.SIGNAL('triggered()'), self.new)

        openf = QtGui.QAction(QtGui.QIcon('icons/open.png'), 'Open', self)
        openf.setShortcut('Ctrl+O')
        openf.setStatusTip('Open')
        self.connect(openf, QtCore.SIGNAL('triggered()'), self.openfile)

        saveas = QtGui.QAction(QtGui.QIcon('icons/save.png'), 'Save As', self)
        saveas.setShortcut('Ctrl+Shft+S')
        saveas.setStatusTip('Save As')
        self.connect(saveas, QtCore.SIGNAL('triggered()'), self.saveAs)

        undo = QtGui.QAction(QtGui.QIcon('icons/undo.png'), 'Undo', self)
        undo.setShortcut('Ctrl+Z')
        undo.setStatusTip('Undo')
        self.connect(undo, QtCore.SIGNAL('triggered()'), self.editor.undo)

        redo = QtGui.QAction(QtGui.QIcon('icons/redo.png'), 'Redo', self)
        redo.setShortcut('Ctrl+Y')
        redo.setStatusTip('Redo')
        self.connect(redo, QtCore.SIGNAL('triggered()'), self.editor.redo)

        selectall = QtGui.QAction(QtGui.QIcon('icons/selectall.png'), 'Select All', self)
        selectall.setShortcut('Ctrl+A')
        selectall.setStatusTip('Select All')
        self.connect(selectall, QtCore.SIGNAL('triggered()'), self.editor.selectAll)

        copy = QtGui.QAction(QtGui.QIcon('icons/copy.png'), 'Copy', self)
        copy.setShortcut('Ctrl+C')
        copy.setStatusTip('Copy')
        self.connect(copy, QtCore.SIGNAL('triggered()'), self.editor.copy)

        paste = QtGui.QAction(QtGui.QIcon('icons/paste.png'), 'Paste', self)
        paste.setShortcut('Ctrl+P')
        paste.setStatusTip('Paste')
        self.connect(paste, QtCore.SIGNAL('triggered()'), self.editor.paste)

        cut = QtGui.QAction(QtGui.QIcon('icons/cut.png'), 'Cut', self)
        cut.setShortcut('Ctrl+Shft+C')
        cut.setStatusTip('Cut')
        self.connect(cut, QtCore.SIGNAL('triggered()'), self.editor.cut)

        sidebar = QtGui.QAction(QtGui.QIcon('icons/sidebar.png'), 'Sidebar Color', self)
        sidebar.setStatusTip('Sidebar Color')
        self.connect(sidebar, QtCore.SIGNAL('triggered()'), self.sidebar)

        textcol = QtGui.QAction(QtGui.QIcon('icons/textcol.png'), 'Line # Color', self)
        textcol.setStatusTip('Line # Color')
        self.connect(textcol, QtCore.SIGNAL('triggered()'), self.textcol)

        mbcol = QtGui.QAction(QtGui.QIcon('icons/mbcol.png'), 'Margin Background Color', self)
        mbcol.setStatusTip('Margin Background Color')
        self.connect(mbcol, QtCore.SIGNAL('triggered()'), self.mbcol)

        mfcol = QtGui.QAction(QtGui.QIcon('icons/mfcol.png'), 'Margin Forground Color', self)
        mfcol.setStatusTip('Margin Foreground Color')
        self.connect(mfcol, QtCore.SIGNAL('triggered()'), self.mfcol)

        ecol = QtGui.QAction(QtGui.QIcon('icons/ecol.png'), 'Edit line # Color', self)
        ecol.setStatusTip('Edit line # Color')
        self.connect(ecol, QtCore.SIGNAL('triggered()'), self.ecol)

        perl = QtGui.QAction(QtGui.QIcon('icons/perl.png'), 'Perl', self)
        perl.setStatusTip('Perl Lexar')
        self.connect(perl, QtCore.SIGNAL('triggered()'), self.perl)

        ruby = QtGui.QAction(QtGui.QIcon('icons/ruby.png'), 'Ruby', self)
        ruby.setStatusTip('Ruby Lexar')
        self.connect(ruby, QtCore.SIGNAL('triggered()'), self.ruby)

        html = QtGui.QAction(QtGui.QIcon('icons/html.png'), 'HTML', self)
        html.setStatusTip('HTML Lexar')
        self.connect(html, QtCore.SIGNAL('triggered()'), self.html)

        css = QtGui.QAction(QtGui.QIcon('icons/css.png'), 'CSS', self)
        css.setStatusTip('CSS Lexar')
        self.connect(css, QtCore.SIGNAL('triggered()'), self.css)

        javascript = QtGui.QAction(QtGui.QIcon('icons/javascript.png'), 'Javascript', self)
        javascript.setStatusTip('Javascript Lexar')
        self.connect(javascript, QtCore.SIGNAL('triggered()'), self.javascript)

        lua = QtGui.QAction(QtGui.QIcon('icons/lua.png'), 'Lua', self)
        lua.setStatusTip('Lua Lexar')
        self.connect(lua, QtCore.SIGNAL('triggered()'), self.lua)

        python = QtGui.QAction(QtGui.QIcon('icons/python.png'), 'Python', self)
        python.setStatusTip('Python Lexar')
        self.connect(python, QtCore.SIGNAL('triggered()'), self.python)

        make = QtGui.QAction(QtGui.QIcon('icons/makefile.png'), 'Make', self)
        make.setStatusTip('Make Lexar')
        self.connect(make, QtCore.SIGNAL('triggered()'), self.make)

        cpp = QtGui.QAction(QtGui.QIcon('icons/cpp.png'), 'CPP', self)
        cpp.setStatusTip('CPP Lexar')
        self.connect(cpp, QtCore.SIGNAL('triggered()'), self.cpp)

        bash = QtGui.QAction(QtGui.QIcon('icons/bash.png'), 'Bash', self)
        bash.setStatusTip('Bash Lexar')
        self.connect(bash, QtCore.SIGNAL('triggered()'), self.bash)

        tex = QtGui.QAction(QtGui.QIcon('icons/tex.png'), 'TeX', self)
        tex.setStatusTip('TeX Lexar')
        self.connect(tex, QtCore.SIGNAL('triggered()'), self.tex)

        sql = QtGui.QAction(QtGui.QIcon('icons/sql.png'), 'SQL', self)
        sql.setStatusTip('SQL Lexar')
        self.connect(sql, QtCore.SIGNAL('triggered()'), self.sql)

        helpw = QtGui.QAction(QtGui.QIcon('icons/help.png'), 'Help', self)
        helpw.setShortcut('Ctrl+H')
        helpw.setStatusTip('Help')
        self.connect(helpw, QtCore.SIGNAL('triggered()'), self.helpw)

        backh = QtGui.QAction(QtGui.QIcon('icons/back.png'), 'Help Back', self)
        backh.setStatusTip('Help Back')
        self.connect(backh, QtCore.SIGNAL('triggered()'), self.backh)

        nexth = QtGui.QAction(QtGui.QIcon('icons/next.png'), 'Help Forward', self)
        nexth.setStatusTip('Help Forward')
        self.connect(nexth, QtCore.SIGNAL('triggered()'), self.nexth)

        backw = QtGui.QAction(QtGui.QIcon('icons/back.png'), 'Back', self)
        backw.setStatusTip('Back')
        self.connect(backw, QtCore.SIGNAL('triggered()'), self.backw)

        nextw = QtGui.QAction(QtGui.QIcon('icons/next.png'), 'Forward', self)
        nextw.setStatusTip('Forward')
        self.connect(nextw, QtCore.SIGNAL('triggered()'), self.nextw)

        self.progress = QtGui.QProgressBar()

        self.help = QWebView()
        __Dir = os.path.dirname(sys.argv[0])
        self.doc = os.path.join(__Dir, 'doc/index.html')
#debug        print self.doc
        self.ur = "file://" + self.doc
        QtCore.QObject.connect(self.help,QtCore.SIGNAL("linkClicked (const QUrl&)"), self.link_clicked)
	self.help.setUrl(QtCore.QUrl(self.ur))

        self.adress = QtGui.QLineEdit()

        self.webbackb = QtGui.QPushButton(QtGui.QIcon('icons/back.png'),"")
        self.connect(self.webbackb, QtCore.SIGNAL("clicked()"), self.backw)

        self.webnextb = QtGui.QPushButton(QtGui.QIcon('icons/next.png'), "")
        self.connect(self.webnextb, QtCore.SIGNAL("clicked()"), self.nextw)

        self.buttonBox = QtGui.QHBoxLayout()
        self.buttonBox.addWidget(self.webbackb)
        self.buttonBox.addWidget(self.webnextb)
        self.buttonBox.addWidget(self.adress)
        self.buttonBox.addWidget(self.progress)

        self.helpbackb = QtGui.QPushButton(QtGui.QIcon('icons/back.png'),"Back")
        self.connect(self.helpbackb, QtCore.SIGNAL("clicked()"), self.backh)

        self.helpnextb = QtGui.QPushButton(QtGui.QIcon('icons/next.png'), "Forward")
        self.connect(self.helpnextb, QtCore.SIGNAL("clicked()"), self.nexth)

        self.buttonBoxhelp = QtGui.QHBoxLayout()
        self.buttonBoxhelp.addWidget(self.helpbackb)
        self.buttonBoxhelp.addWidget(self.helpnextb)

        self.web = QWebView()
        self.urld = "http://google.com"
        QtCore.QObject.connect(self.web,QtCore.SIGNAL("linkClicked (const QUrl&)"), self.link_clicked_web)
        QtCore.QObject.connect(self.adress,QtCore.SIGNAL("returnPressed()"), self.url_changed)
        QtCore.QObject.connect(self.web,QtCore.SIGNAL("loadProgress (int)"), self.load_progress)
        self.adress.setText(self.urld)
	self.web.setUrl(QtCore.QUrl(self.urld))

        self.tab_widget = QtGui.QTabWidget() 
        self.tab1 = QtGui.QWidget() 
        self.tab2 = QtGui.QWidget()
        self.tab3 = QtGui.QWidget()
         
        self.p1_vertical = QtGui.QVBoxLayout(self.tab1) 
        self.p2_vertical = QtGui.QVBoxLayout(self.tab2) 
        self.p3_vertical = QtGui.QVBoxLayout(self.tab3) 
         
        self.tab_widget.addTab(self.tab1, "Code Editor",) 
        self.tab_widget.addTab(self.tab2, "Web Browser",) 

        self.p1_vertical.addWidget(self.editor)
        self.p2_vertical.addLayout(self.buttonBox)
        self.p2_vertical.addWidget(self.web)
        self.p3_vertical.addLayout(self.buttonBoxhelp)
        self.p3_vertical.addWidget(self.help)

        self.setCentralWidget(self.tab_widget)

        self.statusBar()

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(new)
        file.addAction(openf)
        file.addAction(saveas)
        file.addAction(exit)
        edit = menubar.addMenu('&Edit')
        edit.addAction(undo)
        edit.addAction(redo)
        edit.addAction(selectall)
        edit.addAction(copy)
        edit.addAction(paste)
        edit.addAction(cut)
        edit.addAction(helpw)
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
        toolbar.addSeparator()
        toolbar.addAction(exit)

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

    #defines the different functions for the actions above
    def load_progress(self, load):
        self.progress.setValue(load)

    def url_changed(self):
        url = self.adress.text()
        self.web.setUrl(QtCore.QUrl(url))

    def backh(self):
        page = self.help.page()
        history = page.history()
        history.back()

    def nexth(self):
        page = self.help.page()
        history = page.history()
        history.forward()

    def backw(self):
        page = self.web.page()
        history = page.history()
        history.back()

    def nextw(self):
        page = self.web.page()
        history = page.history()
        history.forward()

    def helpw(self):
        self.tab_widget.addTab(self.tab3, "Help")

    def link_clicked(self, url):
        self.help.setUrl(QtCore.QUrl(url))

    def link_clicked_web(self, url):
        self.web.setUrl(QtCore.QUrl(url))
        self.adress.setText(url)

    def sidebar(self):
        col = QtGui.QColorDialog.getColor()

        if col.isValid():
            self.editor.setMarginsBackgroundColor(QtGui.QColor(col.name()))
            self.config.set('Section1', 'mcol', col.name())
            with open('config.cfg', 'wb') as configfile:
                 self.config.write(configfile)

    def textcol(self):
        col = QtGui.QColorDialog.getColor()

        if col.isValid():
            self.editor.setMarginsForegroundColor(QtGui.QColor(col.name()))
            self.config.set('Section1', 'lncol', col.name())
            with open('config.cfg', 'wb') as configfile:
                 self.config.write(configfile)

    def mfcol(self):
        col = QtGui.QColorDialog.getColor()

        if col.isValid():
            self.editor.setFoldMarginColors(QtGui.QColor(col.name()),QtGui.QColor(self.mbcol))
            self.config.set('Section1', 'mfcol', col.name())
            with open('config.cfg', 'wb') as configfile:
                 self.config.write(configfile)

    def mbcol(self):
        col = QtGui.QColorDialog.getColor()

        if col.isValid():
            self.editor.setFoldMarginColors(QtGui.QColor(self.mfcol),QtGui.QColor(col.name()))
            self.config.set('Section1', 'mbcol', col.name())
            with open('config.cfg', 'wb') as configfile:
                 self.config.write(configfile)

    def ecol(self):
        col = QtGui.QColorDialog.getColor()

        if col.isValid():
            self.editor.setCaretLineBackgroundColor(QtGui.QColor(col.name()))
            self.config.set('Section1', 'ecol', col.name())
            with open('config.cfg', 'wb') as configfile:
                 self.config.write(configfile)

    def perl(self):
        lexer = QsciLexerPerl()
        self.editor.setLexer(lexer)

    def ruby(self):
        lexer = QsciLexerRuby()
        self.editor.setLexer(lexer)

    def html(self):
        lexer = QsciLexerHTML()
        self.editor.setLexer(lexer)

    def css(self):
        lexer = QsciLexerCSS()
        self.editor.setLexer(lexer)

    def javascript(self):
        lexer = QsciLexerJavaScript()
        self.editor.setLexer(lexer)

    def lua(self):
        lexer = QsciLexerLua()
        self.editor.setLexer(lexer)

    def python(self):
        lexer = QsciLexerPython()
        self.editor.setLexer(lexer)

    def make(self):
        lexer = QsciLexerMakefile()
        self.editor.setLexer(lexer)

    def cpp(self):
        lexer = QsciLexerCPP()
        self.editor.setLexer(lexer)

    def bash(self):
        lexer = QsciLexerBash()
        self.editor.setLexer(lexer)

    def tex(self):
        lexer = QsciLexerTeX()
        self.editor.setLexer(lexer)

    def sql(self):
        lexer = QsciLexerSQL()
        self.editor.setLexer(lexer)

    def new(self):
        main = MainWindow()
        main.show()
        editorList.append(main)

    def openfile(self):
        fn = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home', '')

        if fn.isEmpty():
            return

        fileName = str(fn)

        try:
            f = open(fileName,'r').read()
            self.editor.setText(f)
        except:
            return

        self.setWindowTitle(fileName+" - PyTe v2")

    def saveAs(self):
        fn = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '')
        try:
            f = open(str(fn),'w+r')
        except:
            return

        f.write(str(self.editor.text()))
        f.close()

#start the app
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
