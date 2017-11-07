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
        self.searchWidget = QLineEdit()
        self.searchWidget.setMaximumSize(100,100)
        #self.searchWidget.setAcceptRichText(True)
        self.searchWidget.returnPressed.connect(self.slot_research)
        self.__UI.horizontalLayout.addWidget(self.searchWidget)

        #Add favourites list
        self.favouritesWidget = QListWidget()
        self.favouritesWidget.setMaximumWidth(220)
        self.favLayout = QVBoxLayout()
        self.__UI.horizontalLayout_2.addLayout(self.favLayout)
        self.favouritesText = QLabel("Favourites")
        self.favouritesText.setText("<span style=' font-size:16pt; font-weight:600; color:#aa0000;'> Favourites </span>")
        self.favLayout.addWidget(self.favouritesText)
        self.favLayout.addWidget(self.favouritesWidget)
        self.favButtonsLayout = QHBoxLayout()
        self.favLayout.addLayout(self.favButtonsLayout)
        self.moreInfoButton = QPushButton("More Info")
        self.favButtonsLayout.addWidget(self.moreInfoButton)
        self.moreInfoButton.clicked.connect(self.slot_open_serie_window)
        self.removeFavButton = QPushButton("Remove Favourite")
        self.favButtonsLayout.addWidget(self.removeFavButton)
        self.removeFavButton.clicked.connect(self.slot_remove_favourite)

        #Load favourites list
        self.favouritesIDList = []
        self.favouritesSeries = []

        self.fileName = "favoris"
        if (os.path.exists(self.fileName)) and (os.path.getsize(self.fileName) > 0):
            with open(self.fileName, "rb") as favFile:
                depickler = pickle.Unpickler(favFile)
                self.favouritesSeries = depickler.load()
                for i in range(len(self.favouritesSeries)):
                    favItem = self.favouritesSeries[i].name
                    self.favouritesWidget.addItem(favItem)
                    self.favouritesIDList += [self.favouritesSeries[i].id]

        #Add ok button
        self.okResearch = QPushButton("Search")
        self.okResearch.setFixedSize(100,40)
        self.okResearch.pressed.connect(self.slot_research)
        self.__UI.horizontalLayout.addWidget(self.okResearch)

        self.sigMapper = QSignalMapper(self)
        self.sigMapper.mapped.connect(self.slot_add_to_favourites)

        self.numberHorizontalLayout = ceil(n_display/5)
        self.positions = [(i+1,j) for i in range(self.numberHorizontalLayout) for j in range(5)]
        self.widgetlist = []
        i=0
        for i in range(n_display):
            newWidget = MainWidget(i, self.seriesList[i])
            self.widgetlist += [newWidget]
            self.__gridLayout.addWidget(newWidget, *self.positions[i])
            i+=1
            self.sigMapper.setMapping(newWidget.favButton, newWidget.id)
            newWidget.favButton.clicked.connect(self.sigMapper.map)

    def _get_seriesList(self):
        return self.__seriesList

    def _set_seriesList(self,newSeriesList):
        self.__seriesList = newSeriesList

    seriesList = property(_get_seriesList, _set_seriesList)

        #Fonts
        # print(QFontDatabase().families())
        # print(len(QFontDatabase().families()))

    def slot_add_to_favourites(self,id):
        if (id not in self.favouritesIDList):
            self.favouritesIDList += [id]
            serie = searchSerie(id)
            nm = serie.name
            self.favouritesSeries += [serie]
            self.favouritesWidget.addItem(nm)

            with open(self.fileName, "wb") as favFile:
                pickler = pickle.Pickler(favFile)
                pickler.dump(self.favouritesSeries)

        else:
            print("Favourite already added.")

    def slot_open_serie_window(self):
        idx = self.favouritesWidget.currentRow()
        id = self.favouritesIDList[idx]
        ser = self.favouritesSeries[idx]
        self.newWindow = NewWindow(ser, self)
        self.newWindow.exec_()

    def slot_research(self):
        self.searchText = self.searchWidget.text()
        for i in reversed(range(self.__UI.gridLayout.count())):
            self.__UI.gridLayout.itemAt(i).widget().setParent(None)
        searchSeries(self.searchText, self.seriesList)
        for i in range(len(self.seriesList)):
            newWidget = MainWidget(i, self.seriesList[i])
            self.__UI.gridLayout.addWidget(newWidget, *self.positions[i])
            self.sigMapper.setMapping(newWidget.favButton, newWidget.id)
            newWidget.favButton.clicked.connect(self.sigMapper.map)

    def slot_remove_favourite(self):
        idx = self.favouritesWidget.currentRow()
        del self.favouritesSeries[idx]
        del self.favouritesIDList[idx]
        self.favouritesWidget.takeItem(idx)

        with open(self.fileName, "wb") as favFile:
            pickler = pickle.Pickler(favFile)
            pickler.dump(self.favouritesSeries)

class MainWidget(QFrame):
    def __init__(self, id, serie, parent = None):
        super(MainWidget, self).__init__(parent)
#        self.UI = uic.loadUi('mainwidget.ui', self)

        self.setFrameStyle(1)
        self.setLineWidth(3)
        self.setObjectName("mainWidget")
        self.setStyleSheet("#mainWidget{border: 3px solid white;}")

        #Attributes
        self.ser = serie
        self.id = serie.id
        
        #Size
        self.sizePolicy = QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.QSizePolicy = self.sizePolicy
        #self.setMinimumSize(100,170)
        self.setFixedSize(300,400)

        #Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        #Text : display serie name
        labelString = serie.name
        #Fonts
        #labelString = str(id) + ". " + QFontDatabase().families()[id]
        self.text = QLabel(labelString)
#        self.UI.text.setText(serie.name)
#        self.UI.text.setTextFormat(QtCore.Qt.RichText)

        self.text.setText("<span style=' font-size:16pt; font-weight:600; color:#FFFFFF;'>"+labelString+"</span>")
        #Fonts
        #self.text.setFont(QFont(QFontDatabase().families()[id], 20))
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.text)


        
        #Image : display serie image
        self.frame = QFrame()
        self.imgLayout = QVBoxLayout(self.frame)

        self.img = QLabel(self)
        #self.img.setMinimumSize(100,100)
        self.img.setScaledContents(True)
        self.pixmap = QPixmap()
        data = urlopen(serie.image).read()
        self.pixmap.loadFromData(data)
        self.img.setPixmap(self.pixmap)
        self.img.setAlignment(QtCore.Qt.AlignCenter)
        self.imgLayout.addWidget(self.img)
        self.layout.addWidget(self.frame)

#        spacer1 = QSpacerItem(80,80,QSizePolicy.Maximum,QSizePolicy.Maximum)
#        self.layout.addItem(spacer1)
        self.layout.addWidget(self.img)
        self.favButton = QPushButton("Add to favorite")
        self.serieButton = QPushButton("More Info")
        self.serieButton.clicked.connect(self.slot_open_new_window)
        self.layout.addWidget(self.favButton)
        self.layout.addWidget(self.serieButton)
#        self.setMaximumHeight(200)

    def slot_open_new_window(self):
        self.newWindow = NewWindow(self.ser, self)
        self.newWindow.exec_()
