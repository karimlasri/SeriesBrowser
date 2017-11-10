from threading import Thread
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import QThread
import datetime
import ClasseSerie
import mainwindow
from Search import searchEpisodes

class Afficher(Thread):

    def __init__(self, favList, parent = None):
        Thread.__init__(self)
        # super(Afficher,self).__init__(parent)
        self.favList = favList
        self.displayList = []
        self.parent = parent

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
                
        self.alertWindow = QMessageBox.information(self.parent,"YO","YO",QMessageBox.Ok)
        # self.alertWindow.textWidget.setText("Il y a {0} episodes qui vont sortir demain".format(str(len(self.displayList))))
        # print("Il y a {0} episodes qui vont sortir demain".format(str(len(self.displayList))))

        # for elt in self.displayList:
        #     self.alertWindow.textWidget.setText(self.alertWindow.textWidget.text() + "\n The episod {0} of season {1} of {2}".format(str(elt[1].number),str(elt[1].season),elt[0]))

        # self.alertWindow.exec_()
        
# class AlertWindow(QDialog):
#
#     def __init__(self,parent = None):
#         super(AlertWindow,self).__init__(parent)
#         self.vLayout = QVBoxLayout(self)
#         self.textWidget = QLabel()
#         self.vLayout.addWidget(self.textWidget)
        

                    








