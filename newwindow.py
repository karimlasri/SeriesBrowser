from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QListWidget, QTextEdit
from ClasseSerie import *
from Search import searchEpisodes

class NewWindow(QDialog):
    def __init__(self, ser, parent = None):
        super(NewWindow,self).__init__(parent)
        self.serie = ser
        self.vLayout = QVBoxLayout()
        self.setLayout(self.vLayout)
        self.textWidget = QLabel(self.serie.name)
        self.vLayout.addWidget(self.textWidget)
        self.resumeWidget = QTextEdit(self.serie.summary)
        self.vLayout.addWidget(self.resumeWidget)
        self.hLayout = QHBoxLayout()
        self.vLayout.addLayout(self.hLayout)
        self.epList = QListWidget()
        self.hLayout.addWidget(self.epList)
        self.epSum = QTextEdit()
        self.hLayout.addWidget(self.epSum)
        # self.UI = uic.loadUi('dialog.ui', self)
        # self.verticalLayout = QVBoxLayout(self)
        self.episodesList = []
        searchEpisodes(self.serie.id, self.episodesList)
        for i in range(len(self.episodesList)):
            self.epList.addItem(self.episodesList[i].name)

        self.epList.itemClicked.connect(self.slot_episode_summary)

    def slot_episode_summary(self, item):
        idx = self.epList.currentRow()
        ep = self.episodesList[idx]
        summ = ep.summary
        self.epSum.clear()
        self.epSum.insertPlainText(summ)
