#!/usr/bin/python
import sys, os
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui, Qsci
from PyQt4.Qsci import QsciScintilla, QsciScintillaBase, QsciLexerPython, QsciLexerPerl, QsciLexerRuby, QsciLexerHTML, QsciLexerCSS, QsciLexerJavaScript, QsciLexerLua, QsciLexerPython, QsciLexerMakefile, QsciLexerCPP, QsciLexerBash, QsciLexerTeX, QsciLexerSQL

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

       self.font = QtGui.QFont()
       self.font.setFamily("Consolas")
       self.font.setFixedPitch(True)
       self.font.setPointSize(10)
       self.fm = QtGui.QFontMetrics(self.font)
       self.editor.setFont(self.font)
       self.editor.setMarginsFont(self.font)
       self.editor.setMarginWidth(0, self.fm.width( "0000" ))

       self.editor.setMarginLineNumbers(0, True)
       self.editor.setUtf8(True)
       self.editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)
       self.editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)
       self.editor.setCaretLineVisible(True)
       self.editor.setCaretLineBackgroundColor(QtGui.QColor('#bfbfbf'))
       self.editor.setMarginsBackgroundColor(QtGui.QColor('#3e3e3e'))
       self.editor.setMarginsForegroundColor(QtGui.QColor('#aaff00'))
       self.editor.setFoldMarginColors(QtGui.QColor('#ff0000'),QtGui.QColor('#000000'))

       #setup the lexer dictionary. This makes setting the lexer easy when a file is loaded
       self.lexer = {'.py': QsciLexerPython(), '.c': QsciLexerCPP(), '.rb': QsciLexerRuby(), '.sh': QsciLexerBash(), '': QsciLexerMakefile(), '.sql': QsciLexerSQL(), '.cpp': QsciLexerCPP(), '.h': QsciLexerCPP(), '.pl': QsciLexerPerl(),
'.html': QsciLexerHTML(),'.css': QsciLexerCSS(),'.js': QsciLexerJavaScript(),'.lua': QsciLexerLua(),'.tex': QsciLexerTeX(), '.txt': QsciLexerTeX()}
       self.editor.setLexer(self.lexer['.py'])

       fileBox = QtGui.QHBoxLayout()
       mainLayout.addLayout(fileBox, 0)



       mainLayout.addWidget(self.editor, 200)

       self.CurrentfileName = ''

   def openFile(self):
      self.fn = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home', '')
      if self.fn.isEmpty():
          return
      self.fileName = str(self.fn)
      try:
          self.f = open(self.fileName,'r').read()
          self.editor.setText(self.f)
      except:
          return
      self.CurrentfileName = self.fileName
      self.extension = os.path.splitext(self.fileName)[1]
      self.editor.setLexer(self.lexer[self.extension])
      
   def openArg(self, FileName):
      self.f = open(FileName,'r').read()
      self.editor.setText(self.f)
      self.CurrentfileName = FileName
      self.extension = os.path.splitext(FileName)[1]
      self.editor.setLexer(self.lexer[self.extension])

   def saveAs(self):
      self.fn = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '')
      self.CurrentfileName = self.fn
      try:
          self.f = open(str(self.fn),'w+r')
      except:
          return
      self.f.write(str(self.editor.text()))
      self.f.close()

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
      try:
          self.f = open(self.CurrentfileName,'w+r')
      except:
          return
      self.f.write(str(self.editor.text()))
      self.f.close()

   def closeEvent(self):
      if (self.editor.isModified() == True):
          ret = QtGui.QMessageBox.warning(self, "PyTe",
                          "The Code has been modified.\n"
                          "Do you want to save your changes?",
                          QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
                          QtGui.QMessageBox.Cancel)
          if ret == QtGui.QMessageBox.Save:
              if self.CurrentfileName=="":
                 self.fn = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '')
                 try:
                     self.f = open(str(self.fn),'w+r')
                 except:
                     return 0
                 self.f.write(str(self.editor.text()))
                 self.f.close()
                 return 1
              else:
                 try:
                     self.f = open(self.CurrentfileName,'w+r')
                 except:
                     return 0
                 self.f.write(str(self.editor.text()))
                 self.f.close()
                 return 1
          elif ret == QtGui.QMessageBox.Cancel:
              return 0
          elif ret == QtGui.QMessageBox.Discard:
              return 1
          else:
              return 1
      else:
          return 1
