import sys
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QApplication,QHBoxLayout

class CustomDialog(QDialog):
    def __init__(self, title , content , parent=None):
        super(CustomDialog, self).__init__(parent)

        # 设置对话框标题
        self.setWindowTitle(title)

        # 创建标签
        self.label = QLabel(content, self)


        # 创建确定和取消按钮
        self.ok_button = QPushButton("确定", self)
        self.cancel_button = QPushButton("取消", self)

        # 连接按钮的点击事件到槽函数
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # 创建布局并添加控件
        main_layout = QVBoxLayout()

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.ok_button)
        bottom_layout.addWidget(self.cancel_button)

        main_layout.addWidget(self.label)
        main_layout.addLayout(bottom_layout)

        # 设置对话框的布局
        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建并显示自定义对话框
    dialog = CustomDialog("标题","问题?")
    if dialog.exec_() == QDialog.Accepted:
        print(1)
    else:
        print(2)

    sys.exit(app.exec_())