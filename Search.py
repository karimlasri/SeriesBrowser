from urllib.request import Request, urlopen
import json
from ClasseSerie import *

base_URL =  "http://api.tvmaze.com/"
C1 = "search/shows?q=" #Classic Search
C8 = "shows/" #Show episodes list (search by ID)



def searchSeries(search_term): # search_term = input for the research, series_list = result list to be modified
    req = Request(base_URL+C1+search_term, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    data = json.loads(webpage.decode())
    series_list = []
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
    return series_list

def searchEpisodes(id, episodes_list):      # id = id of the serie, episodes_list = result list to be modified
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


def searchSerie(id):        # id = id of the serie. This functions retrieves all information about a serie from the id and returns an object from class Serie
    req = Request(base_URL + C8 + str(id), headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    data = json.loads(webpage.decode())
    idnum = data["id"]
    name = data["name"]
    language = data["language"]
    genres = data["genres"]
    premiered = data["premiered"]
    rating = data["rating"]
    summary = data["summary"]
    image = ""
    if data["image"] != None:
        image = data["image"]["medium"]
    else:
        image = "http://www.solidbackgrounds.com/images/2560x1440/2560x1440-black-solid-color-background.jpg"
    serie = Serie(idnum, name, language, genres, premiered, rating, image, summary)
    return(serie)