"""
Created on Thu Oct  5 14:58:00 2017

@author: Karim
"""

#controller, MVC
# -*- coding: utf-8 -*-

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QLabel, QWidget, QPushButton, QScrollArea, QGridLayout, QListWidget, QVBoxLayout, QLineEdit
from PyQt5.QtGui import *
from PyQt5.QtCore import QSize, pyqtSignal, QSignalMapper
from PyQt5 import QtCore
from math import ceil
from urllib.request import Request, urlopen
import ClasseSerie
from Search import searchSeries
import os
from newwindow import *


class MyWindow(QMainWindow):
    def __init__(self,n_display, series_list, nameWindow):
        super().__init__()
        self.nDisplay = n_display
        self.seriesList = series_list
        self.UI = uic.loadUi('main.ui', self)
        self.showMaximized()
        self.horizontalLayoutList = []
        self.name = nameWindow
        # self.mainWidget = QWidget()
        # self.gridLayout = QGridLayout()
        # self.mainWidget.setLayout(self.gridLayout)
        # self.scrollArea = QScrollArea()
        # self.scrollArea.setWidget(self.mainWidget)
        # self.setCentralWidget(self.scrollArea)

        #Name of the window
        self.textLabel = QLabel(nameWindow)
        self.textLabel.setText(nameWindow)
        self.textLabel.setTextFormat(QtCore.Qt.RichText)
        self.textLabel.setText("<span style=' font-size:16pt; font-weight:600; color:#aa0000;'>"+nameWindow+"</span>")
        self.UI.horizontalLayout.addWidget(self.textLabel)

        #Add research bar
        self.searchWidget = QLineEdit()
        self.searchWidget.setMaximumSize(100,100)
        #self.searchWidget.setAcceptRichText(True)
        self.searchWidget.returnPressed.connect(self.slot_research)
        self.UI.horizontalLayout.addWidget(self.searchWidget)

        #Add favourites list
        self.favouritesWidget = QListWidget()
        self.UI.horizontalLayout_2.addWidget(self.favouritesWidget)

        #Load favourites list
        self.favouritesIDList = []
        fileName = "favoris"
        if os.path.exists(fileName):
            with open(fileName, "rb") as favFile:
                depickler = pickle.Unpickler(favFile)
                self.favList = depickler.load()
                for i in range(len(self.favList)):
                    favItem = QString(self.favList[i].name)
                    self.favouritesWidget.addItem(favItem)

        #Add ok button
        self.okResearch = QPushButton("Search")
        self.okResearch.setFixedSize(100,40)
        self.okResearch.pressed.connect(self.slot_research)
        self.UI.horizontalLayout.addWidget(self.okResearch)

        self.sigMapper = QSignalMapper(self)
        self.sigMapper.mapped.connect(self.slot_add_to_favourites)

        self.numberHorizontalLayout = ceil(n_display/5)
        self.positions = [(i+1,j) for i in range(self.numberHorizontalLayout) for j in range(5)]
        self.widgetlist = []
        i=0
        for i in range(n_display):
            newWidget = MainWidget(i, self.seriesList[i])
            self.widgetlist += [newWidget]
            self.UI.gridLayout.addWidget(newWidget, *self.positions[i])
            i+=1
            self.sigMapper.setMapping(newWidget.favButton, newWidget.id)
            newWidget.favButton.clicked.connect(self.sigMapper.map)

    def slot_add_to_favourites(self,id):
        self.favouritesIDList += [id]
        print("id = ", id)

    def slot_research(self):
        self.searchText = self.searchWidget.text()
        print(self.searchText)
        for i in reversed(range(self.UI.gridLayout.count())):
            self.UI.gridLayout.itemAt(i).widget().setParent(None)
        searchSeries(self.searchText, self.seriesList)
        for i in range(self.nDisplay):
            print(self.seriesList[i].name)
            newWidget = MainWidget(i, self.seriesList[i])
            self.UI.gridLayout.addWidget(newWidget, *self.positions[i])

class MainWidget(QFrame):
    def __init__(self, id, serie, parent = None):
        super(MainWidget, self).__init__(parent)
#        self.UI = uic.loadUi('mainwidget.ui', self)
        self.ser = serie
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.id = serie.id
        self.img = QLabel(self)
        self.img.setScaledContents(True)
        self.pixmap = QPixmap()
        data = urlopen(serie.image).read()
        self.pixmap.loadFromData(data)
        self.img = self.img.setPixmap(self.pixmap)

        self.text = QLabel(serie.name)
        self.text.setText(serie.name)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.img)
        self.favButton = QPushButton("Add to favorite")
        self.serieButton = QPushButton("More Info")
        self.serieButton.clicked.connect(self.slot_open_new_window)
        self.layout.addWidget(self.favButton)
        self.layout.addWidget(self.serieButton)
#        self.UI.verticalLayout.addWidget(self.img)
#        self.UI.text.setPlainText(serie.name)
#        self.size = QSize(100,100)
        self.setMaximumSize(100,100)

    def slot_open_new_window(self):
        self.newWindow = NewWindow(self.ser, self)
        self.newWindow.exec_()
