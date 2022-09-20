import random
import time
import json


class knowledgeObject:
    """知识对象"""
    # 在类的定义中，在函数之外定义的属性是静态属性，所有对象共享
    def __init__(self, body = {}, hl = []):
        # 在函数中用self定义的属性是私有属性
        self.body = {}
        self.body["context"] = ""                # 文本信息
        self.body["HL"] = []                     # 文本中的知识点
        self.HL = []                             # 文本中的知识点，也是 knowledgeObject 对象
        self.body["RT"] = [0, 0, 0, 0]           # 复习次数，分别对应[选择,听写,朗读,]
        self.body["CT"] = [0, 0, 0, 0]           # 做对次数，分别对应[选择,听写,朗读,]
        self.body["LT"] = [0.0, 0.0, 0.0, 0.0]   # 上一次复习的系统时间(s)，分别对应[听写,朗读,选择,]
        self.body["PS"] = 1                      # 优先级，PS = k * (当前时间 - LT)/ (CT + alpha) * RT
        self.body["k"] = 1                       # 默认为 1
        self.body["tags"] = {}                   # 字符串字典，用于分类
        self.body["audioPath"] = ""              # 音频路径
        self.body["videoPath"] = ""              # 视频路径
        self.body["imagePath"] = ""              # 图片路径
        self.body["contextExplanation"] = ""     # context 的翻译、解释等
        self.body["moreInfo"] = []               # 其他信息
        
        
        keys = body.keys()
        for k in keys :
            self.body[k] = body[k]
        self.HL = hl

    def UpdatePS (self, mode):
        currentTime = int(time.time())
        random.seed (currentTime)        
        ran = random.random() / 10
        self.body["PS"] = self.body["k"] * (currentTime - self.body["LT"][mode]) / (self.body["CT"][mode] + ran) * (self.body["RT"][mode] + 1)

    def UpdateLS (self):
        self.body["LT"][self.body["mode"]] = int(time.time())

    def UpdateRT (self, count = 0):
        self.body["RT"][self.body["mode"]] += count

    def UpdateCS (self, count = 0):
        self.body["CT"][self.body["mode"]] += count

    def ToString (self):
        str = json.dumps(self.body)
        return str
    


class knowledgeObjectList:
    """ 知识对象列表 """
    objectList = []  # 知识对象列表
    tags = []        # 分类的tag 列表
    mode = 0         # 0:选择（默认）; 1:朗读; 2:听写; ... 
    def compare(self, knowledgeobject):
        return knowledgeobject.body["PS"]

    def sortList (self, reverse = True):
        for ite in self.objectList:
            ite.UpdatePS(mode = self.mode)
        self.objectList.sort(key = self.compare, reverse = reverse)
        self.PrintList()

    def PrintList (self):
        # str = ''
        for ite in self.objectList:
        #     str+= ite.ToString() + '\n'
            print(ite.ToString())

