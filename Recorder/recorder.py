import sys
from PyQt5.QtWidgets import *
from Recorder.FirstChildrenWindows import FirstChildrenWindow
from Scripts import JsFunctions
from common import Buttons,ComboBox
global operator_list, treasure_list, operation_list
operator_list = JsFunctions.read('operatorData')['可用干员']
treasure_list = JsFunctions.read('treasureData')['可用藏品']
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
class MainPage(QWidget):  # 类名改为 PascalCase 规范

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_operators = []
        self.selected_treasures = []
        self.init_ui()
        self.init_subwindows()

    def init_ui(self):
        # 主布局设置
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 控制区域布局
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)

        # 初始化控件
        self.level_combo = ComboBox.CustomComboBox()
        self.level_combo.addItems(['1', '2', '3', '4', '5', '6'])

        self.operation_combo = ComboBox.CustomComboBox()
        self.operation_combo.addItems(operation_list['1'])

        self.emergency_check = QCheckBox('紧急')
        self.operator_btn = Buttons.CustomButton('干员')
        self.treasure_btn = Buttons.CustomButton('藏品')
        self.era_combo = ComboBox.CustomComboBox()
        self.era_combo.addItems(['无', '天灾年代', '魔王年代', '苦难年代', '奇观年代', '拥挤年代'])
        self.submit_btn = Buttons.CustomButton('提交')

        # 添加控件到布局
        control_layout.addWidget(self.level_combo)
        control_layout.addWidget(self.operation_combo)
        control_layout.addWidget(self.emergency_check)
        control_layout.addWidget(self.operator_btn)
        control_layout.addWidget(self.treasure_btn)
        control_layout.addWidget(self.era_combo)
        control_layout.addWidget(self.submit_btn)

        # 信息显示区域
        self.operator_display = QTextBrowser()
        self.operator_display.setMaximumHeight(150)
        self.treasure_display = QTextBrowser()
        self.treasure_display.setMaximumHeight(50)

        # 组合布局
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.operator_display)
        main_layout.addWidget(self.treasure_display)

        self.setLayout(main_layout)

        # 信号连接
        self.level_combo.currentTextChanged.connect(self.update_operations)
        self.operator_btn.clicked.connect(self.show_operator_window)
        self.treasure_btn.clicked.connect(self.show_treasure_window)
        self.submit_btn.clicked.connect(self.submit_operation)

        # 初始化子窗口
    def init_subwindows(self):
        self.operator_window = FirstChildrenWindow('干员', operator_list, self)
        self.operator_window.selection_changed.connect(self.update_operator_display)

        self.treasure_window = FirstChildrenWindow('藏品', treasure_list, self)
        self.treasure_window.selection_changed.connect(self.update_treasure_display)



    def update_operations(self):
        """更新关卡选项"""
        level = self.level_combo.currentText()
        try:
            self.operation_combo.clear()
            self.operation_combo.addItems(operation_list.get(level, []))
        except KeyError:
            QMessageBox.warning(self, '错误', '无效的层数选择')

    def update_operator_display(self, selection):
        """更新干员显示"""
        self.selected_operators = selection
        self.operator_display.setText(', '.join(selection))

    def update_treasure_display(self, selection):
        """更新藏品显示"""
        self.selected_treasures = selection
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
            operation = ('紧急' if self.emergency_check.isChecked() else '') + self.operation_combo.currentText()
            era = self.era_combo.currentText()

            if not self.selected_operators:
                raise ValueError("请选择干员")

            JsFunctions.add_operation(
                level=level,
                operation_name=operation,
                operator_list=self.selected_operators,
                treasure_list=self.selected_treasures,
                era=era
            )
            QMessageBox.information(self, '提交成功', '作战信息已提交')

        except Exception as e:
            QMessageBox.critical(self, '错误', f'提交失败: {str(e)}')


if __name__ == '__main__':
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
    app = QApplication(sys.argv)
    window = MainPage()
    sys.exit(app.exec_())