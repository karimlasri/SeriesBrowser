from threading import Thread
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
import datetime
import ClasseSerie
import mainwindow
from Search import searchEpisodes

class Afficher(Thread):

    def __init__(self, favList):
        Thread.__init__(self)
        self.favList = favList
        self.displayList = []

    def run(self):
        now = datetime.datetime.now()

        for serie in self.favList:
            epList = []
            searchEpisodes(serie.id,epList)
            for ep in epList:
                year = int(ep.airdate[:4])
                month = int(ep.airdate[5:7])
                day = int(ep.airdate[8:10])
                hour = int(ep.airtime[:2])

                timeRelease = datetime.datetime(year,month,day,hour)

                timeDelta = timeRelease - now
#                print(timeDelta)

                if timeDelta.days < 2 and timeDelta.days >=0:
                    print("yo")
                    self.displayList += [(serie.name,ep)]
                
        print(self.displayList)
        self.alertWindow = alertWindow()
        self.alertWindow.textWidget.setText("Il y a {0} episodes qui vont sortir demain".format(str(len(self.displayList))))

        for elt in self.displayList:
            self.alertWindow.textWidget.setText(self.alertWindow.textWidget.text() + "\n The episod {0} of season {1} of {3}".format(str(elt(2).number),str(elt(2).season),elt(1)))
            

        self.alertWindow.exec_()
        
class alertWindow(QDialog):
    
    def __init__(self,parent = None):
        super(alertWindow,self).__init__(parent)
        self.vLayout = QVBoxLayout(self)
        self.textWidget = QLabel()
        self.vLayout.addWidget(self.textWidget)
        

                    








