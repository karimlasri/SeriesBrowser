# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 14:33:35 2017

@author: Karim
"""

class Serie:
    def __init__(self, idnum, nam, lang, genr, prem, rat, img, summ):
        self.__id = idnum
        self.__name = nam
        self.language = lang
        self.genres = genr
        self.premiered = prem
        self.rating = rat
        self.__image = img
        self.__summary = summ

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


class Episode:
    def __init__(self, idnum, nam, seas, nb, airdt, airtm, img, summ):
        self.__id = idnum
        self.__name = nam
        self.__season = seas
        self.__number = nb
        self.__airdate = airdt
        self.__airtime = airtm
        if (airtm == ""):
            self.__airtime = "00:00"
        self.__image = img
        self.__summary = summ

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