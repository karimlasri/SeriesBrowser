"""
Created on Thu Oct  5 14:58:00 2017

@author: Karim
"""

#controller, MVC
# -*- coding: utf-8 -*-

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QSpacerItem, QSizePolicy, QLabel, QWidget, QPushButton, QScrollArea, QGridLayout, QListWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtCore import QSize, pyqtSignal, QSignalMapper
from PyQt5 import QtCore
from math import ceil
from urllib.request import Request, urlopen
import ClasseSerie
from Search import searchSeries, searchSerie, findForthcomingSerie
import os
import datetime
from newwindow import *
import pickle
from alert import Afficher

class MyWindow(QMainWindow): #Main window of the Serie Browser


    def __init__(self,n_display, series_list, nameWindow):  #n_display : number of shows to display when prog is launched,
                                                            # series_list = list of series to be displayed and retrieved from the API,
                                                            # nameWindow = name to be displayed

        super().__init__()
        self.__nDisplay = n_display
        self.__seriesList = series_list

        # Load .ui designed on Qt
        self.__UI = uic.loadUi('main.ui', self)

        # Show window on desktop
        self.showMaximized()

        # Name of the window
        self.__textLabel = QLabel(nameWindow)
        self.__textLabel.setText(nameWindow)
        self.__textLabel.setTextFormat(QtCore.Qt.RichText)
        self.__textLabel.setText("<span style=' font-size:16pt; font-weight:600; color:#aa0000;'>"+nameWindow+"</span>")
        self.__UI.horizontalLayout.addWidget(self.__textLabel)
        
        # Define a Scroll area for serie display
        self.__serieWind = QWidget()        # Create a widget for the scroll area
        self.__scrollArea = QScrollArea()       # I Create a Scroll Area
        self.__scrollArea.setWidgetResizable(True)
        self.__scrollArea.setWidget(self.__serieWind)       # Insert the scroll area in the widget
        self.__gridLayout = QGridLayout()       # Create a grid layout for the scroll area
        self.__serieWind.setLayout(self.__gridLayout)  # Insert the grid layout in the scroll area
        self.__UI.horizontalLayout_2.addWidget(self.__scrollArea)  # Insert the scroll area in the main horizontal layout from .ui

        self.__serieWind.setObjectName("serieWind")
        self.setStyleSheet("#serieWind{background-color: black;}")      # Define color of the scroll area
        self.__scrollArea.verticalScrollBar().setStyleSheet("QScrollBar:vertical {"     # Define style of scroll area              
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

        #  Add research bar
        self.__searchWidget = QLineEdit()
        self.__searchWidget.setFixedSize(150,40)
        self.__searchWidget.returnPressed.connect(self.slot_research)       # Connect the signal return pressed to slot_research
        self.__UI.horizontalLayout.addWidget(self.__searchWidget)       # Insert research bar in layout from .ui

        #  Add research button
        self.__researchButton = QPushButton("Search")
        self.__researchButton.setFixedSize(100, 40)
        self.__researchButton.pressed.connect(self.slot_research)       # Connect the signal pressed to slot_research
        self.__UI.horizontalLayout.addWidget(self.__researchButton)     # Insert research button in layout from .ui  # Add favourites title

        # Favourites
        # Layout
        self.__favLayout = QVBoxLayout()
        self.__UI.horizontalLayout_2.addLayout(self.__favLayout)

        # Title
        self.__favouritesTitle = QLabel("Favourites")
        self.__favouritesTitle.setText(
            "<span style=' font-size:16pt; font-weight:600; color:#aa0000;'> Favourites </span>")
        self.__favLayout.addWidget(self.__favouritesTitle)

        #  Add favourites list with a QListWidget
        self.__favouritesWidget = QListWidget()
        self.__favouritesWidget.setMaximumWidth(250)
        self.__favLayout.addWidget(self.__favouritesWidget)
        self.__favButtonsLayout = QHBoxLayout()
        self.__favLayout.addLayout(self.__favButtonsLayout)

        #  Add More Info button for favourites list
        self.__favMoreInfoButton = QPushButton("More Info")
        self.__favButtonsLayout.addWidget(self.__favMoreInfoButton)
        self.__favMoreInfoButton.clicked.connect(self.slot_open_serie_window)       # Connect clicked signal of MoreInfo button to slot_open_serie_window

        #  Add Remove favourite button for favourites list
        self.__removeFavButton = QPushButton("Remove Favourite")
        self.__favButtonsLayout.addWidget(self.__removeFavButton)
        self.__removeFavButton.clicked.connect(self.slot_remove_favourite)      # Connect clicked signal to Remove button to slot_remove_favourites

        #  Magic Button
        self.__magicButton = QPushButton("MAGIC BUTTON")
        self.__magicButton.clicked.connect(self.slot_magic_add_to_favourites)
        self.__favLayout.addWidget(self.__magicButton)

        #Create and load favourites list
        self.__favouritesIDList = []        # Creation of a ID list of favourites
        self.__favouriteSeries = []         # Creation of list of favourites of class Serie

        self.__fileName = "favourites"         #Creation of a file for pickler
        if (os.path.exists(self.__fileName)) and (os.path.getsize(self.__fileName) > 0):        #Check if the file exists
            with open(self.__fileName, "rb") as favFile:
                depickler = pickle.Unpickler(favFile)
                self.__favouriteSeries = depickler.load()
                for i in range(len(self.__favouriteSeries)):        #Loop to add favourites series to favourite QWidgetList and create favouritesIDList
                    favItem = self.__favouriteSeries[i].name
                    self.__favouritesWidget.addItem(favItem)
                    self.__favouritesIDList += [self.__favouriteSeries[i].id]

        #Alert
        self.alertWindow = Afficher(self.__favouriteSeries,self)
        self.alertWindow.start()
        # self.alertWindow.quit()

        # Signal Mapper to connect slot_add_to_favourites to class MainWidget
        self.__sigMapper = QSignalMapper(self)
        self.__sigMapper.mapped.connect(self.slot_add_to_favourites)
        #self.__sigMapper.mapped.connect(self.alertWindow.slot_add_fav_and_display)


        # Display series MainWidgets on MainWindow
        self.__numberSeriesWidgetLines = ceil(n_display/5)      # 5 widgets per line maximum
        self.__positions = [(i+1,j) for i in range(self.__numberSeriesWidgetLines) for j in range(5)]       # Define positions for the grid layout
        self.__seriesWidgetList = []
        for i in range(len(self.__seriesList)):      #Loop for creation and display of serie MainWidgets
            currentWidget = MainWidget(i, self.__seriesList[i])
            self.__seriesWidgetList += [currentWidget]
            self.__gridLayout.addWidget(currentWidget, *self.__positions[i])
            i+=1
            self.__sigMapper.setMapping(currentWidget.favButton, currentWidget.id)
            currentWidget.favButton.clicked.connect(self.__sigMapper.map)       #Connect add to favourite button of MainWidget to signal mapper

    # Getters and setters
    @property
    def seriesList(self):
        return self.__seriesList

    @seriesList.setter
    def seriesList(self,newSeriesList):
        self.__seriesList = newSeriesList

    # Methods
    # Slot to add a favourite to the QListWidget
    def slot_add_to_favourites(self,id): #id = id of the serie to add to favourites
        if (id not in self.__favouritesIDList):     #Check if the serie is already in the favourite
            self.__favouritesIDList += [id]
            print("favouritesIDListlength : " + str(len(self.__favouritesIDList)))
            serie = searchSerie(id)
            nm = serie.name
            self.__favouriteSeries += [serie]
            self.__favouritesWidget.addItem(nm)
            #self.alertWindow.favList += [serie]
            self.alertWindow.quit()
            self.alertWindow = Afficher(self.__favouriteSeries, self)

            with open(self.__fileName, "wb") as favFile:
                pickler = pickle.Pickler(favFile)
                pickler.dump(self.__favouriteSeries)

        else:       # If the serie is already in the favourites, displaying an error message
            error_dialog = QMessageBox.information(None,"Error","Favourites already added.",QMessageBox.Cancel)

    def slot_magic_add_to_favourites(self):
        now = datetime.datetime.now()
        data = findForthcomingSerie()
        m = False
        i = 0
        while m != True:
            id_serie = data[i]["show"]["id"]
            year = int(data[i]["airdate"][:4])
            month = int(data[i]["airdate"][5:7])
            day = int(data[i]["airdate"][8:10])
            hour = int(data[i]["airtime"][0:2])
            print(hour)
            timeRelease = datetime.datetime(year, month, day, hour)
            print(timeRelease)
            print(now)
            timeDelta = timeRelease - now
            print(timeDelta)
            if timeDelta.days >= 0 and timeDelta.seconds >= 0 and id_serie not in self.__favouritesIDList:
                serie = searchSerie(id_serie)
                m = True
            else:
                i = i + 1
                print(i)
        id = serie.id
        self.__favouritesIDList += [id]
        nm = serie.name
        self.__favouriteSeries += [serie]
        self.__favouritesWidget.addItem(nm)

        with open(self.__fileName, "wb") as favFile:
            pickler = pickle.Pickler(favFile)
            pickler.dump(self.__favouriteSeries)

    # Slot to open window with more information for favourites
    def slot_open_serie_window(self):
        idx = self.__favouritesWidget.currentRow()
        id = self.__favouritesIDList[idx]
        ser = self.__favouriteSeries[idx]
        self.newWindow = NewWindow(ser, self)
        self.newWindow.exec_()


    # Slot to do the research
    def slot_research(self):
        self.__searchText = self.__searchWidget.text()

        # Delete all the widgets displayed in scroll area
        for i in reversed(range(self.__gridLayout.count())):
            self.__gridLayout.itemAt(i).widget().setParent(None)

        # Research on the API
        self.__seriesList = searchSeries(self.__searchText)

        # Add results of the research to the scroll area
        for i in range(len(self.__seriesList)):
            currentWidget = MainWidget(i, self.__seriesList[i])
            self.__gridLayout.addWidget(currentWidget, *self.__positions[i])
            self.__sigMapper.setMapping(currentWidget.favButton, currentWidget.id)
            currentWidget.favButton.clicked.connect(self.__sigMapper.map)

    # Slot to remove a serie from the favourites QListWidget
    def slot_remove_favourite(self):
        idx = self.__favouritesWidget.currentRow()
        del self.__favouriteSeries[idx]
        del self.__favouritesIDList[idx]
        self.__favouritesWidget.takeItem(idx)
        self.alertWindow.quit()
        self.alertWindow = Afficher(self.__favouriteSeries,self)

        with open(self.__fileName, "wb") as favFile:
            pickler = pickle.Pickler(favFile)
            pickler.dump(self.__favouriteSeries)

# Class for the main widget
class MainWidget(QFrame):
    def __init__(self, id, serie, parent = None): # id = id of the widget, serie = serie to be displayed by the widget
        super(MainWidget, self).__init__(parent)

        # Attributes
        self.__ser = serie
        self.__id = serie.id

        # Look
        self.setFrameStyle(1)
        self.setLineWidth(3)
        self.setObjectName("mainWidget")
        self.setStyleSheet("#mainWidget{border: 3px solid white;}")
        
        # Size
        self.__sizePolicy = QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.__QSizePolicy = self.__sizePolicy
        self.setFixedSize(300,400)

        # Layout
        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)

        # Text : display serie name in a QLabel
        labelString = serie.name
        #Fonts
        #labelString = str(id) + ". " + QFontDatabase().families()[id]
        self.__textLabel = QLabel(labelString)
        self.__textLabel.setText("<span style=' font-size:16pt; font-weight:600; color:#FFFFFF;'>"+labelString+"</span>")
        #Fonts
        #self.__text.setFont(QFont(QFontDatabase().families()[id], 20))
        self.__textLabel.setAlignment(QtCore.Qt.AlignCenter)

        
        #Image : display serie image in a QLabel
        self.__img = QLabel(self)
        self.__img.setScaledContents(True)
        self.pixmap = QPixmap()
        data = urlopen(serie.image).read()
        self.pixmap.loadFromData(data)
        self.__img.setPixmap(self.pixmap)
        self.__img.setAlignment(QtCore.Qt.AlignCenter)

        # Buttons "Add to favourite" and "More Info"
        self.__favButton = QPushButton("Add to favourite")
        self.__serieButton = QPushButton("More Info")
        self.__serieButton.clicked.connect(self.slot_open_new_window)       #Connect signal clicked to slot_open_new_window

        # Add to layout
        self.__layout.addWidget(self.__textLabel)
        self.__layout.addWidget(self.__img)
        self.__layout.addWidget(self.favButton)
        self.__layout.addWidget(self.__serieButton)


    # Getters and Setters
    @property
    def favButton(self):
        return self.__favButton

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self,newid):
        self.__id = newid

    # Methods and slots
    def slot_open_new_window(self): # Slot to open description window about a serie
        self.__newWindow = NewWindow(self.__ser, self)
        self.__newWindow.exec_()
