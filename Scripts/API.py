import requests
import JsFunctions
import mwparserfromhell
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
allOperatorNmae()：获取一个 由明日方舟所有干员名称组成的 列表。可以通过选择取消注释其中几行来顺带执行 “向 operatorData.json 文件写入该列表” 的功能
addAllOperatorInformation()：根据 operatorData.json 中的全干员列表获取所有干员的信息并记录在 operatorData.json 中（调用 API 不能太过频繁，此处限制为 2 秒一次，可以更改）
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
    # content = JsFunctions.read('operatorData')
    # content.update({'全干员列表': operator_names})
    # JsFunctions.write('operatorData',content)

    return operator_names

def addAllOperatorInformation():
    content = JsFunctions.read('operatorData')
    operator_names = content["全干员列表"]

    for operatorName in operator_names:
        if not(operatorName in content):
            addOperator(operatorName)   # 这个操作其实挺愚蠢的。每添加一个干员都要重新读取 operatorData.json 一遍
            time.sleep(2)   # 可以更改调用 API 的间隔时间
    return

def allOperatorName_2() -> list:
    dictionary = {'先锋':0, '近卫':1, '狙击':2, '重装':3, '医疗':4, '辅助':5, '术师':6, '特种':7}
    result = []
    for i in range(6):
        result.append([])
    for i in range(6):
        for j in range(8):
            result[i].append([])

    content = JsFunctions.read('operatorData')
    operator_names = content['全干员列表']

    for operatorName in operator_names:
        rarity = content[operatorName]['稀有度']
        profession = content[operatorName]['职业']
        result[5-rarity][dictionary[profession]].append(operatorName)
    

    
    return result