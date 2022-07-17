# coding:utf-8

'''
    函数功能：
    将ui文件转换成py文件
'''
import os
def ui2py(uiFile,pyFile):
    os.system('pyuic5 -o {} {}'.format(pyFile,uiFile))
if __name__=='__main__':
    print('输入0退出程序')
    while True:
        uiFile=input('请输入要转化的ui地址：')
        if uiFile =='0':
            break
        else:
            pyFile=str(uiFile.split('.')[0])+'.py'
            ui2py(uiFile,pyFile)
