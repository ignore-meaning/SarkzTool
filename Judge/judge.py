import sys
import json
import pprint
from PyQt5.QtWidgets import *
from Scripts import JsFunctions
from common import Buttons,ComboBox,Data_list
from Recorder.FirstChildrenWindows import FirstChildrenWindow

class MainPage(QWidget):  # 类名改为 PascalCase 规范

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.init_subwindows()
        # self.show()

    def init_ui(self):
        # 主布局设置
        main_layout = QVBoxLayout()
        # main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 控制区域布局
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)

        operator_layout = QHBoxLayout()
        operator_layout.setSpacing(10)

        treasure_layout = QHBoxLayout()
        treasure_layout.setSpacing(10)

        feasible_mission_layout=QHBoxLayout()
        feasible_mission_layout.setSpacing(10)


        self.operator_btn = Buttons.CustomButton('配置干员')
        self.treasure_btn = Buttons.CustomButton('配置藏品')
        self.era_combo = ComboBox.CustomComboBox()
        self.era_combo.addItems(['无', '天灾年代', '魔王年代', '苦难年代', '奇观年代', '拥挤年代'])
        self.judge_btn=Buttons.CustomButton('判断')

        # 添加控件到布局
        control_layout.addWidget(self.operator_btn)
        control_layout.addWidget(self.treasure_btn)
        control_layout.addWidget(self.era_combo)
        control_layout.addWidget(self.judge_btn)
        # control_layout.setAlignment(Qt.AlignLeft)

        # 信息显示区域
        self.operator_display = QTextBrowser()
        self.operator_display.setMaximumSize(500, 150)
        self.treasure_display = QTextBrowser()
        self.treasure_display.setMaximumSize(500, 150)
        self.feasible_mission_display=QTextBrowser()
        self.feasible_mission_display.setMaximumSize(500, 150)

        operator_layout.addWidget(self.operator_display, stretch=1)
        # operator_layout.setAlignment(Qt.AlignLeft)
        treasure_layout.addWidget(self.treasure_display, stretch=1)
        # treasure_layout.setAlignment(Qt.AlignLeft)
        feasible_mission_layout.addWidget(self.feasible_mission_display,stretch=1)

        # 组合布局
        main_layout.addLayout(control_layout)
        main_layout.addLayout(operator_layout)
        main_layout.addLayout(treasure_layout)
        main_layout.addLayout(feasible_mission_layout)

        self.setLayout(main_layout)

        # 信号连接
        self.operator_btn.clicked.connect(self.show_operator_window)
        self.treasure_btn.clicked.connect(self.show_treasure_window)
        self.judge_btn.clicked.connect(self.judge_operation)

        # 初始化子窗口

    def init_subwindows(self):
        self.operator_window = FirstChildrenWindow('干员', Data_list.DataList.operator_list, self)
        self.operator_window.selection_changed.connect(self.update_operator_display)

        self.treasure_window = FirstChildrenWindow('藏品', Data_list.DataList.treasure_list, self)
        self.treasure_window.selection_changed.connect(self.update_treasure_display)

    def update_operator_display(self, selection):
        """更新干员显示"""
        Data_list.DataList.selected_operators = selection
        self.operator_display.setText(', '.join(selection))

    def update_treasure_display(self, selection):
        """更新藏品显示"""
        Data_list.DataList.selected_treasures = selection
        self.treasure_display.setText(', '.join(selection))

    def show_operator_window(self):
        """显示干员选择窗口"""
        self.operator_window.show()

    def show_treasure_window(self):
        """显示藏品选择窗口"""
        self.treasure_window.show()

    def judge_operation(self):
        feasible_mission=JsFunctions.feasibleMissions(Data_list.DataList.operator_list,
                                                      Data_list.DataList.treasure_list,
                                                      self.era_combo.currentText())
        # print(str(feasible_mission))
        self.feasible_mission_display.setText('\n'.join(f'{key}: {value}' for key, value in feasible_mission.items()))
