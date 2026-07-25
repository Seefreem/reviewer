import random
import os
from src.knowledgeObject import *
from src.loadAndSave import *
from src.vocabularyFile import create_vocabulary, load_vocabulary

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QLineEdit)
from PyQt5.QtWidgets import (QLabel, QFrame, QGridLayout, QTabWidget)
from PyQt5.QtWidgets import (QPlainTextEdit, QMessageBox, QTextEdit)
from PyQt5.QtWidgets import (QShortcut, QDialog, QDialogButtonBox)
from PyQt5.QtWidgets import (QFileDialog, QFormLayout)





"""class Row1():
    #------------------ 第一行
    def __init__(self):
        self.bt1 = QPushButton('全部')
        self.bt2 = QPushButton('Tag筛选')
        self.bt3 = QPushButton('新增知识点')
        self.lineEdit = QLineEdit("")
        self.bt4 = QPushButton('搜索')

        self.hbox = QHBoxLayout()
        # hbox.addStretch(1) # 空白填充，拉伸因子， 参数是QSpacerItem ，其实就是多个Stretch的时候的比例
        self.hbox.addWidget(self.bt1)
        self.hbox.addWidget(self.bt2)
        self.hbox.addWidget(self.bt3)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.lineEdit)
        self.hbox.addWidget(self.bt4)"""

class Row2():
    #------------------ 第二行
    def __init__(self, root):
        self.root = root
        self.btChoose = QPushButton('选择')
        self.btListen = QPushButton('听写')
        self.btRead = QPushButton('朗读')
        self.btSaveinFile = QPushButton('保存文件')
        self.btSaveinFile.clicked.connect(self.SaveInFile)

        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(self.btChoose)
        self.hbox2.addWidget(self.btListen)
        self.hbox2.addWidget(self.btRead)
        self.hbox2.addWidget(self.btSaveinFile)
        self.hbox2.addStretch(1)

    def SaveInFile(self):
        self.root.SaveCurrentVocabulary()


class NewVocabularyDialog(QDialog):
    """Collect the file and descriptive metadata for a new vocabulary book."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("新增单词本")

        self.filePath = QLineEdit()
        self.btBrowse = QPushButton("选择位置")
        self.btBrowse.clicked.connect(self.choosePath)
        fileLayout = QHBoxLayout()
        fileLayout.addWidget(self.filePath)
        fileLayout.addWidget(self.btBrowse)

        self.titleEdit = QLineEdit()
        self.descriptionEdit = QPlainTextEdit()
        self.sourceLanguageEdit = QLineEdit("English")
        self.targetLanguageEdit = QLineEdit("Chinese")
        self.tagsEdit = QLineEdit()
        self.tagsEdit.setPlaceholderText("多个标签用分号分隔")

        form = QFormLayout()
        form.addRow("文件", fileLayout)
        form.addRow("名称", self.titleEdit)
        form.addRow("描述", self.descriptionEdit)
        form.addRow("源语言", self.sourceLanguageEdit)
        form.addRow("目标语言", self.targetLanguageEdit)
        form.addRow("标签", self.tagsEdit)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Save).setText("创建")
        buttons.accepted.connect(self.validateAndAccept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def choosePath(self):
        defaultDirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        path, _ = QFileDialog.getSaveFileName(
            self,
            "新增单词本",
            defaultDirectory,
            "JSON 文件 (*.json)",
        )
        if path:
            if not path.lower().endswith(".json"):
                path += ".json"
            self.filePath.setText(path)
            if not self.titleEdit.text().strip():
                self.titleEdit.setText(os.path.splitext(os.path.basename(path))[0])

    def validateAndAccept(self):
        path = self.filePath.text().strip()
        if not path:
            QMessageBox.warning(self, "无法创建", "请选择新单词本的保存位置。")
            return
        if os.path.basename(path).endswith(".meta.json"):
            QMessageBox.warning(self, "无法创建", "文件名不能以 .meta.json 结尾。")
            return
        self.accept()

    def values(self):
        return self.filePath.text().strip(), {
            "title": self.titleEdit.text().strip(),
            "description": self.descriptionEdit.toPlainText().strip(),
            "sourceLanguage": self.sourceLanguageEdit.text().strip(),
            "targetLanguage": self.targetLanguageEdit.text().strip(),
            "tags": self.tagsEdit.text(),
        }

class Row3():
    #------------------ 第三行
    def __init__(self, root):
        self.root = root
        self.hbox3 = QHBoxLayout()
        self.hbox3_1 = QHBoxLayout()
        self.grid3_2 = QGridLayout()
        self.lableContext = QTextEdit('context')
        # self.lableContext.setLineWrapColumnOrWidth(100)
        self.lableContext.adjustSize()
        self.lableContext.setFrameStyle(QFrame.Panel) # | QFrame.Sunken
        
        self.lableContext.setFont(QtGui.QFont("Courier New", 15))
        self.hbox3_1.addWidget(self.lableContext)

        self.lableCorect = QLabel('CT:')
        self.lableReview = QLabel('RT:')
        self.btDelete = QPushButton('删除')
        self.btChange = QPushButton('修改')
        
        self.btDelete.clicked.connect(self.Delete)
        self.btChange.clicked.connect(self.Edit) 
        self.grid3_2.addWidget(self.lableCorect, 0, 0)
        self.grid3_2.addWidget(self.lableReview, 1, 0)
        self.grid3_2.addWidget(self.btDelete,    0, 1)
        self.grid3_2.addWidget(self.btChange,    1, 1)
        
        self.hbox3.addLayout(self.hbox3_1)
        # self.hbox3.addStretch(1)
        self.hbox3.addLayout(self.grid3_2)

    def Delete(self):
        root = self.root
        if not root.kol.objectList:
            return

        index = root.reviewIndex
        if index >= len(root.kol.objectList):
            index = len(root.kol.objectList) - 1

        del root.kol.objectList[index]

        if not root.kol.objectList:
            root.reviewIndex = 0
            root.correctNumber = -1
            if hasattr(root, "refreshDefaultTab"):
                root.refreshDefaultTab()
            if hasattr(root, "refreshVocabularyHeader"):
                root.refreshVocabularyHeader()
            return

        if index >= len(root.kol.objectList):
            index = len(root.kol.objectList) - 1

        root.reviewIndex = index
        root.GoToPageX(index + 1)
        if hasattr(root, "refreshVocabularyHeader"):
            root.refreshVocabularyHeader()

    def Edit(self):
        root = self.root
        #cur_index = root.tabs.currentIndex()
        root.tabs.setCurrentIndex(2)
        reviewIndex = root.reviewIndex
        koBody = root.kol.objectList[reviewIndex].body

        root.addoredit.lineEditcontext.setPlainText(koBody["context"]) # 两种文本编辑器的设置是不一样的
        root.addoredit.lineEditHL.setText(";".join(koBody["HL"]))
        root.addoredit.lineEditk.setText(str(koBody["k"]))
        tags = koBody["tags"]
        if isinstance(tags, dict):
            tags = tags.keys()
        root.addoredit.lineEdittags.setText(";".join(tags))
        root.addoredit.lineEditaudioPath.setText(koBody["audioPath"])
        root.addoredit.lineEditvideoPath.setText(koBody["videoPath"])
        root.addoredit.lineEditimagePath.setText(koBody["imagePath"])
        root.addoredit.lineEditcontextExplanation.setPlainText(koBody["contextExplanation"])
        root.addoredit.lineEditmoreInfo.setPlainText(";".join(koBody["moreInfo"]))

class Row4():
    #------------------ 第四行
    def __init__(self, root):
        self.root = root
        self.rightAnswer = -1; # 正确答案的序号
        self.btFirst =  QPushButton('X')
        self.btSecond = QPushButton('XX')
        self.btThird =  QPushButton('XXX')
        self.btFirst.setFont(QtGui.QFont("Courier New", 15))
        self.btSecond.setFont(QtGui.QFont("Courier New", 15))
        self.btThird.setFont(QtGui.QFont("Courier New", 15))

        self.btFirst.clicked.connect(self.pushActionFirst)
        self.btSecond.clicked.connect(self.pushActionSecond)
        self.btThird.clicked.connect(self.pushActionThird)

        self.hbox4 = QVBoxLayout()
        # self.hbox4.addStretch(1)
        self.hbox4.addWidget(self.btFirst)
        # self.hbox4.addStretch(1)
        self.hbox4.addWidget(self.btSecond)
        # self.hbox4.addStretch(1)
        self.hbox4.addWidget(self.btThird)
        # self.hbox4.addStretch(1)

    def pushActionFirst(self):
        # print("Right answer is " + str(self.rightAnswer))
        self.btFirst.setStyleSheet('')
        self.btSecond.setStyleSheet('')
        self.btThird.setStyleSheet('')
        index =self.root.reviewIndex
        text = self.root.kol.objectList[index].body["contextExplanation"]
        self.root.defaultPanel.row5.lableExplanation.setText(text)
        mode = self.root.kol.mode
        # self.root.kol.objectList[index].body["RT"][mode] += 1 
        if 0 == self.rightAnswer:
            self.btFirst.setStyleSheet('QPushButton{background-color:rgb(0, 255, 0)}')
            self.root.kol.objectList[index].body["CT"][mode] += 1
        else:
            self.btFirst.setStyleSheet('QPushButton{background-color:rgb(255, 0, 0)}')
            self.root.kol.objectList[index].body["RT"][mode] += 1 # 暂时改为错误时才让RT加一，这样PS的变化更快
        # 避免重复按    
        self.btFirst.setEnabled(False)
        self.btSecond.setEnabled(False)
        self.btThird.setEnabled(False)
        
    def pushActionSecond(self):
        # print("Right answer is " + str(self.rightAnswer))
        self.btFirst.setStyleSheet('')
        self.btSecond.setStyleSheet('')
        self.btThird.setStyleSheet('')
        index =self.root.reviewIndex
        text = self.root.kol.objectList[index].body["contextExplanation"]
        self.root.defaultPanel.row5.lableExplanation.setText(text)
        mode = self.root.kol.mode
        # self.root.kol.objectList[index].body["RT"][mode] += 1
        if 1 == self.rightAnswer:
            self.btSecond.setStyleSheet('QPushButton{background-color:rgb(0, 255, 0)}')
            self.root.kol.objectList[index].body["CT"][mode] += 1
        else:
            self.btSecond.setStyleSheet('QPushButton{background-color:rgb(255, 0, 0)}')
            self.root.kol.objectList[index].body["RT"][mode] += 1 # 暂时改为错误时才让RT加一，这样PS的变化更快
        # 避免重复按    
        self.btFirst.setEnabled(False)
        self.btSecond.setEnabled(False)
        self.btThird.setEnabled(False)

    def pushActionThird(self):
        # print("Right answer is " + str(self.rightAnswer))
        self.btFirst.setStyleSheet('')
        self.btSecond.setStyleSheet('')
        self.btThird.setStyleSheet('')
        # 显示解释       
        index =self.root.reviewIndex
        text = self.root.kol.objectList[index].body["contextExplanation"]
        self.root.defaultPanel.row5.lableExplanation.setText(text)
        mode = self.root.kol.mode
        # self.root.kol.objectList[index].body["RT"][mode] += 1
        if 2 == self.rightAnswer:
            self.btThird.setStyleSheet('QPushButton{background-color:rgb(0, 255, 0)}')
            self.root.kol.objectList[index].body["CT"][mode] += 1
        else:
            self.btThird.setStyleSheet('QPushButton{background-color:rgb(255, 0, 0)}')
            self.root.kol.objectList[index].body["RT"][mode] += 1 # 暂时改为错误时才让RT加一，这样PS的变化更快
        # 避免重复按    
        self.btFirst.setEnabled(False)
        self.btSecond.setEnabled(False)
        self.btThird.setEnabled(False)
        
class Row5():
    #------------------ 第五行
    def __init__(self, root):
        self.root = root
        self.lableExplanation = QTextEdit()
        self.lableExplanation.adjustSize()
        self.lableExplanation.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        # lb2 = QLabel(self)
        # lb2.setGeometry(0,250,300,200)
        # lb2.setPixmap(pix)
        # lb2.setStyleSheet("border: 2px solid red")
        # lb2.setScaledContents(True)
        self.hbox5 = QHBoxLayout()
        self.hbox5.addWidget(self.lableExplanation)

class Row6():
    #------------------ 第六行
    def __init__(self, root):
        self.root = root
        self.btRewnew = QPushButton('重排')
        self.btShuffle = QPushButton('随机')
        self.btNext = QPushButton('下一题')
        self.btPrior = QPushButton('上一题')
        self.progressLable = QLabel("0/0")
        self.btRewnew.clicked.connect(self.reSort)
        self.btShuffle.clicked.connect(self.Shuffle)
        self.btNext.clicked.connect(self.nextKo)
        self.btPrior.clicked.connect(self.PriorKo) 

        self.hbox6 = QHBoxLayout()
        # hbox.addStretch(1) # 空白填充，拉伸因子， 参数是QSpacerItem ，其实就是多个Stretch的时候的比例
        self.hbox6.addWidget(self.btRewnew)
        self.hbox6.addWidget(self.btShuffle)
        self.hbox6.addStretch(1)
        self.hbox6.addWidget(self.btPrior)
        self.hbox6.addWidget(self.progressLable)
        self.hbox6.addWidget(self.btNext)

    def reSort(self):
        if not self.root.kol.objectList:
            return
        self.root.kol.sortList();
        self.root.GoToPageX(1)
        pass

    def nextKo(self):
        # 刷新界面
        if self.root.reviewIndex + 1< len(self.root.kol.objectList):
            self.root.GoToPageX(self.root.reviewIndex + 2)
    
    def PriorKo(self):
        # 刷新界面
        if self.root.reviewIndex - 1 >= 0:
            self.root.GoToPageX(self.root.reviewIndex)

    def Shuffle(self):
        random.shuffle(self.root.kol.objectList)
        self.root.GoToPageX(1)


#------------------默认界面
class DefaultPanel():
    def __init__(self, root):
        self.root = root
        #------------------ 第二行  选择，听写，朗读
        self.row2 = Row2(root = self.root);
        #------------------ 第三行  context，CT，RT，删除，修改
        self.row3 = Row3(root = self.root);
        #------------------ 第四行  选项1，选项2，选项3
        self.row4 = Row4(root = self.root);
        #------------------ 第五行  释义
        self.row5 = Row5(root = self.root);
        #------------------ 第六行  重排，上下题目
        self.row6 = Row6(root = self.root);
        
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.row2.hbox2)
        self.vbox.addLayout(self.row3.hbox3)
        self.vbox.addLayout(self.row4.hbox4)
        self.vbox.addLayout(self.row5.hbox5)
        # self.vbox.addStretch(1)
        self.vbox.addLayout(self.row6.hbox6)

#----------------新增/编辑
class AddOrEdit():
    def __init__(self, root):
        self.root = root
        # context,HL,k,tags,audioPath,videoPath,imagePath,contextExplanation,moreInfo
        self.grid = QGridLayout()
        self.lablecontext = QLabel("context")
        self.lineEditcontext = QPlainTextEdit("")
        #self.lineEditcontext.setPlainText("")
        self.grid.addWidget(self.lablecontext, 0, 0)
        self.grid.addWidget(self.lineEditcontext, 0, 1)
        self.lableHL = QLabel("HL")
        self.lineEditHL = QLineEdit("")
        self.grid.addWidget(self.lableHL, 1, 0)
        self.grid.addWidget(self.lineEditHL, 1, 1)
        self.lablek = QLabel("k")
        self.lineEditk = QLineEdit("")
        self.grid.addWidget(self.lablek, 2, 0)
        self.grid.addWidget(self.lineEditk, 2, 1)
        self.labletags = QLabel("tags")
        self.lineEdittags = QLineEdit("")
        self.grid.addWidget(self.labletags, 3, 0)
        self.grid.addWidget(self.lineEdittags, 3, 1)
        self.lableaudioPath = QLabel("audioPath")
        self.lineEditaudioPath = QLineEdit("")
        self.grid.addWidget(self.lableaudioPath, 4, 0)
        self.grid.addWidget(self.lineEditaudioPath, 4, 1)
        self.lablevideoPath = QLabel("videoPath")
        self.lineEditvideoPath = QLineEdit("")
        self.grid.addWidget(self.lablevideoPath, 5, 0)
        self.grid.addWidget(self.lineEditvideoPath, 5, 1)
        self.lableimagePath = QLabel("imagePath")
        self.lineEditimagePath = QLineEdit("")
        self.grid.addWidget(self.lableimagePath, 6, 0)
        self.grid.addWidget(self.lineEditimagePath, 6, 1)
        self.lablecontextExplanation = QLabel("contextExplanation")
        self.lineEditcontextExplanation = QPlainTextEdit("")
        self.grid.addWidget(self.lablecontextExplanation, 7, 0)
        self.grid.addWidget(self.lineEditcontextExplanation, 7, 1)
        self.lablemoreInfo = QLabel("moreInfo")
        self.lineEditmoreInfo = QPlainTextEdit("")
        self.grid.addWidget(self.lablemoreInfo, 8, 0)
        self.grid.addWidget(self.lineEditmoreInfo, 8, 1)
        self.lableKoNumber = QLabel("Total KO numbers")
        self.lableKoNumber2 = QLabel("")
        self.grid.addWidget(self.lableKoNumber, 9, 0)
        self.grid.addWidget(self.lableKoNumber2, 9, 1)
        
        self.btSave = QPushButton("保存新增")
        self.grid.addWidget(self.btSave, 10, 0)
        self.btSave.clicked.connect(self.SaveAdded)
        self.btSave = QPushButton("保存修改")
        self.grid.addWidget(self.btSave, 10, 1)
        self.btSave.clicked.connect(self.saveChanges)

    def saveChanges(self):
        root = self.root
        #cur_index = root.tabs.currentIndex()
        # root.tabs.setCurrentIndex(2)
        reviewIndex = root.reviewIndex
        koBody = root.kol.objectList[reviewIndex].body
        koBody["context"] = root.addoredit.lineEditcontext.toPlainText()
        koBody["HL"] = root.addoredit.lineEditHL.text().split(";")
        print(str(koBody["HL"]))
        kStr = root.addoredit.lineEditk.text()
        if len(kStr) != 0:
            koBody["k"] = int(kStr)
        else:
            koBody["k"] = 1
        print("k " + str(koBody["k"]))
        koBody["tags"] = root.addoredit.lineEdittags.text().split(";")
        print(str(koBody["tags"]))
        
        koBody["audioPath"] = root.addoredit.lineEditaudioPath.text()
        koBody["videoPath"] = root.addoredit.lineEditvideoPath.text()
        koBody["imagePath"] = root.addoredit.lineEditimagePath.text()
        
        koBody["contextExplanation"] = root.addoredit.lineEditcontextExplanation.toPlainText()
        koBody["moreInfo"] = root.addoredit.lineEditmoreInfo.toPlainText().split(";")
        print(str(koBody["moreInfo"]))
        print("Changed !")
        self.lableKoNumber2.setText(str(len(root.kol.objectList)))
        root.refreshVocabularyHeader()

    def SaveAdded(self):
        root = self.root
        # root.tabs.setCurrentIndex(2)
        # reviewIndex = len(root.kol.objectList)
        ko = knowledgeObject() 
        koBody = ko.body
        root.kol.objectList.append(ko)
        koBody["context"] = root.addoredit.lineEditcontext.toPlainText()
        koBody["HL"] = root.addoredit.lineEditHL.text().split(";")
        print(str(koBody["HL"]))
        kStr = root.addoredit.lineEditk.text()
        if len(kStr) != 0:
            koBody["k"] = int(kStr)
        else:
            koBody["k"] = 1
        print("k " + str(koBody["k"]))
        koBody["tags"] = root.addoredit.lineEdittags.text().split(";")
        print(str(koBody["tags"]))
        
        koBody["audioPath"] = root.addoredit.lineEditaudioPath.text()
        koBody["videoPath"] = root.addoredit.lineEditvideoPath.text()
        koBody["imagePath"] = root.addoredit.lineEditimagePath.text()
        
        koBody["contextExplanation"] = root.addoredit.lineEditcontextExplanation.toPlainText()
        koBody["moreInfo"] = root.addoredit.lineEditmoreInfo.toPlainText().split(";")
        print(str(koBody["moreInfo"]))
        print("Added !")

        self.lineEditcontext.setPlainText("")
        self.lineEditHL.setText("")
        self.lineEditk.setText("")
        self.lineEdittags.setText("")
        self.lineEditaudioPath.setText("")
        self.lineEditvideoPath.setText("")
        self.lineEditimagePath.setText("")
        self.lineEditcontextExplanation.setPlainText("")
        self.lineEditmoreInfo.setPlainText("")

        self.lableKoNumber2.setText(str(len(root.kol.objectList)))
        if len(root.kol.objectList) == 1:
            root.GoToPageX(1)
        root.refreshVocabularyHeader()
        
class Example(QWidget):
    def __init__(self):
        super().__init__()
        projectDirectory = os.path.dirname(os.path.abspath(__file__))
        self.currentVocabularyPath = os.path.join(projectDirectory, "data", "ko.json")
        self.currentVocabularyMetadata = {}
        self.kol = knowledgeObjectList()
        koList, self.currentVocabularyMetadata = load_vocabulary(self.currentVocabularyPath)
        self.kol.objectList = []
        for ite in koList:
            self.kol.objectList.append(knowledgeObject(body = ite))
        self.Init_UI()
        # self.kol.PrintList()
        
        # 准备数据
        self.reviewIndex = 0;
        self.correctNumber = -1;
        if self.kol.objectList:
            self.kol.sortList();
            self.GoToPageX(1)
        else:
            self.refreshDefaultTab()
        self.refreshVocabularyHeader()

        # 注册快捷键
        QShortcut(QtGui.QKeySequence(self.tr("Ctrl+D")), self, self.NextPage)
        QShortcut(QtGui.QKeySequence(self.tr("Ctrl+A")), self, self.PriorPage)

    def NextPage(self):
        if self.reviewIndex + 1< len(self.kol.objectList):
            self.GoToPageX(self.reviewIndex + 2)
    
    def PriorPage(self):
        if self.reviewIndex - 1 >= 0:
            self.GoToPageX(self.reviewIndex)
    
    # 根据当前的 self.reviewIndex 自动显示在界面上
    def refreshDefaultTab(self):
        if not self.kol.objectList:
            self.reviewIndex = 0
            self.correctNumber = -1
            self.defaultPanel.row3.lableContext.setPlainText(
                "当前单词本为空。请在“新增/编辑”页面添加单词。"
            )
            self.defaultPanel.row3.lableCorect.setText("CT:0")
            self.defaultPanel.row3.lableReview.setText("RT:0")
            self.defaultPanel.row5.lableExplanation.setText("")
            self.defaultPanel.row6.progressLable.setText("0/0")
            self.defaultPanel.row6.btPrior.setEnabled(False)
            self.defaultPanel.row6.btNext.setEnabled(False)
            self.defaultPanel.row3.btDelete.setEnabled(False)
            self.defaultPanel.row3.btChange.setEnabled(False)
            for button in self.answerButtons():
                button.setText("—")
                button.setEnabled(False)
                button.setStyleSheet("")
            return

        self.defaultPanel.row3.btDelete.setEnabled(True)
        self.defaultPanel.row3.btChange.setEnabled(True)
        if self.reviewIndex >= len(self.kol.objectList):
            self.reviewIndex = len(self.kol.objectList) - 1
        context = self.kol.objectList[self.reviewIndex].body["context"]
        review  = self.kol.objectList[self.reviewIndex].body["RT"]
        correct = self.kol.objectList[self.reviewIndex].body["CT"]
        mode    = self.kol.mode
        reviewHl = self.kol.objectList[self.reviewIndex].body["HL"]
        contextWithBlank = context
        for ite in reviewHl:
            contextWithBlank = contextWithBlank.replace(ite, '___')
        self.defaultPanel.row3.lableContext.setPlainText(contextWithBlank)
        self.defaultPanel.row3.lableCorect.setText('CT:' + str(correct[mode]))
        self.defaultPanel.row3.lableReview.setText('RT:' + str(review [mode]))

        listLen = len(self.kol.objectList)
        otherIndexes = [index for index in range(listLen) if index != self.reviewIndex]
        answerList = [self.reviewIndex]
        answerList.extend(random.sample(otherIndexes, min(2, len(otherIndexes))))
        random.shuffle(answerList)
        print("listLen " + str(listLen))
        print("answerList" + str(answerList))
        print("self.reviewIndex " + str(self.reviewIndex))
        # self.kol.PrintList()
        # 记录哪一个按钮是正确答案
        for i in range(len(answerList)):
            if self.reviewIndex == answerList[i] :
                self.correctNumber = i;
                self.defaultPanel.row4.rightAnswer = i;
                break;
        # "".join(a)  >>> '12'
        # " ".join(a) >>> '1 2'
        # ",".join(a) >>> '1,2'
        for position, button in enumerate(self.answerButtons()):
            button.setStyleSheet("")
            if position < len(answerList):
                answer = self.kol.objectList[answerList[position]].body["HL"]
                button.setText(",".join(answer))
                button.setEnabled(True)
            else:
                button.setText("—")
                button.setEnabled(False)

        self.defaultPanel.row5.lableExplanation.setText("")
        self.defaultPanel.row6.progressLable.setText(str(self.reviewIndex + 1) + '/' + str(listLen))
        self.defaultPanel.row6.btPrior.setEnabled(self.reviewIndex > 0)
        self.defaultPanel.row6.btNext.setEnabled(self.reviewIndex < listLen - 1)

    def GoToPageX(self, pageNumber):
        if not self.kol.objectList:
            self.refreshDefaultTab()
            return
        self.reviewIndex = pageNumber - 1;
        self.correctNumber = -1;
        self.refreshDefaultTab()

    def answerButtons(self):
        return [
            self.defaultPanel.row4.btFirst,
            self.defaultPanel.row4.btSecond,
            self.defaultPanel.row4.btThird,
        ]
        
    def Init_UI(self):
        self.setGeometry(300,300,1000,700) # 初始窗口大小
        self.setWindowTitle('EnglishReviewer')

        self.defaultPanel = DefaultPanel(root = self);
        self.addoredit = AddOrEdit(root = self)
        self.btNewVocabulary = QPushButton("新增单词本")
        self.btSelectVocabulary = QPushButton("选择单词表")
        self.btNewVocabulary.clicked.connect(self.NewVocabulary)
        self.btSelectVocabulary.clicked.connect(self.SelectVocabulary)
        self.vocabularyLabel = QLabel("")
        self.vocabularyLabel.setToolTip("当前单词表及其元数据")
        self.vocabularyLayout = QHBoxLayout()
        self.vocabularyLayout.addWidget(self.btNewVocabulary)
        self.vocabularyLayout.addWidget(self.btSelectVocabulary)
        self.vocabularyLayout.addWidget(self.vocabularyLabel)
        self.vocabularyLayout.addStretch(1)
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs.resize(300,200)
        # self.tab3.clicked.connect(self.add)
        # 三个按钮信号都绑定一个槽函数show_panel
        # self.sender().objectName()
        # 获取当前点击按钮的名称，结合字典获得索引
        # self.qsl.setCurrentIndex(index)
        # 通过索引设置堆叠布局展示的页面

        # Add tabs
        self.tabs.addTab(self.tab1,"默认模式")
        self.tabs.addTab(self.tab2,"Tag筛选")
        self.tabs.addTab(self.tab3,"新增/编辑")
        self.tabs.addTab(self.tab4,"搜索")
        
        # Create first tab
        self.tab1.setLayout(self.defaultPanel.vbox)
        self.tab3.setLayout(self.addoredit.grid)
        # # 自动切换不同的页面/tabs的方法
        # cur_index = self.tabs.currentIndex()
        # print("cur_index "+ str(cur_index))
        # self.tabs.setCurrentIndex(2)
        
        # Add tabs to widget
        self.layout = QVBoxLayout(self)
        self.layout.addLayout(self.vocabularyLayout)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout) # 将布局填充到窗体中
        self.show()

    def refreshVocabularyHeader(self):
        title = self.currentVocabularyMetadata.get("title")
        if not title:
            title = os.path.splitext(os.path.basename(self.currentVocabularyPath))[0]
        fileName = os.path.basename(self.currentVocabularyPath)
        self.vocabularyLabel.setText(
            "当前单词本：{}（{}，{} 个词条）".format(
                title,
                fileName,
                len(self.kol.objectList),
            )
        )
        description = self.currentVocabularyMetadata.get("description", "")
        source = self.currentVocabularyMetadata.get("sourceLanguage", "")
        target = self.currentVocabularyMetadata.get("targetLanguage", "")
        tags = self.currentVocabularyMetadata.get("tags", [])
        if isinstance(tags, list):
            tags = "、".join(tags)
        self.vocabularyLabel.setToolTip(
            "路径：{}\n描述：{}\n语言：{} → {}\n标签：{}".format(
                self.currentVocabularyPath,
                description,
                source,
                target,
                tags,
            )
        )
        self.setWindowTitle("EnglishReviewer - " + title)
        self.addoredit.lableKoNumber2.setText(str(len(self.kol.objectList)))

    def SaveCurrentVocabulary(self, showMessage=True):
        try:
            SaveFile(self.currentVocabularyPath, self.kol.objectList)
        except Exception as error:
            QMessageBox.critical(self, "保存失败", str(error))
            return False
        if showMessage:
            QMessageBox.information(
                self,
                "保存成功",
                "已保存到：\n" + self.currentVocabularyPath,
            )
        return True

    def confirmVocabularySwitch(self):
        result = QMessageBox.question(
            self,
            "切换单词本",
            "切换后，当前未保存的修改会丢失。是否先保存当前单词本？",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            QMessageBox.Save,
        )
        if result == QMessageBox.Cancel:
            return False
        if result == QMessageBox.Save:
            return self.SaveCurrentVocabulary(showMessage=False)
        return True

    def NewVocabulary(self):
        dialog = NewVocabularyDialog(self)
        if dialog.exec_() != QDialog.Accepted:
            return
        if not self.confirmVocabularySwitch():
            return
        path, metadata = dialog.values()
        try:
            createdPath, createdMetadata = create_vocabulary(path, metadata)
        except Exception as error:
            QMessageBox.critical(self, "创建失败", str(error))
            return
        self.loadVocabulary(createdPath, createdMetadata)
        self.tabs.setCurrentIndex(2)
        QMessageBox.information(
            self,
            "创建成功",
            "新单词本已创建。请在“新增/编辑”页面添加第一个词条。",
        )

    def SelectVocabulary(self):
        initialDirectory = os.path.dirname(self.currentVocabularyPath)
        path, _ = QFileDialog.getOpenFileName(
            self,
            "选择单词表",
            initialDirectory,
            "JSON 文件 (*.json)",
        )
        if not path:
            return
        if path.endswith(".meta.json"):
            QMessageBox.warning(self, "无法打开", "请选择单词表 JSON，而不是元数据文件。")
            return
        try:
            objects, metadata = load_vocabulary(path)
        except Exception as error:
            QMessageBox.critical(self, "打开失败", str(error))
            return
        if not self.confirmVocabularySwitch():
            return
        self.loadVocabulary(path, metadata, objects)

    def loadVocabulary(self, path, metadata=None, objects=None):
        if objects is None:
            objects, loadedMetadata = load_vocabulary(path)
            if metadata is None:
                metadata = loadedMetadata
        self.currentVocabularyPath = os.path.abspath(path)
        self.currentVocabularyMetadata = metadata or {}
        self.kol.objectList = [knowledgeObject(body=body) for body in objects]
        self.reviewIndex = 0
        self.correctNumber = -1
        if self.kol.objectList:
            self.kol.sortList()
        self.refreshDefaultTab()
        self.refreshVocabularyHeader()

    def closeEvent(self, event):
        # 弹窗
        result = QMessageBox.information(self,'提示','是否保存？', QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)
        if QMessageBox.Ok == result:
            self.SaveCurrentVocabulary(showMessage=False)
        # SaveFile('./data/ko.json', self.kol.objectList)
    def add(self):
        print("clicked tab3")
    def show_panel(self):
        print("show_panel ")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    app.exit(app.exec_())
