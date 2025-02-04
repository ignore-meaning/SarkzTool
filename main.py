from Recorder import recorder
from Judge import judge
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

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

    # 干员池、藏品池与作战，目前直接手敲进了 python 文件里，之后应该要单独写一个程序通过读取 img 文件夹的信息自动获得列表
    operator_list = ['阿米娅_2', '阿米娅(近卫)_2', '阿米娅(医疗)_2', '承曦格雷伊_2', '铎铃_2', '菲莱_2', '古米',
                     '古米_2', '寒芒克洛丝_2', '赫默_2', '卡达', '凯尔希_2', '砾', '迷迭香', '迷迭香_2', '魔王_2',
                     '桑葚_2', '深律_2', '石英', '桃金娘', '巫恋_2', '稀音_2', '锡人_2', '晓歌_2', '伊桑', '陨星_2',
                     '火海', '离迁', '侵略', '兴亡']
    treasure_list = ['国王的铠甲', '国王的新枪', '国王的延伸', '轰鸣之手', '诸王的冠冕']
    operation_list = {
        '1': ['坏邻居', '公害', '安全检查', '夺路而逃', '冰川期'],
        '2': ['见闻峰会', '拆东补西', '排风口', '炉工志愿队', '有序清场', '卡兹瀑布', '丛林密布'],
        '3': ['大旗一盘', '血脉之辩', '遮天蔽日', '劳作的清晨', '溃乱魔典', '盲盒商场', '火力小队', '机动队',
              '守望的河水', '卫士不语功', '存亡之战', '或然面纱', '奉献', '斩首', '离歌的庭院', '赴敌者', '王冠之下'],
        '4': ['年代断层', '朽败考察', '飞越大水坑', '腥红甬道', '现代战争法则', '假想对冲', '幽灵城', '神出鬼没',
              '混沌', '争议频发'],
        '5': ['寄人城池下', '计划耕种', '巫咒同盟', '通道封锁', '无罪净土', '浮空城接舷战', '残破学院', '建制',
              '莱茵卫士', '紧急授课', '朝谒', '思维纠正', '魂灵朝谒'],
        '6': ['谋求共识', '神圣的渴求', '洞天福地', '外道', '圣城', '授法', '不容拒绝'],
        '7': ['不容拒绝']
    }

    window = MainWindow()
    window.show()
    app.exec()
