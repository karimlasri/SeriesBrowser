# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 15:19:52 2017

@author: Karim
"""

from Search import search
import time
import urllib
from mainwindow import *

#URLs disponibles

base_URL =  "http://api.tvmaze.com/"
C1 = "search/shows?q=" #Classic Search
C2 = "singlesearch/shows?q=girls" #Another type of search (less interesting in our case)
C3 = "lookup/shows?tvrage=24493" #Search by tvrage
C4 = "search/people?q=lauren" #People search
C5 = "schedule?country=US&date=2014-12-01" #Schedule search
C6 = "schedule/full" #Full schedule to come
C7 = "shows/1?embed=cast" #Show main information (search by ID)
C8 = "shows/1/episodes?specials=1" #Show episodes list (search by ID)
C9 = "shows/1/episodebynumber?season=1&number=1" #Show episode by number (show by ID)
C10 = "shows/1/episodesbydate?date=2013-07-01" #Episodes by date
C11 = "shows/1/seasons" #Show seasons
C12 = "seasons/1/episodes" #Season episodes
C13 = "shows/1/cast" #Show cast
C14 = "shows/1/crew" #Show crew

seriesList = []
#SEARCH
search_terms = "girls"

search(search_terms, seriesList)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MyWindow(5, seriesList, "HomePage", "HomePage")
    sys.exit(app.exec_())