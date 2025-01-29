import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


# 自定义 Label 类，继承自 QLabel
class CustomLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        # 设置 Label 的初始样式
        self.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0; /* 浅灰色背景 */
                color: black; /* 文字颜色 */
                //border: 2px solid #333; /* 深灰色边框 */
                padding: 10px; /* 内边距 */
                font-size: 16px; /* 字体大小 */
                border-radius: 5px; /* 圆角 */
                qproperty-alignment: AlignCenter; /* 文字居中 */
            }
        """)
        # 设置字体为粗体
        font = QFont()
        font.setBold(True)  # 设置为粗体
        self.setFont(font)



    # 添加 setFixedSize 方法
    def setFixedSize(self, width, height):
        super().setFixedSize(width, height)  # 调用父类的 setFixedSize 方法


# 主窗口类
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("Custom Label Example")
        self.setGeometry(100, 100, 300, 200)

        # 创建布局
        layout = QVBoxLayout()

        # 创建自定义 Label 实例
        custom_label = CustomLabel("干员列表：")

        # 设置 Label 的固定大小
        custom_label.setFixedSize(200, 50)  # 宽度 200，高度 50

        # 将 Label 添加到布局中
        layout.addWidget(custom_label)

        # 设置窗口的布局
        self.setLayout(layout)


# 主程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建主窗口实例
    window = MainWindow()
    window.show()

    # 运行应用程序
    sys.exit(app.exec_())