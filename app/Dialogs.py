import sys
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QApplication

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super(CustomDialog, self).__init__(parent)

        # 设置对话框标题
        self.setWindowTitle("自定义对话框")

        # 创建标签
        self.label = QLabel("请输入一些内容:", self)

        # 创建输入框
        self.input_line = QLineEdit(self)

        # 创建确定和取消按钮
        self.ok_button = QPushButton("确定", self)
        self.cancel_button = QPushButton("取消", self)

        # 连接按钮的点击事件到槽函数
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # 创建布局并添加控件
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_line)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        # 设置对话框的布局
        self.setLayout(layout)

    def get_input_text(self):
        # 返回输入框中的文本
        return self.input_line.text()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建并显示自定义对话框
    dialog = CustomDialog()
    if dialog.exec_() == QDialog.Accepted:
        print("用户输入的内容是:", dialog.get_input_text())
    else:
        print("用户取消了对话框")

    sys.exit(app.exec_())