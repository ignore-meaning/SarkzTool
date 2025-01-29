# 该程序基本没有可扩展性，也没有任何自定义样式，因此仅作为前期过渡使用
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import JsFunctions

# 干员池、藏品池与作战，目前直接手敲进了 python 文件里，之后应该要单独写一个程序通过读取 img 文件夹的信息自动获得列表
operator_list = ['阿米娅(近卫)_2','承曦格雷伊_2','铎铃_2','菲莱_2','古米','古米_2','寒芒克洛丝_2','赫默_2','卡达','凯尔希_2','砾','魔王_2','桑葚_2','深律_2','桃金娘','巫恋_2','稀音_2','锡人_2','晓歌_2','伊桑','陨星_2']
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

class MainPage(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()
        
    
    def initUI(self):
        self.setWindowTitle('萨卡兹肉鸽奇妙小工具')
        self.setWindowIcon(QIcon('img/operators/头像_凯尔希_2.png'))
        
        # 此处定义 垂直布局 self.vbox 和 水平布局 self.hbox 嵌套使用。页面下 2/3 的部分给了 self.bottom_midpage1 和 self.bottom_midpage2（用来盛放信息框，显示选择的干员与藏品）
        self.vbox = QVBoxLayout(self)
        self.above_midpage = QWidget()
        self.bottom_midpage1 = QTextBrowser()
        self.bottom_midpage2 = QTextBrowser()
        self.vbox.addWidget(self.above_midpage)
        self.vbox.addWidget(self.bottom_midpage1)
        self.vbox.addWidget(self.bottom_midpage2)

        self.hbox = QHBoxLayout(self.above_midpage)

        '''
        此处定义了 6 个部件，分别为：
        self.Level_box，下拉式菜单，用于选择“层数”
        self.Operation_box，单行输入框，用于输入“关卡名”
        self.operator_button，按钮，用于打开选择干员的子页面；绑定至 self.openOperatorPage 函数，用于打开子页面
        self.treasure_button，按钮，用于打开选择藏品的子页面；绑定至 self.openTreasurePage 函数，用于打开子页面
        self.Era_box，下拉式菜单，用于选择“年代”
        self.Submit_button，按钮，用于提交“作战”；绑定至 self.Submit 函数，用于提交作战
        '''
        self.Level_box = QComboBox()
        self.Level_box.addItems(['1','2','3','4','5','6'])
        self.Operation_box = QComboBox()
        self.Operation_box.addItems(operation_list['1'])
        self.Level_box.currentTextChanged.connect(self.LevelChange)
        self.emergency_box = QCheckBox('紧急？')
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
        self.hbox.addWidget(self.emergency_box)
        self.hbox.addWidget(self.operator_button)
        self.hbox.addWidget(self.treasure_button)
        self.hbox.addWidget(self.Era_box)
        self.hbox.addWidget(self.Submit_button)

        # 创建两个子页面 self.operator_page 和 self.treasure_page
        self.operator_page = SonPage('干员', self)
        self.treasure_page = SonPage('藏品', self)

        # 定义两个列表，分别用于存放 选择的干员 与 选择的藏品
        self.collectedOperator = []
        self.collectedTreasure = []

    def LevelChange(self):
        self.Operation_box.clear()
        self.Operation_box.addItems(operation_list[self.Level_box.currentText()])

    def Text1Change(self):
        # 更新第一个文本框的内容
        self.collectedOperator = []
        for i in range(len(operator_list)):
            if self.operator_page.layout_list[i].isChecked():
                self.collectedOperator.append(operator_list[i])
        self.bottom_midpage1.setText(str(self.collectedOperator))

    def Text2Change(self):
        # 更新第二个文本框的内容
        self.collectedTreasure = []
        for i in range(len(treasure_list)):
            if self.treasure_page.layout_list[i].isChecked():
                self.collectedTreasure.append(treasure_list[i])
        self.bottom_midpage2.setText(str(self.collectedTreasure))
    
    def openOperatorPage(self):
        self.operator_page.show()   # 打开干员选择子页面
    
    def openTreasurePage(self):
        self.treasure_page.show()   # 打开藏品选择子页面

    def Submit(self):
        JsFunctions.add_operation(int(self.Level_box.currentText()), ('','紧急')[self.emergency_box.isChecked()] + self.Operation_box.currentText(), self.collectedOperator, self.collectedTreasure, self.Era_box.currentText()) # 调用 JsFunctions 的函数提交作战

class SonPage(QDialog):
    # 子页面所属的类
    def __init__(self, type, father):   # type 决定了实体化的子页面到底是“干员子页面”还是“藏品子页面”；father 参数使得子页面也可以调用父页面里的变量或函数
        super().__init__()
        self.layout_list = []       # 一种取巧的方式。子页面要呈现许多干员或藏品以供选择，因此选择 QGridLayout 布局。为了不给每一个选项小部件都起名字，直接用一个列表把它们装起来。
        self.type = type
        self.father = father
        self.initUI()
        for unit in self.layout_list:
            unit.toggled.connect(self.pp)   # self.layout_list 列表中的元素为许多 QCheckBox，给它们所有添加上一个事件监视器（当选择发生变动时调用 self.pp 函数，也就是改变父页面的两个文本框里的内容）
    
    def initUI(self):
        self.setWindowTitle(self.type)
        self.grid= QGridLayout(self)
        if self.type == '干员':
            self.grid_setlayout(operator_list)
            self.setWindowIcon(QIcon('img/operators/头像_阿米娅(近卫)_2.png'))
        elif self.type == '藏品':
            self.grid_setlayout(treasure_list)
            self.setWindowIcon(QIcon('img/treasures/国王的新枪.png'))
    
    def grid_setlayout(self,content:list):
        # 用于设置布局
        n = len(content)
        m = n//5 + 1
        self.layout_list = []
        for i in range(m):
            j = 0
            while i*5 + j + 1 <= n and j <= 4:
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