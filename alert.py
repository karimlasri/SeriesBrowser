from threading import Thread
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import datetime
import classe_serie
import main_window
from search import searchEpisodes, searchSerie

class Afficher(QThread):

    # On pyqt, signals can't be defined in init function and should be initialized before
    __seriesReleased = pyqtSignal()

    def __init__(self, favList, notifEnabled, parent = None):
        QThread.__init__(self)
        self.__favList = favList # Complete list of user's favourites
        self.__displayList = [] # List of episodes that will be aired soon
        self.__seriesReleased.connect(self.slot_show_forthcoming_series) # Connecting signal to function that displays forthcoming series
        self.__notificationsEnabled = notifEnabled # Bool that indicates whether notifications are enabled or not

    # Getters and setters
    @property
    def favList(self):
        return self.__favList

    @favList.setter
    def favList(self, newFavList):
        self.__favList = newFavList

    @property
    def notificationsEnabled(self):
        return self.__notificationsEnabled

    @notificationsEnabled.setter
    def notificationsEnabled(self, newValue):
        if (type(newValue == bool)):
            self.__notificationsEnabled = newValue

    # Function that displays forthcoming series in a message box
    def slot_show_forthcoming_series(self):
        self.__text = ""
        for elt in self.__displayList: # Iterating on soon-to-be-displayed episodes to add text to the message box
            episodeString = elt[0] + " S" + str(elt[1].season) + " E" + str(elt[1].number) + " will be aired on " + elt[1].airdate + " at " + elt[1].airtime + "\n"
            self.__text += episodeString
        # Displaying the message box
        QMessageBox.information(None, "Some series will be aired soon !", self.__text , QMessageBox.Ok)

    def run(self):
        while (self.__notificationsEnabled):
            self.display_forthcoming_episodes()
            QThread.sleep(120)

    # Function that refreshes the list of forthcoming episodes and displays them by emitting a signal connected to the right slot
    def display_forthcoming_episodes(self):
        self.__displayList = []
        self.__now = datetime.datetime.now()
        for serie in self.__favList: # Testing all episodes from all series in favourite list to check whether they will be aired soon
            epList = searchEpisodes(serie.id)
            for ep in epList:
                year = int(ep.airdate[:4])
                month = int(ep.airdate[5:7])
                day = int(ep.airdate[8:10])
                hour = int(ep.airtime[0:2])
                min = int(ep.airtime[3:4])
                timeRelease = datetime.datetime(year,month,day,hour,min)
                timeDelta = timeRelease - self.__now
                if (timeDelta.days < 2) and (timeDelta.days >= 0) and (timeDelta.seconds >= 0): # Tests whether the episode is aired within two days
                    self.__displayList += [(serie.name,ep)]
        if self.__displayList != [] and self.__notificationsEnabled: # If there are episodes to display, a signal is emitted, activating slot_show_forthcoming_series
            self.__seriesReleased.emit()