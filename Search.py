from urllib.request import Request, urlopen
import json
from ClasseSerie import *

base_URL =  "http://api.tvmaze.com/"
C1 = "search/shows?q=" #Classic Search

def search(search_term, series_list):

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
            image = "http://www.qygjxz.com/data/out/31/5754152-black-image.jpg"
        serie = Serie(idnum, name, language, genres, premiered, rating, image, summary)
        series_list += [serie]