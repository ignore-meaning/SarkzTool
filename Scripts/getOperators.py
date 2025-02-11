import requests
import JsFunctions
import mwparserfromhell
import os
import time
url = "https://prts.wiki/api.php"   # prts 站点提供的 api 接口



'''
operatorInformation(operatorName)：调用 api 接口返回一个干员的信息（干员名为 operatorName）。
addOperator(operatorName)：向 operatorData.json 文件中增加一个干员（干员名为 operatorName）的信息
'''
def operatorInformation(operatorName:str='阿米娅') -> dict:
    params = {
        "action": "query",
        "format": "json",
        "titles": operatorName,
        "prop": "revisions",
        "rvprop": "content",
    }
    response = requests.get(url, params=params)
    data = response.json()
    pages = data['query']['pages']
    for page_id in pages:
        page = pages[page_id]
        if 'revisions' in page:
            content = page['revisions'][0]['*']
            break
    parsed = mwparserfromhell.parse(content)

    templates = parsed.filter_templates()
    for template in templates:
        if template.name.strip()[:10] == 'CharinfoV2':
            rarity = template.get("稀有度").value.strip()
            profession = template.get("职业").value.strip()
            break
    result = {
        operatorName: {
            '稀有度': int(rarity),
            '职业': profession
        }
    }
    return result

def addOperator(operatorName:str='凯尔希'):
    operatorData = JsFunctions.read('operatorData')
    operatorData.update(operatorInformation(operatorName))
    JsFunctions.write('operatorData',operatorData)



'''
allOperatorName()：获取一个 由明日方舟所有干员名称组成的 列表。可以通过选择取消注释其中几行来顺带执行 “向 operatorData.json 文件写入该列表” 的功能
addAllOperatorInformation()：根据 operatorData.json 中的全干员获取所有干员的信息并记录在 operatorData.json 中（调用 API 不能太过频繁，此处限制为 2 秒一次，可以更改）
allSortedOperatorName()：将干员按照游戏内的顺序排好（含精二）
'''
def allOperatorName() -> list:
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'categorymembers',
        'cmtitle': 'category:干员',
        'cmlimit': 500
    }
    response = requests.get(url, params)
    data = response.json()

    operator_names = [member['title'] for member in data['query']["categorymembers"]]
    operator_pageid = [member['pageid'] for member in data['query']["categorymembers"]]

    # 可以通过注释下面三行来取消写入 operatorData.json 文件
    operatorData = JsFunctions.read('operatorData')
    operatorData.update({'全干员': operator_names})
    JsFunctions.write('operatorData',operatorData)

    return operator_names

def addAllOperatorInformation():
    operatorData = JsFunctions.read('operatorData')
    operator_names = operatorData["全干员"]
    addedOperators = []

    for operatorName in operator_names:
        if not(operatorName in operatorData):
            addOperator(operatorName)   # 这个操作其实挺愚蠢的。每添加一个干员都要重新读取 operatorData.json 一遍
            addedOperators.append(operatorName)
            time.sleep(2)   # 可以更改调用 API 的间隔时间
    return addedOperators

def allSortedOperatorName() -> list:
    proCom = {'先锋':0, '近卫':1, '狙击':2, '重装':3, '医疗':4, '辅助':5, '术师':6, '特种':7}
    list0 = []
    for i in range(6):
        list0.append([])
    for i in range(6):
        for j in range(8):
            list0[i].append([])

    operatorData = JsFunctions.read('operatorData')
    operator_names = operatorData['全干员']

    for operatorName in operator_names:
        rarity = operatorData[operatorName]['稀有度']
        profession = operatorData[operatorName]['职业']
        list0[5-rarity][proCom[profession]].append(operatorName)
    
    list1=[]
    for i in range(6):
        for j in range(8):
            list1 += list0[i][j]

    list2 = []
    for operatorName in list1:
        list2.append(operatorName)
        if operatorData[operatorName]['稀有度'] >= 3: list2.append(operatorName + '_2')
    
    operatorData.update({'全干员排序': list2})
    JsFunctions.write('operatorData', operatorData)

    return list2

def availableOperators() -> list:
    filePath = os.path.join(os.path.dirname(__file__), '../img/operators/')

    operators = os.listdir(filePath)

    operatorData = JsFunctions.read('operatorData')
    operator_full = operatorData['全干员排序']

    operators = list(filter(lambda operatorName: '头像_'+operatorName+'.png' in operators, operator_full))

    operatorData.update({'可用干员': operators})
    JsFunctions.write('operatorData',operatorData)
    return operators