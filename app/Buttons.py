import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt  # 导入 Qt 模块以使用光标样式

class CustomButton(QPushButton):
    def __init__(self, text, on_click, parent=None):
        super().__init__(text, parent)
        self.on_click = on_click
        self.clicked.connect(self._on_click)

        # 设置按钮的初始样式
        self.setStyleSheet("""
            QPushButton {
                background-color: #e3dede; /* 灰色背景 */
                color: black; /* 文字颜色 */
                border: 2px solid gray; /* 黑色边框 */
                padding: 10px 20px; /* 内边距 */
                font-size: 16px; /* 字体大小 */

            }
            QPushButton:hover {
                background-color: #A9A9A9; /* 悬停时的背景色 */
            }
            QPushButton:pressed {
                background-color: #696969; /* 按下时的背景色 */
            }
        """)

        # 设置鼠标悬停时的光标样式为手型
        self.setCursor(Qt.PointingHandCursor)

        # 固定按钮的大小
        self.setFixedSize(120, 50)  # 宽度 200，高度 50

    def _on_click(self):
        # 调用传递进来的函数
        self.on_click()

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 创建一个自定义按钮，点击时触发 self.custom_action 方法
        button = CustomButton('Click Me', self.custom_action)
        layout.addWidget(button)

        self.setLayout(layout)
        self.setWindowTitle('Custom Button Example')
        self.show()

    def custom_action(self):
        print('Button clicked! Custom action executed.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())