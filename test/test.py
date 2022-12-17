import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 tabs - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        self.show()
    
class MyTableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Tab 1")
        self.tabs.addTab(self.tab2,"Tab 2")
        
        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("PyQt5 button")
        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.setLayout(self.tab1.layout)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())



# ''' test '''
# body1 = {}
# body1["context"] = "context 1"                # 文本信息
# body1["HL"] = ['1']                     # 文本中的知识点
# body1["PS"] = 1 

# body2 = {}
# body2["context"] = "context 2"                # 文本信息
# body2["HL"] = ['2']                     # 文本中的知识点
# body2["PS"] = 2

# body3 = {}
# body3["context"] = "context 3"                # 文本信息
# body3["HL"] = ['3']                     # 文本中的知识点
# body3["PS"] = 3 

# KO1 = knowledgeObject(body = body1)
# KO2 = knowledgeObject(body = body2)
# KO3 = knowledgeObject(body = body3)

# KOL = knowledgeObjectList()
# KOL.objectList.append(KO1)
# KOL.objectList.append(KO2)
# KOL.objectList.append(KO3)
# print("Original list")
# KOL.PrintList()

# KOL.sortList()
# print("After sorting")
# KOL.PrintList()


# # save in file —— OK
# SaveFile('./data/ko.json', KOL.objectList)


# read from file —— OK
# koList = LoadFile('./data/ko.json')
# KOL = knowledgeObjectList()
# for ite in koList:
#     KOL.objectList.append(knowledgeObject(body = ite))

# print("After loading")
# KOL.PrintList()
