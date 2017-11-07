# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 14:33:35 2017

@author: Karim
"""

class Serie:
    def __init__(self, idnum, nam, lang, genr, prem, rat, img, summ):
        self.id = idnum
        self.name = nam
        self.language = lang
        self.genres = genr
        self.premiered = prem
        self.rating = rat
        self.image = img
        self.summary = summ

    # @property
    # def name(self):
    #     return self.__name
    #
    # @name.setter
    # def name(self, newid):
    #     self.__name = newid


class Episode:
    def __init__(self, idnum, nam, seas, nb, airdt, airtm, img, summ):
        self.id = idnum
        self.name = nam
        self.season = seas
        self.number = nb
        self.airdate = airdt
        self.airtime = airtm
        self.image = img
        self.summary = summ