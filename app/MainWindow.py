import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from app.FirstChildrenWindows import FirstChildrenWindow
from Scripts import JsFunctions

operator_list = ['阿米娅_2','阿米娅(近卫)_2','阿米娅(医疗)_2','承曦格雷伊_2','铎铃_2','菲莱_2','古米','古米_2','寒芒克洛丝_2','赫默_2','卡达','凯尔希_2','砾','迷迭香','迷迭香_2','魔王_2','桑葚_2','深律_2','石英','桃金娘','巫恋_2','稀音_2','锡人_2','晓歌_2','伊桑','陨星_2','火海','离迁','侵略','兴亡']
treasure_list = ['国王的铠甲','国王的新枪','国王的延伸','轰鸣之手','诸王的冠冕']
operation_list = {
    '1': ['坏邻居','公害','安全检查','夺路而逃','冰川期'],
    '2': ['见闻峰会','拆东补西','排风口','炉工志愿队','有序清场','卡兹瀑布','丛林密布'],
    '3': ['大旗一盘','血脉之辩','遮天蔽日','劳作的清晨','溃乱魔典','盲盒商场','火力小队','机动队','守望的河水','卫士不语功','存亡之战','或然面纱','奉献','斩首','离歌的庭院','赴敌者','王冠之下'],
    '4': ['年代断层','朽败考察','飞越大水坑','腥红甬道','现代战争法则','假想对冲','幽灵城','神出鬼没','混沌','争议频发'],
    '5': ['寄人城池下','计划耕种','巫咒同盟','通道封锁','无罪净土','浮空城接舷战','残破学院','建制','莱茵卫士','紧急授课','朝谒','思维纠正','魂灵朝谒'],
    '6': ['谋求共识','神圣的渴求','洞天福地','外道','圣城','授法','不容拒绝'],
    '7': ['不容拒绝']
}


class MainWindow(QMainWindow):  # 类名改为 PascalCase 规范

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setWindowTitle('萨卡兹肉鸽奇妙小工具')
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), '../img/operators/头像_凯尔希_2.png')))  # 改为相对当前文件的路径

        # 创建中央部件和主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)  # 添加边距
        main_layout.setSpacing(10)  # 设置间距

        # 上部控件布局
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)

        # 初始化控件
        self.level_combo = QComboBox()
        self.level_combo.addItems(['1', '2', '3', '4', '5', '6'])

        self.operation_combo = QComboBox()
        self.operation_combo.addItems(operation_list['1'])

        self.emergency_check = QCheckBox('紧急')
        self.operator_btn = QPushButton('干员')
        self.treasure_btn = QPushButton('藏品')
        self.era_combo = QComboBox()
        self.era_combo.addItems(['无', '天灾年代', '魔王年代', '苦难年代', '奇观年代', '拥挤年代'])
        self.submit_btn = QPushButton('提交')

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
        self.operator_display.setMaximumHeight(80)
        self.treasure_display = QTextBrowser()
        self.treasure_display.setMaximumHeight(80)

        # 添加所有部件到主布局
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.operator_display)
        main_layout.addWidget(self.treasure_display)

        # 信号连接
        self.level_combo.currentTextChanged.connect(self.update_operations)
        self.operator_btn.clicked.connect(self.show_operator_window)
        self.treasure_btn.clicked.connect(self.show_treasure_window)
        self.submit_btn.clicked.connect(self.submit_operation)

        # 初始化子窗口
        self.operator_window = FirstChildrenWindow('干员', operator_list, self)
        self.operator_window.selection_changed.connect(self.update_operator_display)

        self.treasure_window = FirstChildrenWindow('藏品', treasure_list, self)
        self.treasure_window.selection_changed.connect(self.update_treasure_display)

        # 初始化选择列表
        self.selected_operators = []
        self.selected_treasures = []

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

            if not operation:
                raise ValueError("请选择关卡")

            JsFunctions.add_operation(
                level=level,
                operation=operation,
                operators=self.selected_operators,
                treasures=self.selected_treasures,
                era=era
            )
            QMessageBox.information(self, '提交成功', '作战信息已提交')

        except Exception as e:
            QMessageBox.critical(self, '错误', f'提交失败: {str(e)}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())