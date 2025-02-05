import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt

class CustomComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)  # 启用鼠标跟踪
        self.setFixedSize(130, 50)

    def enterEvent(self, event):
        """鼠标进入时触发"""
        super().enterEvent(event)
        self.setCursor(Qt.PointingHandCursor)  # 模拟点击，显示下拉菜单

    def leaveEvent(self, event):
        """鼠标离开时触发"""
        super().leaveEvent(event)
        self.setCursor(Qt.ArrowCursor)  # 隐藏下拉菜单