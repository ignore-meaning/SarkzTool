from Recorder import recorder
from Judge import judge
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("萨卡兹肉鸽奇妙小工具")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('img/operators/头像_凯尔希_2.png'))

        # 创建堆叠窗口容器
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 创建页面实例
        self.recorder_page = recorder.MainPage()
        self.judge_page = judge.MainPage()

        # 添加页面到堆叠容器
        self.stacked_widget.addWidget(self.recorder_page)
        self.stacked_widget.addWidget(self.judge_page)

        # 创建菜单栏
        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()

        # 切换菜单
        switch_menu = menu_bar.addMenu("功能")

        # 添加切换动作
        action_page1 = QAction("Recorder", self)
        action_page1.triggered.connect(lambda: self.switch_page(0))
        switch_menu.addAction(action_page1)

        action_page2 = QAction("Judge", self)
        action_page2.triggered.connect(lambda: self.switch_page(1))
        switch_menu.addAction(action_page2)

    def switch_page(self, index):
        self.stacked_widget.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
