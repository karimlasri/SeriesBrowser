import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QLabel, QWidget, QPushButton, QScrollArea, QGridLayout, QVBoxLayout, QLineEdit
from PyQt5.QtGui import *
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5 import QtCore
from math import ceil
from urllib.request import Request, urlopen
import ClasseSerie

#controller, MVC
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 14:58:00 2017

@author: Karim
"""




class MyWindow(QMainWindow):
    def __init__(self,n_display, series_list, nameWindow, typeWindow):
        super().__init__()
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
        # self.gridLayout.addWidget(QPushButton('yo'))
        self.textLabel = QLabel(nameWindow)
        self.textLabel.setText(nameWindow)
        self.textLabel.setTextFormat(QtCore.Qt.RichText)
        self.textLabel.setText("<span style=' font-size:16pt; font-weight:600; color:#aa0000;'>"+nameWindow+"</span>")
        self.UI.gridLayout.addWidget(self.textLabel)
        self.searchWidget = QLineEdit()
        self.searchWidget.setMaximumSize(100,100)
        #self.searchWidget.setAcceptRichText(True)
        self.searchWidget.returnPressed.connect(self.slot_text_changed)
        self.UI.gridLayout.addWidget(self.searchWidget, 0, 2)
        # TODO : Changer serieWidget
        if typeWindow == "serie":
            serieWidget = MainWidget(1, series_list[1])
            self.UI.gridLayout.addWidget(serieWidget)
            
        numberHorizontalLayout = ceil(n_display/5)
        positions = [(i+1,j) for i in range(numberHorizontalLayout) for j in range(5)]
        self.newWidgetlist = []
        i=0
        for i in range(n_display):
                newWidget = MainWidget(i, series_list[i])
                self.newWidgetlist += [newWidget]
                self.UI.gridLayout.addWidget(newWidget, *positions[i])
                i+=1
    def slot_text_changed(self):
        self.searchText = self.searchWidget.text()
        print(self.searchText)

class MainWidget(QFrame):
    def __init__(self, id, serie):
        super().__init__()
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
        self.layout.addWidget(QPushButton(self.text))
#        self.UI.verticalLayout.addWidget(self.img)
#        self.UI.text.setPlainText(serie.name)
#        self.size = QSize(100,100)
        self.setMaximumSize(100,100)


