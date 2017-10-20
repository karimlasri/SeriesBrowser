from urllib.request import Request, urlopen
import json
from ClasseSerie import *

base_URL =  "http://api.tvmaze.com/"
C1 = "search/shows?q=" #Classic Search
C8 = "shows/" #Show episodes list (search by ID)

def searchSeries(search_term, series_list):

    req = Request(base_URL+C1+search_term, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    data = json.loads(webpage.decode())
    del series_list[:]
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
            image = "http://www.solidbackgrounds.com/images/2560x1440/2560x1440-black-solid-color-background.jpg"
        serie = Serie(idnum, name, language, genres, premiered, rating, image, summary)
        series_list += [serie]

def searchEpisodes(id, episodes_list):
    req = Request(base_URL+C8+str(id)+"/episodes", headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    data = json.loads(webpage.decode())
    del episodes_list[:]
    for e in data:
        name = e["name"]
        idnum = e["id"]
        name = e["name"]
        seas = e["season"]
        nb = e["number"]
        airdt = e["airdate"]
        airtm = e["airtime"]
        summary = e["summary"]
        image = ""
        if e["image"] != None:
            image = e["image"]["medium"]
        else :
            image = "http://www.solidbackgrounds.com/images/2560x1440/2560x1440-black-solid-color-background.jpg"
        episode = Episode(idnum, name, seas, nb, airdt, airtm, image, summary)
        episodes_list += [episode]