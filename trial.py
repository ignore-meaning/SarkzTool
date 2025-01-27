import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow

# 创建一个主窗口类，继承自 QMainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # 调用父类 QMainWindow 的初始化方法
        self.setWindowTitle("萨卡兹肉鸽奇妙小工具")  # 设置窗口标题

        # 创建一个 QLabel 标签，并将其作为主窗口的中央控件
        label = QLabel("work work work 堂堂开工！", self)
        self.setCentralWidget(label)  # 将标签作为窗口的中央控件

# 创建一个 PyQt5 应用程序对象
app = QApplication(sys.argv)

# 创建主窗口实例
window = MainWindow()
window.show()  # 显示窗口

# 进入应用程序的事件循环，保持应用程序运行，直到关闭窗口
sys.exit(app.exec_())