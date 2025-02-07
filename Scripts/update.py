import JsFunctions
import getOperators



def main():
    print('\n请选择进行的业务:\n1.作战数据更新\n2.干员数据更新\n3.藏品数据更新\n4.查看操作记录\n5.清除操作记录\n按 E 退出程序')

    answer = input('>>')
    match answer:
        case 'E':
            exit()
        case '1':
            operationUpdate()
        case '2':
            operatorUpdate()
        case '3':
            treasureUpdate()
        case '4':
            for i in range(len(actionList)):
                print(f'{i+1}: {actionList[i]}')
        case '5':
            actionList.clear()

def operationUpdate():
    print('\n请选择操作:\n1.用 operationData_draft.json 中的内容覆写 operationData.json\n2.将 operationData_draft.json 中的作战添加至 operationData.json\n3.清空 operationData_draft.json 文件\n4.清空 operationData.json 文件（慎用！很难反悔）\n按 e 返回主界面')
    answer = input('>>')
    match answer:
        case 'e':
            return
        case '1':
            JsFunctions.transfer('operationData_draft', 'operationData')
            actionList.append('作战覆写')
        case '2':
            JsFunctions.renovate('operationData_draft', 'operationData')
            actionList.append('作战更新')
        case '3':
            JsFunctions.clear('operationData_draft')
            actionList.append('清除临时作战数据')
        case '4':
            JsFunctions.clear('operationData')
            actionList.append('清除作战数据')
        case _:
            operationUpdate()

def operatorUpdate():
    print('\n请选择操作:\n1.向 PRTS 查询当前游戏实装的干员名单\n2.向 PRTS 查询所有干员的基础信息（最坏情况预计耗时 10 分钟）\n3.根据干员信息将所有干员进行排序（区分精二与否）\n4.根据 img 文件夹下的文件获取当前可用的干员\n5.一条龙服务！\n按 e 返回主界面')
    answer = input('>>')
    match answer:
        case 'e':
            return
        case '1':
            print('全干员:', getOperators.allOperatorName())
            actionList.append('更新全干员')
        case '2':
            addedOperators = getOperators.addAllOperatorInformation()
            print('添加的干员有', addedOperators)
            actionList.append('更新干员信息')
        case '3':
            print('全干员排序:', getOperators.allSortedOperatorName())
            actionList.append('更新全干员排序')
        case '4':
            print('可用干员:', getOperators.availableOperators())
            actionList.append('更新可用干员')
        case '5':
            getOperators.allOperatorName()
            getOperators.addAllOperatorInformation()
            getOperators.allSortedOperatorName()
            getOperators.availableOperators()
            actionList.append('干员更新一条龙')
        case _:
            operatorUpdate()

def treasureUpdate():
    print('\n尚未开发')



actionList = []
print('欢迎使用“萨卡兹肉鸽奇妙小工具”数据库更新程序')
while True:
    main()