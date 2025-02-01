import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QLabel

class CustomComboBox(QComboBox):
    def __init__(self, on_change, parent=None):
        super().__init__(parent)
        self.on_change = on_change
        self.currentIndexChanged.connect(self._on_change)

    def _on_change(self, index):
        # 调用传递进来的函数，并传递当前选中的索引和文本
        self.on_change(index, self.currentText())

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 创建一个自定义下拉框，选项改变时触发 self.on_combobox_change 方法
        self.combobox = CustomComboBox(self.on_combobox_change)
        self.combobox.addItem('Option 1')
        self.combobox.addItem('Option 2')
        self.combobox.addItem('Option 3')
        layout.addWidget(self.combobox)

        self.setLayout(layout)
        self.setWindowTitle('Custom ComboBox Example')
        self.show()

    def on_combobox_change(self, index, text):
        # 更新标签内容
        print(f'Selected: {text} (Index: {index})')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())