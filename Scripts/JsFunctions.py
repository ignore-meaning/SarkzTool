import json
import os
address = {
    'operationData_draft': os.path.join(os.path.dirname(__file__), '../data/operationData_draft.json'),
    'operationData': os.path.join(os.path.dirname(__file__), '../data/operationData.json'),
    'operatorData': os.path.join(os.path.dirname(__file__), '../data/operatorData.json'),
    'treasureData': os.path.join(os.path.dirname(__file__), '../data/treasureData.json'),
    'missionData': os.path.join(os.path.dirname(__file__), '../data/missionData.json')
}



'''
read(filename)：读取 address[filename] 文件的内容并翻译为 python 能理解的对象（大概是字典）并返回
write(filename, content)：将 python 对象（大概是字典） content 翻译为 json 内容并覆写 address[filename] 文件
rewrite(filename)：将 address[filename] 文件用自己本身的内容覆写一遍（用于统一格式）
transfer(file1, file2)：用文件 file1 的内容去覆写 file2 文件
'''
def read(filename:str='operationData_draft'):
    with open(address[filename], "r", encoding="utf-8") as OPD_F:
        return json.load(OPD_F)

def write(filename:str, content):
    with open(address[filename], "w", encoding="utf-8") as OPD_F:
        json.dump(content, OPD_F, ensure_ascii=False, indent=4)
    return

def rewrite(filename:str):
    content = read(filename)
    write(filename, content)
    return

def clear(filename:str):
    write(filename, {})
    return

def transfer(file1:str='operationData_draft', file2:str='operationData'):
    content = read(file1)
    write(file2, content)
    return




'''
subsetQ(list1, list2)：判断列表 list1 是否为 list2 的“子集”（即前者的元素也是后者的元素，不考虑顺序）。空集是任意集合（包括另一个空集）的子集。返回值为 True 或 False。
operatorSubsetQ(list1, list2)：判断两个干员列表的“子集关系”

add_operation(level, mission, operator_list, treasure_list)：
    向 operationData.json 文件中添加作战记录，所需参数分别为：
        作战层数 level；
        作战名 mission；
        干员列表 operator_list；
        藏品列表 treasure_list；
        年代名称 era
    向 operationData.json 文件中添加作战记录会考虑以下情形：
        若该关卡尚未被创建过，这次会创建该关卡；
        若 operationData.json 文件中已经有了更优记录（用更少的干员，更少的藏品），则这次的作战记录不会被添加（若消耗的时间过长，该功能可以被关闭）

renovate()：将 operationData_draft.json 中的作战添加至 operationData.json
feasibleMissions(operator_list, treasure_list, era)：根据干员列表 operator_list、藏品列表 treasure_list、年代 era 来获取所有当前打得过的关卡
'''
def subsetQ(list1:list, list2:list) -> bool:
    if len(list1) == 0:
        return True
    else:
        for i in list1:
            if not(i in list2):
                return False
        return True
    
def operatorSubsetQ(list1:list, list2:list) -> bool:
    if len(list1) == 0:
        return True
    else:
        for operator in list1:
            if operator[:3] == '阿米娅':
                rarity = ''
                if operator[-2:] == '_2':
                    rarity = '_2'
                profession_list = ['', '(近卫)', '(医疗)']
                amiya = ['阿米娅'+profession+rarity for profession in profession_list] + ['阿米娅'+profession+rarity+'_2' for profession in profession_list]
                flag = False
                for ami in amiya:
                    if ami in list2:
                        flag = True
                        break
                if flag == False:
                    return False
                continue
            if not(operator in list2 or operator+'_2' in list2):
                return False
        return True

def add_operation(level:int, mission:str, operator_list:list, treasure_list:list, era:str):
    content = read('operationData_draft')
    LevelStr="Level %d"%(level)
    if not(LevelStr in content):
        content[LevelStr] = {}
    if not(mission in content[LevelStr]):
        content[LevelStr][mission] = []
    operation_list = content[LevelStr][mission]
    flag = True
    for operation in operation_list:    # 若想取消“判断是否存在更优记录”的功能，将该 for 循环语句注释掉即可
        if operation["年代"] == era and operatorSubsetQ(operation['干员'], operator_list) and subsetQ(operation['藏品'], treasure_list):
            flag = False
            break
    if flag:
        operation_list.append(
            {
                "干员": operator_list,
                "藏品": treasure_list,
                "年代": era
            }
        )
    write('operationData_draft', content)
    return

def renovate():
    content1 = read('operationData_draft')
    content2 = read('operationData')
    levels = content1.keys()
    for level in levels:
        if not(level in content2):
            content2[level] = content1[level]
        else:
            missions = content1[level].keys()
            for mission in missions:
                if not(mission in content2[level]):
                    content2[level][mission] = content1[level][mission]
                else:
                    newOperations = content1[level][mission]
                    for newOperation in newOperations:
                        if not(newOperation in content2[level][mission]):
                            content2[level][mission].append(newOperation)
    write('operationData', content2)
    return

def feasibleMissions(operator_list:list, treasure_list:list, era:str) -> dict:
    feasibleMission_list = {'1':[],'2':[],'3':[],'4':[],'5':[],'6':[],'7':[]}
    operationData = read('operationData')
    for level_str in operationData:
        level = level_str.strip('Level ')
        missions = operationData[level_str]
        for mission in missions:
            operation_list = missions[mission]
            for operation in operation_list:
                operators = operation['干员']
                treasures = operation['藏品']
                eraQ = operation['年代']
                if operatorSubsetQ(operators, operator_list) and subsetQ(treasures, treasure_list) and eraQ == era and not(mission in feasibleMission_list[level]):
                    feasibleMission_list[level].append(mission)
    return feasibleMission_list