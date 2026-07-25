import json

def LoadFile (fileName):
    """ 从json文件中加载数据
    filename 是绝对路径
    return data 是以list形式存放的KO，每个ko是一个字典对象
    """
    data = []
    with open(fileName, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def SaveFile (fileName, data):
    """ 把知识对象存进文件
    filename 是绝对路径
    data 是以list形式存放的KO
    """
    koList = []
    for ite in data:
        koList.append(ite.body)
    with open(fileName, 'w', encoding='utf-8') as f:
        json.dump(koList, f, ensure_ascii=False)
