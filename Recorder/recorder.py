import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from Recorder.FirstChildrenWindows import FirstChildrenWindow
from Scripts import JsFunctions
from common import Buttons,ComboBox,Data_list

class MainPage(QWidget):  # 类名改为 PascalCase 规范

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.init_subwindows()
        #self.show()

    def init_ui(self):
        # 主布局设置
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)

        # 控制区域布局
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)

        operator_layout=QHBoxLayout()
        operator_layout.setSpacing(10)

        treasure_layout = QHBoxLayout()
        treasure_layout.setSpacing(10)

        # 初始化控件
        self.level_combo = ComboBox.CustomComboBox()
        self.level_combo.addItems(['1', '2', '3', '4', '5', '6'])

        self.mission_combo = ComboBox.CustomComboBox()
        self.mission_combo.addItems(Data_list.DataList.mission_list['1'])

        self.emergency_check = QCheckBox('紧急')
        self.operator_btn = Buttons.CustomButton('配置干员')
        self.treasure_btn = Buttons.CustomButton('配置藏品')
        self.era_combo = ComboBox.CustomComboBox()
        self.era_combo.addItems(['无', '天灾年代', '魔王年代', '苦难年代', '奇观年代', '拥挤年代'])
        self.submit_btn = Buttons.CustomButton('提交')

        # 添加控件到布局
        control_layout.addWidget(self.level_combo)
        control_layout.addWidget(self.mission_combo)
        control_layout.addWidget(self.emergency_check)
        control_layout.addWidget(self.era_combo)
        control_layout.addWidget(self.submit_btn)
        #control_layout.setAlignment(Qt.AlignLeft)

        # 信息显示区域
        self.operator_display = QTextBrowser()
        self.operator_display.setMaximumSize(500, 150)
        self.treasure_display = QTextBrowser()
        self.treasure_display.setMaximumSize(500, 150)


        operator_layout.addWidget(self.operator_btn)
        operator_layout.addWidget(self.operator_display, stretch=1)
        #operator_layout.setAlignment(Qt.AlignLeft)
        treasure_layout.addWidget(self.treasure_btn)
        treasure_layout.addWidget(self.treasure_display, stretch=1)
        #treasure_layout.setAlignment(Qt.AlignLeft)

        # 组合布局
        main_layout.addLayout(control_layout)
        main_layout.addLayout(operator_layout)
        main_layout.addLayout(treasure_layout)

        self.setLayout(main_layout)

        # 信号连接
        self.level_combo.currentTextChanged.connect(self.update_missions)
        self.operator_btn.clicked.connect(self.show_operator_window)
        self.treasure_btn.clicked.connect(self.show_treasure_window)
        self.submit_btn.clicked.connect(self.submit_operation)

        # 初始化子窗口
    def init_subwindows(self):
        self.operator_window = FirstChildrenWindow('干员', Data_list.DataList.operator_list, self)
        self.operator_window.selection_changed.connect(self.update_operator_display)

        self.treasure_window = FirstChildrenWindow('藏品', Data_list.DataList.treasure_list, self)
        self.treasure_window.selection_changed.connect(self.update_treasure_display)



    def update_missions(self):
        """更新关卡选项"""
        level = self.level_combo.currentText()
        try:
            self.mission_combo.clear()
            self.mission_combo.addItems(Data_list.DataList.mission_list.get(level, []))
        except KeyError:
            QMessageBox.warning(self, '错误', '无效的层数选择')

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

    def submit_operation(self):
        """提交作战信息"""
        try:
            level = int(self.level_combo.currentText())
            mission = ('紧急' if self.emergency_check.isChecked() else '') + self.mission_combo.currentText()
            era = self.era_combo.currentText()

            if not Data_list.DataList.selected_operators:
                raise ValueError("请选择干员")

            JsFunctions.add_operation(
                level=level,
                mission=mission,
                operator_list=Data_list.DataList.selected_operators,
                treasure_list=Data_list.DataList.selected_treasures,
                era=era
            )
            QMessageBox.information(self, '提交成功', '作战信息已提交')

        except Exception as e:
            QMessageBox.critical(self, '错误', f'提交失败: {str(e)}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainPage()
    sys.exit(app.exec_())