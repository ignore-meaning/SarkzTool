import json
filename = "operationData.json"



'''
read()：读取 json 文件内容并翻译为 python 对象
write(content)：将 python 对象（大概是字典） content 翻译为 json 内容并覆写 json 文件
rewrite()：将 json 文件用自己本身的内容覆写（用于统一格式）
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




'''
add_operation(level, operation_name, operator_list, treasure_list)：
    向 json 文件中添加作战记录。作战层数 level；作战名 operation_name；干员列表 treasure_list；年代名称 era
'''
def add_operation(level:int, operation_name:str, operator_list:list, treasure_list:list, era:str):
    content = read()
    LevelStr="Level%d"%(level)
    if not(LevelStr in content):
        content[LevelStr] = {}
    if not(operation_name in content[LevelStr]):
        content[LevelStr][operation_name] = []
    operation = content[LevelStr][operation_name]
    operation.append(
        {
            "干员": operator_list,
            "藏品": treasure_list,
            "年代": era
        }
    )
    write(content)
    return