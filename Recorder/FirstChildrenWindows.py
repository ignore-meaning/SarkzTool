from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
from common import Buttons,Data_list
img_path = os.path.join(os.path.dirname(__file__), '../img/')
class FirstChildrenWindow(QDialog):
    selection_changed = pyqtSignal(list)  # 新增选择变更信号

    def __init__(self, window_type, content_list, parent=None):
        super().__init__(parent)
        self.window_type = window_type
        self.content_list = content_list
        self.imagebuttons = []  # 更明确的命名

        self.init_ui()
        self.setup_grid_layout()
        self.setWindowModality(Qt.NonModal)  # 设置为非模态窗口

    def init_ui(self):
        self.setWindowTitle(self.window_type)
        self.setMinimumSize(600, 400)

        # 主布局
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)  # 添加边距
        self.grid_layout.setHorizontalSpacing(15)  # 水平间距
        self.grid_layout.setVerticalSpacing(10)  # 垂直间距

        # 设置图标
        icon_path = {
            '干员': os.path.join(img_path, 'operators/头像_阿米娅(近卫)_2.png'),
            '藏品': os.path.join(img_path, 'treasures/国王的新枪.png')
        }.get(self.window_type, '')
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))

    def setup_grid_layout(self):
        """初始化网格布局"""
        self.clear_layout()

        # 每行显示5个项目
        columns = 5
        for index, content in enumerate(self.content_list):
            row = index // columns
            col = index % columns
            icon_path = self.get_icon_path(content)
            imagebuton = Buttons.ImageButton(icon_path,content)
            imagebuton.clicked.connect(self.emit_selection_changed)  # 连接信号

            self.grid_layout.addWidget(imagebuton, row, col, Qt.AlignCenter)
            self.imagebuttons.append(imagebuton)

    def get_icon_path(self, content):
        """获取图标路径"""
        operator_path='operators/头像_' + content + '.png'
        treasure_path='treasures/'+ content +'.png'
        base_path = {
            '干员': os.path.join(img_path, operator_path),
            '藏品': os.path.join(img_path, treasure_path)
        }
        return base_path[self.window_type]

    def emit_selection_changed(self):
        """发射选择变更信号"""
        selected = [self.content_list[i]
                    for i, ib in enumerate(self.imagebuttons) if ib.is_checked()]
        self.selection_changed.emit(selected)

    def clear_layout(self):
        """清空布局"""
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if widget := item.widget():
                widget.deleteLater()

    def reset(self):
        """重置选中状态"""
        # 获取当前应选中的项
        if self.window_type == "干员":
            selected_names = Data_list.DataList.selected_operators
        elif self.window_type == "藏品":
            selected_names = Data_list.DataList.selected_treasures
        else:
            selected_names = []

        # 遍历所有按钮，直接设置状态
        for ib in self.imagebuttons:
            is_selected = ib.get_name() in selected_names
            if (is_selected and not ib.is_checked()) or (not is_selected and ib.is_checked()) :
               ib.click()
        if self.window_type == "干员":
            Data_list.DataList.selected_operators = selected_names
        elif self.window_type == "藏品":
            Data_list.DataList.selected_treasures = selected_names




    # def get_selected_items(self):
    #     """获取当前选中项"""
    #     return [self.content_list[i]
    #             for i, cb in enumerate(self.checkboxes) if cb.isChecked()]