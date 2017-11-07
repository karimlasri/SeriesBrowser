from threading import Thread
import datetime
import ClasseSerie
import mainwindow

class Afficher(Thread):

    def __init__(self, favList):
        Thread.__init__(self)
        self.favList = favList

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

                if timeDelta.days < 2 and timeDelta.days >=0:
                    #thing to do








