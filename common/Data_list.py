from Scripts import JsFunctions


class DataList:
    selected_operators = []
    selected_treasures = []
    operator_list = JsFunctions.read('operatorData')['可用干员']
    treasure_list = JsFunctions.read('treasureData')['可用藏品']
    mission_list = JsFunctions.read('missionData')
