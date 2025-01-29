import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import JsFunctions

operator_list = ['阿米娅(近卫)_2','承曦格雷伊_2','铎铃_2','菲莱_2','古米_2','寒芒克洛丝_2','赫默_2','卡达','凯尔希_2','砾','魔王_2','桑葚_2','深律_2','桃金娘','巫恋_2','稀音_2','锡人_2','晓歌_2','伊桑','陨星_2']
treasure_list = ['国王的铠甲','国王的新枪','国王的延伸','轰鸣之手','诸王的冠冕']

class MainPage(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()
        
    
    def initUI(self):
        self.setWindowTitle('萨卡兹肉鸽奇妙小工具')
        self.setWindowIcon(QIcon('img/operators/头像_魔王_2.png'))
        self.vbox = QVBoxLayout(self)
        self.above_midpage = QWidget()
        self.bottom_midpage1 = QTextBrowser()
        self.bottom_midpage2 = QTextBrowser()
        self.vbox.addWidget(self.above_midpage)
        self.vbox.addWidget(self.bottom_midpage1)
        self.vbox.addWidget(self.bottom_midpage2)

        self.hbox = QHBoxLayout(self.above_midpage)

        self.Level_box = QComboBox()
        self.Level_box.addItems(['1','2','3','4','5','6'])
        self.Level_box.currentIndexChanged.connect(self.Text1Change)
        self.Operation_box = QLineEdit()
        self.operator_button = QPushButton('干员')
        self.operator_button.clicked.connect(self.openOperatorPage)
        self.treasure_button = QPushButton('藏品')
        self.treasure_button.clicked.connect(self.openTreasurePage)
        self.Era_box = QComboBox()
        self.Era_box.addItems(['无','天灾年代','魔王年代','苦难年代','奇观年代','拥挤年代'])
        self.Submit_button = QPushButton('提交')
        self.Submit_button.clicked.connect(self.Submit)

        self.hbox.addWidget(self.Level_box)
        self.hbox.addWidget(self.Operation_box)
        self.hbox.addWidget(self.operator_button)
        self.hbox.addWidget(self.treasure_button)
        self.hbox.addWidget(self.Era_box)
        self.hbox.addWidget(self.Submit_button)

        self.operator_page = SonPage('干员', self)
        self.treasure_page = SonPage('藏品', self)
        self.collectedOperator = []
        self.collectedTreasure = []

    def Text1Change(self):
        self.collectedOperator = []
        for i in range(len(operator_list)):
            if self.operator_page.layout_list[i].isChecked():
                self.collectedOperator.append(operator_list[i])
        self.bottom_midpage1.setText(str(self.collectedOperator))

    def Text2Change(self):
        self.collectedTreasure = []
        for i in range(len(treasure_list)):
            if self.treasure_page.layout_list[i].isChecked():
                self.collectedTreasure.append(treasure_list[i])
        self.bottom_midpage2.setText(str(self.collectedTreasure))
    
    def openOperatorPage(self):
        self.operator_page.show()
    
    def openTreasurePage(self):
        self.treasure_page.show()

    def Submit(self):
        self.Text1Change()
        self.Text2Change()
        JsFunctions.add_operation(int(self.Level_box.currentText()), self.Operation_box.text(), self.collectedOperator, self.collectedTreasure, self.Era_box.currentText())

class SonPage(QDialog):
    def __init__(self,type,father):
        super().__init__()
        self.layout_list = []
        self.type = type
        self.father = father
        self.initUI()
        for unit in self.layout_list:
            unit.toggled.connect(self.pp)
    
    def initUI(self):
        self.setWindowTitle(self.type)
        self.grid= QGridLayout(self)
        if self.type == '干员':
            self.grid_setlayout(operator_list)
        elif self.type == '藏品':
            self.grid_setlayout(treasure_list)
    
    def grid_setlayout(self,content:list):
        n = len(content)
        m = n//5 + 1
        self.layout_list = []
        for i in range(m):
            j = 0
            while i*5 + j + 1 <= n:
                self.layout_list.append(QCheckBox(self))
                if self.type == '干员':
                    address = 'img/operators/头像_'+content[i*5+j]+'.png'
                elif self.type == '藏品':
                    address = 'img/treasures/'+content[i*5+j]+'.png'
                self.layout_list[i*5+j].setIcon(QIcon(address))
                self.layout_list[i*5+j].setIconSize(QSize(60, 60))
                self.grid.addWidget(self.layout_list[i*5+j],i,j)
                j += 1
    
    def pp(self):
        self.father.Text1Change()
        self.father.Text2Change()


app = QApplication([])
w = MainPage()

sys.exit(app.exec_())