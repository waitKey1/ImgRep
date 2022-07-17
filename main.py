import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
from _functools import partial


import ui.Start as A
import ui.ImgGenerate as B
import tools.ImgGen as ImgGen


def ImgGenerate(ui):  #点击运行之后，根据输入运行爬虫
    engine=ui.getcombobox()
    print(engine)
    search=ui.lineEdit.text()
    number=int(ui.lineEdit_2.text())
    outFile=ui.lineEdit_3.text()
    print(search,number,outFile)
    ImgGene=ImgGen.ImgGenerate(engine,search,number,outFile)
    ImgGene.run()


def openBegin(MainWindow): #打开运行页面
    MainWindow.close()
    ui=B.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.pushButton.clicked.connect(partial(ImgGenerate,ui))



if __name__=='__main__':     #打开开始页面
    app=QApplication(sys.argv)
    MainWindow=QMainWindow()
    ui=A.Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.pushButton.clicked.connect(partial(openBegin,MainWindow))#如果触发Button事件，关闭当前页面打开，运行页面
    sys.exit((app.exec_()))
