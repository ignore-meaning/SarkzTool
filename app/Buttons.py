import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt  # 导入 Qt 模块以使用光标样式


# 自定义按钮类，继承自 QPushButton
class CustomButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        # 设置按钮的初始样式
        self.setStyleSheet("""
            QPushButton {
                background-color: #808080; /* 灰色背景 */
                color: white; /* 文字颜色 */
                border: 2px solid black; /* 黑色边框 */
                padding: 10px 20px; /* 内边距 */
                font-size: 16px; /* 字体大小 */
                border-radius: 5px; /* 圆角 */
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

        # 连接按钮的点击信号到自定义的槽函数
        self.clicked.connect(self.on_clicked)

    # 自定义的槽函数
    def on_clicked(self):
        print("Custom button clicked!")


# 主窗口类
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("Custom Button Example")
        self.setGeometry(100, 100, 300, 200)

        # 创建布局
        layout = QVBoxLayout()

        # 创建自定义按钮实例
        custom_button = CustomButton("添加干员")

        # 将按钮添加到布局中
        layout.addWidget(custom_button)

        # 设置窗口的布局
        self.setLayout(layout)


# 主程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建主窗口实例
    window = MainWindow()
    window.show()

    # 运行应用程序
    sys.exit(app.exec_())