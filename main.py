# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 15:19:52 2017

@author: Karim
"""

from main_window import *
from search import randomSearch

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow(randomSearch(), "HomePage")
    sys.exit(app.exec_())

