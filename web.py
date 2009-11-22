        self.weblist = []
        self.adresslist = []
        self.webbblist = []
        self.webnblist = []
        self.webboxlist = []
        self.progresslist = []
        self.urllist = []

        newweb = QtGui.QAction(QtGui.QIcon('icons/new.png'), 'New Web', self)
        newweb.setShortcut('Ctrl+Shift+N')
        newweb.setStatusTip('New Web')
        self.connect(newweb, QtCore.SIGNAL('triggered()'), self.newweb)

        backw = QtGui.QAction(QtGui.QIcon('icons/back.png'), 'Back', self)
        backw.setStatusTip('Back')
        self.connect(backw, QtCore.SIGNAL('triggered()'), self.backw)

        nextw = QtGui.QAction(QtGui.QIcon('icons/next.png'), 'Forward', self)
        nextw.setStatusTip('Forward')
        self.connect(nextw, QtCore.SIGNAL('triggered()'), self.nextw)

        self.adress = len(self.adresslist)
        self.adress = QtGui.QLineEdit()
        self.adresslist.append(self.adress)

        self.webbackb = len(self.webbblist)
        self.webbackb = QtGui.QPushButton(QtGui.QIcon('icons/back.png'),"")
        self.webbblist.append(self.webbackb)

        self.webnextb = len(self.webnblist)
        self.webnextb = QtGui.QPushButton(QtGui.QIcon('icons/next.png'), "")
        self.webnblist.append(self.webnextb)

        self.buttonBox = len(self.webboxlist)
        self.buttonBox = QtGui.QHBoxLayout()
        self.webboxlist.append(self.buttonBox)

        self.progress = len(self.progresslist)
        self.progress = QtGui.QProgressBar()
        self.progresslist.append(self.progress)

        self.web = len(self.weblist)
        self.web = QWebView()
        self.weblist.append(self.web)

        self.connect(self.webbackb, QtCore.SIGNAL("clicked()"), self.backw)
        self.connect(self.webnextb, QtCore.SIGNAL("clicked()"), self.nextw)

        self.buttonBox.addWidget(self.webbackb)
        self.buttonBox.addWidget(self.webnextb)
        self.buttonBox.addWidget(self.adress)
        self.buttonBox.addWidget(self.progress)

        self.urld = len(self.urllist)
        self.urld = "http://google.com"
        self.urllist.append(self.urld)
        QtCore.QObject.connect(self.web,QtCore.SIGNAL("linkClicked (const QUrl&)"), self.link_clicked_web)
        QtCore.QObject.connect(self.adress,QtCore.SIGNAL("returnPressed()"), self.url_changed)
        QtCore.QObject.connect(self.web,QtCore.SIGNAL("loadProgress (int)"), self.load_progress)
        self.adress.setText(self.urld)
	self.web.setUrl(QtCore.QUrl(self.urld))

        self.tab = QtGui.QWidget()
        self.p = QtGui.QVBoxLayout(self.tab)
        self.tab_widget.addTab(self.tab, QtGui.QIcon('icons/tex.png'), "Web")
        self.p.addLayout(self.buttonBox)
        self.p.addWidget(self.web)

        self.tablist.append(self.tab)
        self.plist.append(self.p)


    def newweb(self):
        self.adress = len(self.adresslist)
        self.adress = QtGui.QLineEdit()
        self.adresslist.append(self.adress)

        self.webbackb = len(self.webbblist)
        self.webbackb = QtGui.QPushButton(QtGui.QIcon('icons/back.png'),"")
        self.webbblist.append(self.webbackb)

        self.webnextb = len(self.webnblist)
        self.webnextb = QtGui.QPushButton(QtGui.QIcon('icons/next.png'), "")
        self.webnblist.append(self.webnextb)

        self.buttonBox = len(self.webboxlist)
        self.buttonBox = QtGui.QHBoxLayout()
        self.webboxlist.append(self.buttonBox)

        self.progress = len(self.progresslist)
        self.progress = QtGui.QProgressBar()
        self.progresslist.append(self.progress)

        self.web = len(self.weblist)
        self.web = QWebView()
        self.weblist.append(self.web)

        self.connect(self.webbackb, QtCore.SIGNAL("clicked()"), self.backw)
        self.connect(self.webnextb, QtCore.SIGNAL("clicked()"), self.nextw)

        self.buttonBox.addWidget(self.webbackb)
        self.buttonBox.addWidget(self.webnextb)
        self.buttonBox.addWidget(self.adress)
        self.buttonBox.addWidget(self.progress)

        self.urld = len(self.urllist)
        self.urld = "http://google.com"
        self.urllist.append(self.urld)
        QtCore.QObject.connect(self.web,QtCore.SIGNAL("linkClicked (const QUrl&)"), self.link_clicked_web)
        QtCore.QObject.connect(self.adress,QtCore.SIGNAL("returnPressed()"), self.url_changed)
        QtCore.QObject.connect(self.web,QtCore.SIGNAL("loadProgress (int)"), self.load_progress)
        self.adress.setText(self.urld)
	self.web.setUrl(QtCore.QUrl(self.urld))

        self.tab = QtGui.QWidget()
        self.p = QtGui.QVBoxLayout(self.tab)
        self.tab_widget.addTab(self.tab, QtGui.QIcon('icons/tex.png'), "Web")
        self.p.addLayout(self.buttonBox)
        self.p.addWidget(self.web)

        self.tablist.append(self.tab)
        self.plist.append(self.p)

    def load_progress(self, load):
        self.codeli = self.tab_widget.currentIndex()
        self.progress = self.progresslist[self.codeli]
        self.progress.setValue(load)

    def url_changed(self):
        self.codeli = self.tab_widget.currentIndex()
        self.adress = self.adresslist[self.codeli]
        self.web = self.weblist[self.codeli]
        url = self.adress.text()
        self.web.setUrl(QtCore.QUrl(url))

    def backw(self):
        self.codeli = self.tab_widget.currentIndex()
        self.web = self.weblist[self.codeli]
        page = self.web.page()
        history = page.history()
        history.back()

    def nextw(self):
        self.codeli = self.tab_widget.currentIndex()
        self.web = self.weblist[self.codeli]
        page = self.web.page()
        history = page.history()
        history.forward()

    def link_clicked_web(self, url):
        self.codeli = self.tab_widget.currentIndex()
        self.web = self.weblist[self.codeli]
        self.adress = self.adresslist[self.codeli]
        self.web.setUrl(QtCore.QUrl(url))
        self.adress.setText(url)
