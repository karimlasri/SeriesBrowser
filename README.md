##### POOA PROJECT  ####

SERIES BROWSER
Group 9 : Karim Lasri, Charlotte Vidal, Titouan Poisson

This desktop application aims to be a Serie Browser tool to look for series and create a list of favourites.
It will keep you up-to-date for the forthcoming episodes of your favourites series.

GETTING STARTED

Prerequisites
This application is based on the Qt framework through the library PyQt5
This library can be installed through pip or downloaded at https://pypi.python.org/pypi/PyQt5

It also uses classical python libraries : math, urllib, datetime, os, pickle, json, string and random.

Because the application is working with an API, the computer should be connected to the internet.

RUNNING

To run the application, run the file "main.py".

HOW TO USE ME

This application has several functionalities:
 - A Search can be done on the top right part of the window
 - The buttons "More Info" displays more information about a serie : summary, list of episods and summaries of episods.
 - A serie displayed on the mainwindow can be added to the favourites list by pushing the button "Add to favourite" below the image of the serie
 - The list of favourites can be handled by the buttons below it "Remove from favourites" or "Clear Favourites". The button "More Info" displays more 
   information about a serie in the list.
 - The check box "Enable notifications" enables or disables the thread for the notification system.

  /!\ Magic button
This button is only here to test the notification system. It looks for a serie that has forthcoming episods within 2 days and adds it to the favourites list.
As a result, a notification will pop out to display the latters.

DESCRIPTION

The API used is the one of TVMAZE accessible at http://www.tvmaze.com/api. This API enables various requests, 
such as a search by keywords or retrieve a serie or episod by ID, etc.

The code is divided into 8 different files :

 - main.py : this file is the launcher of the application

 - ClasseSerie.py : this file codes the storage class of data pulled from the API.
	Class Serie
	Class Episode

 - mainwindow.py : this is the core of the code, where all the Qt framework is used. It's divided in two classes.
	Class MainWindow : class for the main window 
	Class MainWidget : class for the main widget used in the display of a serie in the mainwindow.

 - newwindow.py : this file codes the window that pops out to display more information about a serie : summary, list of episods, summaries of episods.
	Class NewWindow

 - Search.py : this file gathers all the functions used to request data from the API.

 - alert.py : this file codes the thread used in the notification system to display forthcoming episods from the list of favourites series.
              The thread looks in the favourites list if some episodes will be aired within 2 days and pops out a window if so.
	Class AlertWindow

 - main.ui : C++ file used by PyQt5 to create the fundation of the mainwindow.

 - favourites : file used by the python pickler to store favourites list.