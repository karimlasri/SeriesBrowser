from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QListWidget, QTextEdit
from ClasseSerie import *
from Search import searchEpisodes

class NewWindow(QDialog):
    def __init__(self, ser, parent = None):
        super(NewWindow,self).__init__(parent)
        self.__serie = ser
        self.__vLayout = QVBoxLayout()
        self.setLayout(self.__vLayout)
        self.__textWidget = QLabel(self.__serie.name)
        self.__vLayout.addWidget(self.__textWidget)
        self.__resumeWidget = QTextEdit(self.__serie.summary)
        self.__vLayout.addWidget(self.__resumeWidget)
        self.__hLayout = QHBoxLayout()
        self.__vLayout.addLayout(self.__hLayout)
        self.__epList = QListWidget()
        self.__hLayout.addWidget(self.__epList)
        self.__epSum = QTextEdit()
        self.__hLayout.addWidget(self.__epSum)
        # self.UI = uic.loadUi('dialog.ui', self)
        # self.verticalLayout = QVBoxLayout(self)
        self.__episodesList = []
        searchEpisodes(self.__serie.id, self.__episodesList)
        for i in range(len(self.__episodesList)):
            self.__epList.addItem(self.__episodesList[i].name)

        self.__epList.itemClicked.connect(self.slot_episode_summary)

    def slot_episode_summary(self, item):
        idx = self.__epList.currentRow()
        ep = self.__episodesList[idx]
        summ = ep.summary
        self.__epSum.clear()
        if summ != None :
            # Remove "<p>" and "<\p>"
            summList = summ.split("<")
            summ = summList[1]
            summList = summ.split(">")
            summ = summList[1]
            self.__epSum.insertPlainText(summ)
        else:
            self.__epSum.insertPlainText("No description available.")
