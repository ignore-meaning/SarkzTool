from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from common import Page
class MainPage(Page.Page):
    def __init__(self, parent=None):
        super().__init__(parent)

    def output(self):
        print(Page.Page.selected_operators)


