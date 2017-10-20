# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 15:19:52 2017

@author: Karim
"""

from urllib.request import Request, urlopen
import json
import time
import urllib
from ClasseSerie import *
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


nameList = []
imgList = []
dico = {}
seriesList = []
#SEARCH
search_terms = "girls"
req = Request(base_URL+C1+search_terms, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
data = json.loads(webpage.decode())

for e in data:
    name = e["show"]["name"]
    idnum = e["show"]["id"]
    name = e["show"]["name"]
    language = e["show"]["language"]
    genres = e["show"]["genres"]
    premiered = e["show"]["premiered"]
    rating = e["show"]["rating"]
    summary = e["show"]["summary"]
    image = ""
    if e["show"]["image"] != None:
        image = e["show"]["image"]["medium"]
    else :
        image = "http://www.qygjxz.com/data/out/31/5754152-black-image.jpg"
    serie = Serie(idnum, name, language, genres, premiered, rating, image, summary)
    seriesList += [serie]
    dico[name]=image
nVids = len(nameList)
print(nameList)
print(nVids)
print(imgList)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MyWindow(5, seriesList, "HomePage", "HomePage")
    sys.exit(app.exec_())