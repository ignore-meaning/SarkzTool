from PyQt5.QtWidgets import *

class Page(QWidget):
    selected_operators = []
    selected_treasures = []

    def __init__(self, parent=None):
        super().__init__(parent)
