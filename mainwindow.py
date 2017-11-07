"""
Created on Thu Oct  5 14:58:00 2017

@author: Karim
"""

#controller, MVC
# -*- coding: utf-8 -*-

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QSpacerItem, QSizePolicy, QLabel, QWidget, QPushButton, QScrollArea, QGridLayout, QListWidget, QVBoxLayout, QLineEdit, QHBoxLayout
from PyQt5.QtGui import *
from PyQt5.QtCore import QSize, pyqtSignal, QSignalMapper
from PyQt5 import QtCore
from math import ceil
from urllib.request import Request, urlopen
import ClasseSerie
from Search import searchSeries, searchSerie
import os
from newwindow import *
import pickle

class MyWindow(QMainWindow):
    def __init__(self,n_display, series_list, nameWindow):
        super().__init__()
        self.__nDisplay = n_display
        self.__seriesList = series_list
        self.__UI = uic.loadUi('main.ui', self)
        self.showMaximized()

        #Name of the window
        self.__textLabel = QLabel(nameWindow)
        self.__textLabel.setText(nameWindow)
        self.__textLabel.setTextFormat(QtCore.Qt.RichText)
        self.__textLabel.setText("<span style=' font-size:16pt; font-weight:600; color:#aa0000;'>"+nameWindow+"</span>")
        self.__UI.horizontalLayout.addWidget(self.__textLabel)
        
        #Scroll area
        self.__serieWind = QWidget()
        self.__scrollArea = QScrollArea()
        self.__scrollArea.setWidgetResizable(True)
        self.__scrollArea.setWidget(self.__serieWind)
        self.__gridLayout = QGridLayout()
        self.__serieWind.setObjectName("serieWind")
        self.setStyleSheet("#serieWind{background-color: black;}")
        self.__serieWind.setLayout(self.__gridLayout)
        self.__UI.horizontalLayout_2.addWidget(self.__scrollArea)
        self.__scrollArea.verticalScrollBar().setStyleSheet("QScrollBar:vertical {"              
        "    border: 1px solid #999999;"
        "    background:white;"
        "    width:10px;    "
        "    margin: 0px 0px 0px 0px;"
        "}"
        "QScrollBar::handle:vertical {"
        "    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,"
        "    stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130), stop:1 rgb(32, 47, 130));"
        "    min-height: 0px;"
        "}"
        "QScrollBar::add-line:vertical {"
        "    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,"
        "    stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));"
        "    height: 0px;"
        "    subcontrol-position: bottom;"
        "    subcontrol-origin: margin;"
        "}"
        "QScrollBar::sub-line:vertical {"
        "    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,"
        "    stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));"
        "    height: 0 px;"
        "    subcontrol-position: top;"
        "    subcontrol-origin: margin;"
        "}")

        #Add research bar
        self.__searchWidget = QLineEdit()
        self.__searchWidget.setMaximumSize(100,100)
        #self.searchWidget.setAcceptRichText(True)
        self.__searchWidget.returnPressed.connect(self.slot_research)
        self.__UI.horizontalLayout.addWidget(self.__searchWidget)

        #Add favourites list
        self.__favouritesWidget = QListWidget()
        self.__favouritesWidget.setMaximumWidth(220)
        self.__favLayout = QVBoxLayout()
        self.__UI.horizontalLayout_2.addLayout(self.__favLayout)
        self.__favouritesTitle = QLabel("Favourites")
        self.__favouritesTitle.setText("<span style=' font-size:16pt; font-weight:600; color:#aa0000;'> Favourites </span>")
        self.__favLayout.addWidget(self.__favouritesTitle)
        self.__favLayout.addWidget(self.__favouritesWidget)
        self.__favButtonsLayout = QHBoxLayout()
        self.__favLayout.addLayout(self.__favButtonsLayout)
        self.__favMoreInfoButton = QPushButton("More Info")
        self.__favButtonsLayout.addWidget(self.__favMoreInfoButton)
        self.__favMoreInfoButton.clicked.connect(self.slot_open_serie_window)
        self.__removeFavButton = QPushButton("Remove Favourite")
        self.__favButtonsLayout.addWidget(self.__removeFavButton)
        self.__removeFavButton.clicked.connect(self.slot_remove_favourite)

        #Load favourites list
        self.__favouritesIDList = []
        self.__favouriteSeries = []

        self.__fileName = "favoris"
        if (os.path.exists(self.__fileName)) and (os.path.getsize(self.__fileName) > 0):
            with open(self.__fileName, "rb") as favFile:
                depickler = pickle.Unpickler(favFile)
                self.__favouriteSeries = depickler.load()
                for i in range(len(self.__favouriteSeries)):
                    favItem = self.__favouriteSeries[i].name
                    self.__favouritesWidget.addItem(favItem)
                    self.__favouritesIDList += [self.__favouriteSeries[i].id]

        #Add research button
        self.__researchButton = QPushButton("Search")
        self.__researchButton.setFixedSize(100,40)
        self.__researchButton.pressed.connect(self.slot_research)
        self.__UI.horizontalLayout.addWidget(self.__researchButton)

        self.__sigMapper = QSignalMapper(self)
        self.__sigMapper.mapped.connect(self.slot_add_to_favourites)

        self.__numberSeriesWidgetLines = ceil(n_display/5)
        self.__positions = [(i+1,j) for i in range(self.__numberSeriesWidgetLines) for j in range(5)]
        self.__seriesWidgetList = []
        i=0
        for i in range(n_display):
            currentWidget = MainWidget(i, self.__seriesList[i])
            self.__seriesWidgetList += [currentWidget]
            self.__gridLayout.addWidget(currentWidget, *self.__positions[i])
            i+=1
            self.__sigMapper.setMapping(currentWidget.favButton, currentWidget.id)
            currentWidget.favButton.clicked.connect(self.__sigMapper.map)

    @property
    def seriesList(self):
        return self.__seriesList

    @seriesList.setter
    def seriesList(self,newSeriesList):
        self.__seriesList = newSeriesList


        #Fonts
        # print(QFontDatabase().families())
        # print(len(QFontDatabase().families()))

    def slot_add_to_favourites(self,id):
        if (id not in self.__favouritesIDList):
            self.__favouritesIDList += [id]
            serie = searchSerie(id)
            nm = serie.name
            self.__favouriteSeries += [serie]
            self.__favouritesWidget.addItem(nm)

            with open(self.__fileName, "wb") as favFile:
                pickler = pickle.Pickler(favFile)
                pickler.dump(self.__favouriteSeries)

        else:
            print("Favourite already added.")

    def slot_open_serie_window(self):
        idx = self.__favouritesWidget.currentRow()
        id = self.__favouritesIDList[idx]
        ser = self.__favouriteSeries[idx]
        self.newWindow = NewWindow(ser, self)
        self.newWindow.exec_()

    def slot_research(self):
        self.__searchText = self.__searchWidget.text()
        for i in reversed(range(self.__gridLayout.count())):
            self.__gridLayout.itemAt(i).widget().setParent(None)
        searchSeries(self.__searchText, self.__seriesList)
        for i in range(len(self.__seriesList)):
            currentWidget = MainWidget(i, self.__seriesList[i])
            self.__gridLayout.addWidget(currentWidget, *self.__positions[i])
            self.__sigMapper.setMapping(currentWidget.favButton, currentWidget.id)
            currentWidget.favButton.clicked.connect(self.__sigMapper.map)

    def slot_remove_favourite(self):
        idx = self.__favouritesWidget.currentRow()
        del self.__favouriteSeries[idx]
        del self.__favouritesIDList[idx]
        self.__favouritesWidget.takeItem(idx)

        with open(self.__fileName, "wb") as favFile:
            pickler = pickle.Pickler(favFile)
            pickler.dump(self.__favouriteSeries)

class MainWidget(QFrame):
    def __init__(self, id, serie, parent = None):
        super(MainWidget, self).__init__(parent)
#        self.UI = uic.loadUi('mainwidget.ui', self)

        self.setFrameStyle(1)
        self.setLineWidth(3)
        self.setObjectName("mainWidget")
        self.setStyleSheet("#mainWidget{border: 3px solid white;}")

        #Attributes
        self.__ser = serie
        self.__id = serie.id
        
        #Size
        self.__sizePolicy = QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.__QSizePolicy = self.__sizePolicy
        self.setFixedSize(300,400)

        #Layout
        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)

        #Text : display serie name
        labelString = serie.name
        #Fonts
        #labelString = str(id) + ". " + QFontDatabase().families()[id]
        self.__textLabel = QLabel(labelString)
#        self.UI.text.setText(serie.name)
#        self.UI.text.setTextFormat(QtCore.Qt.RichText)

        self.__textLabel.setText("<span style=' font-size:16pt; font-weight:600; color:#FFFFFF;'>"+labelString+"</span>")
        #Fonts
        #self.__text.setFont(QFont(QFontDatabase().families()[id], 20))
        self.__textLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.__layout.addWidget(self.__textLabel)


        
        #Image : display serie image
        self.__frame = QFrame()
        self.__imgLayout = QVBoxLayout(self.__frame)

        self.__img = QLabel(self)
        #self.__img.setMinimumSize(100,100)
        self.__img.setScaledContents(True)
        self.pixmap = QPixmap()
        data = urlopen(serie.image).read()
        self.pixmap.loadFromData(data)
        self.__img.setPixmap(self.pixmap)
        self.__img.setAlignment(QtCore.Qt.AlignCenter)
        self.__imgLayout.addWidget(self.__img)
        self.__layout.addWidget(self.__frame)

#        spacer1 = QSpacerItem(80,80,QSizePolicy.Maximum,QSizePolicy.Maximum)
#        self.__layout.addItem(spacer1)
        self.__layout.addWidget(self.__img)
        self.__favButton = QPushButton("Add to favorite")
        self.__serieButton = QPushButton("More Info")
        self.__serieButton.clicked.connect(self.slot_open_new_window)
        self.__layout.addWidget(self.favButton)
        self.__layout.addWidget(self.__serieButton)
#        self.setMaximumHeight(200)

    @property
    def favButton(self):
        return self.__favButton

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self,newid):
        self.__id = newid

    def slot_open_new_window(self):
        self.__newWindow = NewWindow(self.__ser, self)
        self.__newWindow.exec_()
