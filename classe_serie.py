# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 14:33:35 2017

@author: Karim
"""

# Class to store series
class Serie:
    def __init__(self, idnum, nam, img, summ):
        self.__id = idnum # Unique id
        try:
            if (idnum == None):
                raise ValueError("The idnum shouldn't be empty.")
        except ValueError:
            self.__id = 0

        self.__name = nam # Name of the serie
        try:
            if (nam == "" or nam == None):
                raise ValueError("The name shouldn't be empty.")
        except ValueError:
            self.__name = "Unnamed"

        self.__image = img # Image of the serie
        try:
            if (img == None):
                raise ValueError("The image shouldn't be empty.")
            else:
                self.__image = img["medium"]
        except ValueError: # If the serie has no image, a black image is loaded instead
            self.__image = "http://www.solidbackgrounds.com/images/2560x1440/2560x1440-black-solid-color-background.jpg"

        self.__summary = summ # Summary of the serie
        try:
            if (summ == "" or summ == None):
                raise ValueError("The summary shouldn't be empty.")
        except ValueError:
            self.__airtime = "No summary available."

    #Getters
    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def image(self):
        return self.__image

    @property
    def summary(self):
        return self.__summary

# Class to store episodes
class Episode:
    def __init__(self, idnum, nam, seas, nb, airdt, airtm, img, summ):
        self.__id = idnum # Unique ID
        try:
            if (idnum == None):
                raise ValueError("The id shouldn't be empty.")
        except ValueError:
            self.__id = 1

        self.__name = nam # Name of the episode
        try:
            if (nam == "" or nam == None):
                raise ValueError("The name shouldn't be empty.")
        except ValueError:
            self.__name = "No name available"

        self.__season = seas # Season of the episode
        try:
            if (seas == None):
                raise ValueError("The season shouldn't be empty.")
        except ValueError:
            self.__season = 0

        self.__number = nb # Number of the serie in the season
        try:
            if (nb == None):
                raise ValueError("The number shouldn't be empty.")
        except ValueError:
            self.__number = 0

        self.__airdate = airdt # Airdate of the episode
        try:
            if (airdt == "" or airdt == None):
                raise ValueError("The airdate shouldn't be empty.")
        except ValueError:
            self.__airdate = "2000-01-01"

        self.__airtime = airtm # Airtime of the episode
        try:
            if (airtm == "" or airtm == None):
                raise ValueError("The airtime shouldn't be empty.")
        except ValueError:
            self.__airtime = "00:00"

        self.__image = img # Image of the episode
        try:
            if (img == None or img == ""):
                raise ValueError("The image shouldn't be empty.")
        except ValueError: # If the episode has no image, a black one is loaded
            self.__image = "http://www.solidbackgrounds.com/images/2560x1440/2560x1440-black-solid-color-background.jpg"

        self.__summary = summ # The summary of the episode
        try:
            if (summ == "" or summ == None):
                raise ValueError("The summary shouldn't be empty.")
        except ValueError:
            self.__summary = "No summary available."

    # Getters
    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def season(self):
        return self.__season

    @property
    def number(self):
        return self.__number

    @property
    def airdate(self):
        return self.__airdate

    @property
    def airtime(self):
        return self.__airtime

    @property
    def image(self):
        return self.__image

    @property
    def summary(self):
        return self.__summary