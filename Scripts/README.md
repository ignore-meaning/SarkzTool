## 文件介绍

* JsFunctions.py：与 .json 文件交互的函数

* getOperators.py：通过 PRTS 的 API 获取所有干员的基础信息（名称、稀有度、职业）；通过读取 img/operators/ 下文件的名称获取可选干员名单（按游戏内规则排序）；将上面两条的结果存入 operatorData.json 文件

## 可外部调用的函数

### JsFunctions.py

#### read(filename)

读取对应 .json 文件的内容并将其翻译为 python 可理解的内容（字典或列表）

参数：

* `filename`：字符串，用于选择读取的 .json 文件。可选值为 `'operationData'`、`'operationData_draft'`、`'operatorData'` 和 `'treasureData'`，分别用于读取对应的 .json 文件

#### add_operation(level, operation_name, operator_list, treasure_list, era)

向 operationData_draft.json 中添加一个作战

参数：

* `level`：关卡的层数，数据类型为整形

* `operation_name`：关卡的名字，数据类型为字符串

* `operator_list`：所用干员名字组成的列表（请先行排好序）

* `treasure_list`：所用藏品名字组成的列表（请先行排好序）（思绪也被看作是一个藏品）

* `era`：所遭遇的年代，数据类型为字符串

例子：`add_operation(3,'存亡之战',['迷迭香_2'],['轰鸣之手','金酒之杯'],'苦难年代')`

### getOperators.py

#### availableOperators()

通过比对 img 文件夹下的文件名与 operatorData.json 所储存的全干员信息，计算当前可选的所有干员（按游戏内规则排序），存入 operatorData.json 文件并返回

注：推荐使用 `JsFunctions.read('operatorData')['可用干员']` 而非该函数来读取可用干员




