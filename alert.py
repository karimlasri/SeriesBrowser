from threading import Thread
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import datetime
import ClasseSerie
import mainwindow
from Search import searchEpisodes

class Afficher(QThread):

    seriesReleased = pyqtSignal()

    def __init__(self, favList, parent = None):
        QThread.__init__(self)
        self.favList = favList
        self.displayList = []
        self.seriesReleased.connect(self.slot_show_forthcoming_series)

    def slot_show_forthcoming_series(self):
        self.text = "boo"
        print(self.displayList)
        for elt in self.displayList:
            x = str(1)
            str = elt[0] + " S" #+ str(elt[1].season) + " E" + str(elt[1].number) + " will be aired on " + elt[1].airdate + "\n"
            # str = "k"
            self.text += str
        # self.messageBox.setText(self.text)
        self.messageBox = QMessageBox.information(None, "YO", self.text , QMessageBox.Ok)


    def run(self):
        self.now = datetime.datetime.now()
        print(self.displayList)
        for serie in self.favList:
            epList = []
            searchEpisodes(serie.id,epList)
            for ep in epList:
                year = int(ep.airdate[:4])
                month = int(ep.airdate[5:7])
                day = int(ep.airdate[8:10])
                timeRelease = datetime.datetime(year,month,day)
                timeDelta = timeRelease - self.now
                # print(timeDelta)

                if timeDelta.days < 1 and timeDelta.days >=0:
                    print("yyoo")
                    self.displayList += [(serie.name,ep)]
                    print(ep.season)

        if self.displayList != []:
            self.seriesReleased.emit()