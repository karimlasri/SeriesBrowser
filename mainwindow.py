import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QLabel, QWidget, QPushButton, QScrollArea, QGridLayout, QListWidget, QVBoxLayout, QLineEdit
from PyQt5.QtGui import *
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5 import QtCore
from math import ceil
from urllib.request import Request, urlopen
import ClasseSerie
from Search import search
import os
from newwindow import *

#controller, MVC
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 14:58:00 2017

@author: Karim
"""


class MyWindow(QMainWindow):
    def __init__(self,n_display, series_list, nameWindow, typeWindow):
        super().__init__()
        self.nDisplay = n_display
        self.seriesList = series_list
        self.UI = uic.loadUi('main.ui', self)
        self.showMaximized()
        self.horizontalLayoutList = []
        self.name = nameWindow
        self.type = typeWindow
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

        # TODO : Changer serieWidget
        if typeWindow == "serie":
            serieWidget = MainWidget(1, series_list[1])
            self.UI.gridLayout.addWidget(serieWidget)
            
        self.numberHorizontalLayout = ceil(n_display/5)
        self.positions = [(i+1,j) for i in range(self.numberHorizontalLayout) for j in range(5)]
        self.widgetlist = []
        i=0
        for i in range(n_display):
                newWidget = MainWidget(i, self.seriesList[i])
                self.widgetlist += [newWidget]
                self.UI.gridLayout.addWidget(newWidget, *self.positions[i])
                i+=1

    def slot_research(self):
        self.searchText = self.searchWidget.text()
        print(self.searchText)
        for i in reversed(range(self.UI.gridLayout.count())):
            self.UI.gridLayout.itemAt(i).widget().setParent(None)
        search(self.searchText, self.seriesList)
        for i in range(self.nDisplay):
            print(self.seriesList[i].name)
            newWidget = MainWidget(i, self.seriesList[i])
            self.UI.gridLayout.addWidget(newWidget, *self.positions[i])

        #     self.UI.gridLayout.addWidget(newWidget, *positions[i])

class MainWidget(QFrame):
    def __init__(self, id, serie, parent = None):
        super(MainWidget, self).__init__(parent)
#        self.UI = uic.loadUi('mainwidget.ui', self)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.id = serie.id
        self.img = QLabel(self)
        self.img.setScaledContents(True)
        self.pixmap = QPixmap()
        data = urlopen(serie.image).read()
        self.pixmap.loadFromData(data)
        self.img = self.img.setPixmap(self.pixmap)
        self.layout.addWidget(self.img)
        self.text = QLabel(serie.name)
        self.text.setText(serie.name)
        self.layout.addWidget(self.text)
        self.favButton = QPushButton("Add to favorite")
        self.favButton.clicked.connect(self.open_new_window)
        self.layout.addWidget(self.favButton)
#        self.UI.verticalLayout.addWidget(self.img)
#        self.UI.text.setPlainText(serie.name)
#        self.size = QSize(100,100)
        self.setMaximumSize(100,100)

    def open_new_window(self):
        self.newWindow = NewWindow(self)
        self.newWindow.exec_()
