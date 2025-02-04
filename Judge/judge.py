from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        # 原MainWindow1的UI初始化代码
        self.label1 = QLabel("Judge")
        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        self.setLayout(layout)
