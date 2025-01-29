import json
filename = "operationData.json"



'''
read()：读取 operationData.json 文件内容并翻译为 python 能理解的对象（大概是字典）并返回。
write(content)：将 python 对象（大概是字典） content 翻译为 json 内容并覆写 operationData.json 文件
rewrite()：将 operationData.json 文件用自己本身的内容覆写一遍（用于统一格式）
'''
def read():
    with open(filename, "r", encoding="utf-8") as OPD_F:
        return json.load(OPD_F)

def write(content):
    with open(filename, "w", encoding="utf-8") as OPD_F:
        json.dump(content, OPD_F, ensure_ascii=False, indent=4)
    return

def rewrite():
    content = read()
    write(content)
    return

def clear():
    write({})
    return




'''
subsetQ(list1,list2)：判断列表 list1 是否为 list2 的“子集”（即前者的元素也是后者的元素，不考虑顺序）。空集是任意集合（包括另一个空集）的子集。返回值为 True 或 False。

add_operation(level, operation_name, operator_list, treasure_list)：
    向 operationData.json 文件中添加作战记录，所需参数分别为：
        作战层数 level；
        作战名 operation_name；
        干员列表 operator_list；
        藏品列表 treasure_list；
        年代名称 era
    向 operationData.json 文件中添加作战记录会考虑以下情形：
        若该关卡尚未被创建过，这次会创建该关卡；
        若 operationData.json 文件中已经有了更优记录（用更少的干员，更少的藏品），则这次的作战记录不会被添加（若消耗的时间过长，该功能可以被关闭）
'''
def subsetQ(list1:list, list2:list) -> bool:
    m,n = len(list1), len(list2)
    if m == 0:
        return True
    elif n == 0:
        return False
    else:
        for i in range(m):
            for j in range(n):
                if list1[i] == list2[j]:
                    break
                if j == n-1:
                    return False
        return True

def add_operation(level:int, operation_name:str, operator_list:list, treasure_list:list, era:str):
    content = read()
    LevelStr="Level %d"%(level)
    if not(LevelStr in content):
        content[LevelStr] = {}
    if not(operation_name in content[LevelStr]):
        content[LevelStr][operation_name] = []
    operation_list = content[LevelStr][operation_name]
    flag = True
    for operation in operation_list:    # 若想取消“判断是否存在更优记录”的功能，将该 for 循环语句注释掉即可
        if operation["年代"] == era and subsetQ(operation['干员'], operator_list) and subsetQ(operation['藏品'], treasure_list):
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
    write(content)
    return