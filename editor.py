#!/usr/bin/python
import sys, os
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui, Qsci
from PyQt4.Qsci import QsciScintilla, QsciScintillaBase, QsciLexerPython, QsciLexerPerl, QsciLexerRuby, QsciLexerHTML, QsciLexerCSS, QsciLexerJavaScript, QsciLexerLua, QsciLexerPython, QsciLexerMakefile, QsciLexerCPP, QsciLexerBash, QsciLexerTeX, QsciLexerSQL, QsciLexerXML
import ConfigParser
import ast

class editor(QtGui.QWidget):
   def __init__(self, parent, main):
       QtGui.QWidget.__init__(self)

       self.__Dir = os.path.dirname(sys.argv[0])
       self.icons =  os.path.join(self.__Dir, 'icons/')

       self.main = main

       mainLayout = QtGui.QVBoxLayout()
       mainLayout.setContentsMargins(0, 0, 0, 0)
       mainLayout.setSpacing(0)
       self.setLayout(mainLayout)

       self.editor = QsciScintilla(self)
       #parse the config file and grab all the stuff we need to configure some basics in scintilla
       self.config = ConfigParser.ConfigParser()
       self.configfile =  os.path.join(self.__Dir, 'config.cfg')
       self.config.read(self.configfile)
       self.fontfam = self.config.get('Section1', 'fontf')
       self.ecolor = self.config.get('Section1', 'ecol')
       self.mcolor = self.config.get('Section1', 'mcol')
       self.lncolor = self.config.get('Section1', 'lncol')
       self.mfcolor = self.config.get('Section1', 'mfcol')
       self.mbcolor = self.config.get('Section1', 'mbcol')
       self.fontSize = ast.literal_eval(self.config.get('Section1', 'fontSize'))
       self.fixedPitch = ast.literal_eval(self.config.get('Section1', 'fixedPitch'))
       self.marginWidth = self.config.get('Section1', 'marginWidth')
       self.autoIndent = ast.literal_eval(self.config.get('Section1', 'autoIndent'))
       self.marginLine = ast.literal_eval(self.config.get('Section1', 'marginLineNumber'))
       self.marginLineSec = ast.literal_eval(self.config.get('Section1', 'marginLineNumberSecond'))
       self.setUf = ast.literal_eval(self.config.get('Section1', 'setUf8'))
       self.carretLine = ast.literal_eval(self.config.get('Section1', 'carretLine'))
       self.defaultLexer = self.config.get('Section1', 'defaultLexer')

       #set all the basics for scintilla, should be pretty explanitory
       self.font = QtGui.QFont()
       self.font.setFamily(self.fontfam)
       self.font.setFixedPitch(self.fixedPitch)
       self.font.setPointSize(self.fontSize)
       self.fm = QtGui.QFontMetrics(self.font)
       self.editor.setFont(self.font)
       self.editor.setMarginsFont(self.font)
       self.editor.setMarginWidth(0, self.fm.width( self.marginWidth ))
       self.editor.setAutoCompletionSource(QsciScintilla.AcsAll)
       self.editor.setAutoIndent(self.autoIndent)
       self.editor.setMarginLineNumbers(self.marginLine, self.marginLineSec)
       self.editor.setUtf8(self.setUf)
       self.editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)
       self.editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)
       self.editor.setCaretLineVisible(self.carretLine)
       self.editor.setCaretLineBackgroundColor(QtGui.QColor(self.ecolor))
       self.editor.setMarginsBackgroundColor(QtGui.QColor(self.mcolor))
       self.editor.setMarginsForegroundColor(QtGui.QColor(self.lncolor))
       self.editor.setFoldMarginColors(QtGui.QColor(self.mfcolor),QtGui.QColor(self.mbcolor))

       #setup the lexer dictionary. This makes setting the lexer easy when a file is loaded
       self.lexer = {'.py': QsciLexerPython(), '.json': QsciLexerJavaScript(), '.c': QsciLexerCPP(), '.rb': QsciLexerRuby(), '.sh': QsciLexerBash(), '': QsciLexerMakefile(), '.sql': QsciLexerSQL(), '.cpp': QsciLexerCPP(), '.h': QsciLexerCPP(), '.pl': QsciLexerPerl(),'.html': QsciLexerHTML(),'.css': QsciLexerCSS(), '.less': QsciLexerCSS() ,'.js': QsciLexerJavaScript(), '.coffee' : QsciLexerJavaScript(),'.lua': QsciLexerLua(),'.tex': QsciLexerTeX(), '.txt': QsciLexerTeX(), '.cfg': QsciLexerTeX(), '.php': QsciLexerHTML(), '.xml': QsciLexerXML(), '.md':QsciLexerTeX(), '.pm':QsciLexerPerl()}
       self.editor.setLexer(self.lexer[self.defaultLexer])

       self.filetypes = '*.py *.json *.c *.rb *.sh *.sql *.cpp *.h *.pl *.pm *.html *.css *.less *.js *.coffee *.lua *.tex *.txt *.md *.cfg *.php *.xml'

       fileBox = QtGui.QHBoxLayout()
       mainLayout.addLayout(fileBox, 0)

       mainLayout.addWidget(self.editor, 200)

       self.CurrentfileName = ''

   def openFile(self):
      self.fn = QtGui.QFileDialog.getOpenFileName(self, 'Open file',  os.getenv("HOME") , self.filetypes)
      if self.fn.isEmpty():
          return
      self.fileName = str(self.fn)
      try:
          self.f = open(self.fileName,'r').read()
          self.editor.setText(self.f)
      except:
          return 0
      self.CurrentfileName = self.fileName
      self.extension = os.path.splitext(self.fileName)[1]
      self.editor.setLexer(self.lexer[self.extension])

   def saveAs(self):
      self.fn = QtGui.QFileDialog.getSaveFileName(self, 'Save File', os.getenv("HOME"), self.filetypes)
      self.CurrentfileName = self.fn
      try:
          self.f = open(str(self.fn),'w+r')
      except:
          return 0
      self.f.write(str(self.editor.text()))
      self.f.close()
      return 1

   def getTitle(self):
      return self.CurrentfileName

   def getFile(self):
      self.file =self.CurrentfileName.split('/')
      return self.file[len(self.file)-1]

   def getFileType(self):
      self.extension = os.path.splitext(self.CurrentfileName)
      return self.extension[len(self.extension)-1]

   def redo(self):
      self.editor.redo()

   def undo(self):
      self.editor.undo()

   def cut(self):
      self.editor.cut()

   def copy(self):
      self.editor.copy()

   def paste(self):
      self.editor.paste()

   def selectAll(self):
      self.editor.selectAll()

   def save(self):
      if self.CurrentfileName=='':
	      self.saveAs()
      else:
	      try:
                   self.f = open(self.CurrentfileName,'w+r')
              except:
                   return 0
              self.f.write(str(self.editor.text()))
              self.f.close()
              return 1

   def closeEvent(self):
      if (self.editor.isModified() == True):
          ret = QtGui.QMessageBox.warning(self, "PyTe",
                          "The Code has been modified.\n"
                          "Do you want to save your changes?",
                          QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
                          QtGui.QMessageBox.Cancel)
          if ret == QtGui.QMessageBox.Save:
              if self.CurrentfileName=="":
                 return self.saveAs()
              else:
                 return self.save()
          elif ret == QtGui.QMessageBox.Cancel:
              return 0
          elif ret == QtGui.QMessageBox.Discard:
              return 1
          else:
              return 1
      else:
          return 1
