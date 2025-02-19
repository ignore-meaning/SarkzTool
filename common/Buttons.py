from PyQt5.QtWidgets import QPushButton, QCheckBox, QApplication
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor
from PyQt5.QtCore import Qt, QSize
import os
class CustomButton(QPushButton):
    def __init__(self, text,  parent=None):
        super().__init__(text, parent)

        # 设置按钮的初始样式
        self.setStyleSheet("""
            QPushButton {
                background-color:white;
                color: black; /* 文字颜色 */
                border: 1px solid gray; /* 黑色边框 */
                padding: 10px 20px; /* 内边距 */
                font-size: 20px; /* 字体大小 */
                border-radius: 5px;

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
        self.setFixedSize(125, 50)  # 宽度 200，高度 50


class ImageButton(QPushButton):
    def __init__(self, image_path,image_name):
        super().__init__()
        self.name=image_name
        self.normal_pixmap = QPixmap(image_path)
        if self.normal_pixmap.isNull():
            raise ValueError("Invalid image file path")

        self.dark_pixmap = self._create_dark_pixmap()
        self._setup_ui()
        self._connect_signals()
        # 设置鼠标悬停时的光标样式为手型
        self.setCursor(Qt.PointingHandCursor)

    def get_name(self):
        return self.name

    def _setup_ui(self):
        # Resize the image to 50x50 px
        resized_pixmap = self.normal_pixmap.scaled(75, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setIcon(QIcon(resized_pixmap))
        self.setIconSize(resized_pixmap.size())
        self.setFixedSize(resized_pixmap.size())  # Set the button size to the resized image size
        self.setStyleSheet("QPushButton { border: none; }")

        # 创建并配置复选框
        self.checkbox = QCheckBox(self)
        self.checkbox.setFocusPolicy(Qt.NoFocus)
        checked_path=os.path.join(os.path.dirname(__file__), '../img/checked.png')
        checked_path = os.path.normpath(checked_path)  # 规范化路径
        checked_path = checked_path.replace('\\', '/')  # 将反斜杠转换为正斜杠
        self.checkbox.setStyleSheet(f"""
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid #999;
            }}
            QCheckBox::indicator:checked{{
                background: transparent;
                border: 1px solid #999;
                image:url({checked_path});
            }}
            QCheckBox {{
                background: transparent;
            }}
        """)
        self._update_checkbox_position()

    def _create_dark_pixmap(self):
        """创建变暗后的图片版本"""
        dark_pixmap = QPixmap(self.normal_pixmap.size())
        dark_pixmap.fill(Qt.transparent)

        painter = QPainter(dark_pixmap)
        painter.drawPixmap(0, 0, self.normal_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_Darken)
        painter.fillRect(self.normal_pixmap.rect(), QColor(0, 0, 0, 128))
        painter.end()

        return dark_pixmap

    def _update_checkbox_position(self):
        """更新复选框位置到右上角"""
        checkbox_size = self.checkbox.sizeHint()
        self.checkbox.move(
            self.width() - checkbox_size.width() - 2,  # 添加2像素边距
            2
        )

    def _connect_signals(self):
        """连接信号与槽"""
        self.clicked.connect(self.toggle_check_state)
        self.checkbox.stateChanged.connect(self._update_appearance)

    def resizeEvent(self, event):
        """重写大小改变事件处理"""
        super().resizeEvent(event)
        self._update_checkbox_position()

    def toggle_check_state(self):
        """切换复选框状态"""
        self.checkbox.setChecked(not self.checkbox.isChecked())

    def _update_appearance(self, state):
        """根据复选框状态更新显示"""
        if state:
            self.setIcon(QIcon(self.dark_pixmap))
        else:
            self.setIcon(QIcon(self.normal_pixmap))

    def is_checked(self):
        """返回当前选中状态"""
        return self.checkbox.isChecked()



# 使用示例
if __name__ == "__main__":
    import sys
    import os

    img_path = os.path.join(os.path.dirname(__file__), '../img/operators/头像_伊桑.png')

    app = QApplication(sys.argv)

    button = ImageButton(img_path,'伊桑')  # 替换为实际图片路径
    button.show()
    sys.exit(app.exec_())