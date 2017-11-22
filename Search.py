from urllib.request import Request, urlopen
import json
from ClasseSerie import *
import string
import random
import datetime

base_URL =  "http://api.tvmaze.com/"
C1 = "search/shows?q=" #Classic Search
C5 = "schedule?country=US" #Schedule search
C8 = "shows/" #Show episodes list (search by ID)


# #URLs disponibles
#
# base_URL =  "http://api.tvmaze.com/"
# C1 = "search/shows?q=" #Classic Search
# C2 = "singlesearch/shows?q=girls" #Another type of search (less interesting in our case)
# C3 = "lookup/shows?tvrage=24493" #Search by tvrage
# C4 = "search/people?q=lauren" #People search
# C5 = "schedule?country=US&date=2014-12-01" #Schedule search
# C6 = "schedule/full" #Full schedule to come
# C7 = "shows/1?embed=cast" #Show main information (search by ID)
# C8 = "shows/1/episodes?specials=1" #Show episodes list (search by ID)
# C9 = "shows/1/episodebynumber?season=1&number=1" #Show episode by number (show by ID)
# C10 = "shows/1/episodesbydate?date=2013-07-01" #Episodes by date
# C11 = "shows/1/seasons" #Show seasons
# C12 = "seasons/1/episodes" #Season episodes
# C13 = "shows/1/cast" #Show cast
# C14 = "shows/1/crew" #Show crew

def searchSeries(search_term): # takes search_term, a string, as an input for the research, and returns a list of Serie objects constructed from the result of the API
    req = Request(base_URL+C1+search_term, headers={'User-Agent': 'Mozilla/5.0'}) # the URL that should be read
    webpage = urlopen(req).read()
    data = json.loads(webpage.decode())
    series_list = []
    for e in data: # parsing the json file
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
        serie = Serie(idnum, name, language, genres, premiered, rating, image, summary) # constructing a Serie object from the parsed data
        series_list += [serie] # appending the Serie object to the list to be returned
    return series_list

def searchEpisodes(id): # takes id, a number identifying a serie on the API, as an input for the research, and returns a list of Episode objects constructed from the list of episodes of the serie
    req = Request(base_URL + C8 + str(id) + "/episodes", headers={'User-Agent': 'Mozilla/5.0'}) # the URL that should be read
    webpage = urlopen(req).read()
    data = json.loads(webpage.decode())
    episodes_list = []
    for e in data: # parsing the json file
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
        episode = Episode(idnum, name, seas, nb, airdt, airtm, image, summary) # constructing an Episode object from the parsed data
        episodes_list += [episode]
    return(episodes_list)


def searchSerie(id): # id = id of the serie in the API. This functions retrieves all information about a serie from the id and returns an object from class Serie
    req = Request(base_URL + C8 + str(id), headers={'User-Agent': 'Mozilla/5.0'}) # the URL that should be read
    webpage = urlopen(req).read()
    data = json.loads(webpage.decode())
    # parsing the json file
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
    else: # if the serie has no image
        image = "http://www.solidbackgrounds.com/images/2560x1440/2560x1440-black-solid-color-background.jpg"
    serie = Serie(idnum, name, language, genres, premiered, rating, image, summary) # constructing a Serie object from the parsed data
    return(serie)

#Finds a serie that's going to be aired soon and is not in IDList
def findForthcomingSerie(IDList):
    now = datetime.datetime.now()
    req = Request(base_URL + C5, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    data = json.loads(webpage.decode())
    found = False
    i = 0
    while (found != True) and (i < len(data)):
        id_serie = data[i]["show"]["id"]
        year = int(data[i]["airdate"][:4])
        month = int(data[i]["airdate"][5:7])
        day = int(data[i]["airdate"][8:10])
        hour = int(data[i]["airtime"][0:2])
        min = int(data[i]["airtime"][3:4])
        timeRelease = datetime.datetime(year, month, day, hour, min)
        timeDelta = timeRelease - now
        if timeDelta.days >= 0 and timeDelta.seconds >= 0 and id_serie not in IDList:
            serie = searchSerie(id_serie)
            found = True
        else:
            i = i + 1
    # if i == len(data): lever une exception
    #    raiseError
    return serie

def randomSearch():
    seriesList = []
    seriesList += searchSeries(random.choice(string.ascii_lowercase))
    seriesList += searchSeries(random.choice(string.ascii_lowercase))
    return seriesList