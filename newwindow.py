from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QListWidget, QTextEdit
from ClasseSerie import *
from Search import searchEpisodes

# Class NewWindow is QDialog displaying informations about the serie : summary, list of episods and summaries of episods
class NewWindow(QDialog):
    def __init__(self, ser, parent = None):
        super(NewWindow,self).__init__(parent)
        self.__serie = ser

        # Layouts
        self.__vLayout = QVBoxLayout()      # Main Layout
        self.setLayout(self.__vLayout)
        self.__hLayout = QHBoxLayout()      # Secondary layout


        # Name of the serie
        self.__textWidget = QLabel(self.__serie.name)
        self.__vLayout.addWidget(self.__textWidget)

        # Summary of the serie
        self.__resumeWidget = QTextEdit(self.__serie.summary)
        self.__vLayout.addWidget(self.__resumeWidget)
        self.__vLayout.addLayout(self.__hLayout)

        # List of episods
        self.__epList = QListWidget()
        self.__hLayout.addWidget(self.__epList)

        # Summary of the episods
        self.__epSum = QTextEdit()
        self.__hLayout.addWidget(self.__epSum)

        # Retrieving list of episodes from API
        self.__episodesList = []
        searchEpisodes(self.__serie.id, self.__episodesList)
        for i in range(len(self.__episodesList)):
            name = "S"+str(self.__episodesList[i].season)+"E"+str(self.__episodesList[i].number)+" - "+self.__episodesList[i].name
            self.__epList.addItem(name)

        # Connecting signal itemClicked in QListWidget to display episodes summaries
        self.__epList.itemClicked.connect(self.slot_episode_summary)


    # Methods and slots

    def slot_episode_summary(self): # slot to display episode summary
        idx = self.__epList.currentRow()
        ep = self.__episodesList[idx]
        summ = ep.summary
        self.__epSum.clear()

        if summ == "" or summ == None:
            self.__epSum.insertPlainText("No description available.")

        else:
            # Remove "<p>" and "<\p>"
            summList = summ.split("<")
            summ = summList[1]
            summList = summ.split(">")
            summ = summList[1]
            self.__epSum.insertPlainText(summ)

