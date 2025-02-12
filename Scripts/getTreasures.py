import requests
import JsFunctions
import mwparserfromhell
import os
import time
url = "https://prts.wiki/api.php"   # prts 站点提供的 api 接口


'''
allTreasureName()：调用 API 获取所有的藏品与思绪（已排序）
availableTreasures()：根据 img 下的文件读取当前可用的藏品与思绪
'''
def allTreasureName() -> list:
    params = {
        "action": "query",
        "format": "json",
        "titles": '萨卡兹的无终奇语/想象实体图鉴',
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

    treasure_list = []
    templates = parsed.filter_templates()
    for template in templates:
        if template.name.strip() == '收藏品':
            treasure_list.append(template.get('名称').value.strip())
    

    params['titles'] = '萨卡兹的无终奇语/佚散思维辑录'
    response = requests.get(url, params=params)
    data = response.json()
    pages = data['query']['pages']
    for page_id in pages:
        page = pages[page_id]
        if 'revisions' in page:
            content = page['revisions'][0]['*']
            break
    
    parsed = mwparserfromhell.parse(content)
    sections = parsed.get_sections(include_headings=True)
    for section in sections:
        headings = section.filter_headings()
        for heading in headings:
            if heading.title.strip() == '灵感':
                parsed = section
    
    templates = parsed.filter_templates()
    for template in templates:
        if template.name.strip() == ':萨卡兹的无终奇语/思绪':
            treasure_list.append(template.get('名称').value.strip())

    treasureData = JsFunctions.read('treasureData')
    treasureData.update({'全藏品': treasure_list})
    JsFunctions.write('treasureData', treasureData)

    return treasure_list

def availableTreasures() -> list:
    filePath = os.path.join(os.path.dirname(__file__), '../img/treasures/')

    treasures = os.listdir(filePath)

    treasureData = JsFunctions.read('treasureData')
    treasure_full = treasureData['全藏品']

    treasures = list(filter(lambda treasureName: treasureName +'.png' in treasures, treasure_full))

    treasureData.update({'可用藏品': treasures})
    JsFunctions.write('treasureData',treasureData)
    return treasures