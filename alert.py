from threading import Thread
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import datetime
import ClasseSerie
import mainwindow
from Search import searchEpisodes, searchSerie

class Afficher(QThread):

    seriesReleased = pyqtSignal()

    def __init__(self, favList, parent = None):
        QThread.__init__(self)
        self.__favList = favList
        self.displayList = []
        self.seriesReleased.connect(self.slot_show_forthcoming_series)

    @property
    def favList(self):
        return self.__favList

    @favList.setter
    def favList(self, newFavList):
        self.__favList = newFavList

    def slot_show_forthcoming_series(self):
        self.text = ""
        print(len(self.displayList))
        for elt in self.displayList:
            episodeString = elt[0] + " S" + str(elt[1].season) + " E" + str(elt[1].number) + " will be aired on " + elt[1].airdate + " at " + elt[1].airtime + "\n"
            self.text += episodeString
        self.messageBox = QMessageBox.information(None, "Some series will be aired soon !", self.text , QMessageBox.Ok)

    def slot_add_fav_and_display(self,id):
        ser = searchSerie(id)
        if (ser not in self.__favList):
            self.__favList += [ser]
            self.display_forthcoming_episodes()

    def display_forthcoming_episodes(self):
        self.displayList = []
        self.now = datetime.datetime.now()
        print("favlist length : " + str(len(self.favList)))
        for serie in self.favList:
            epList = []
            searchEpisodes(serie.id,epList)
            for ep in epList:
                year = int(ep.airdate[:4])
                month = int(ep.airdate[5:7])
                day = int(ep.airdate[8:10])
                timeRelease = datetime.datetime(year,month,day)
                timeDelta = timeRelease - self.now
                if timeDelta.days < 1 and timeDelta.days >=0:
                    self.displayList += [(serie.name,ep)]
        if self.displayList != []:
            self.seriesReleased.emit()

    def run(self):
        while (True):
            self.display_forthcoming_episodes()
            QThread.sleep(20)