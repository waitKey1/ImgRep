#coding=utf-8
import re
import time
import requests
from urllib import parse #对汉字进行编码
import os
#用来随机抽头发出申请

from fake_useragent import UserAgent #随机生成一个user-agent,模拟有多个浏览器访问
#import urllib3

class ImgGenerate:
    def __init__(self,engine,search,maxNum,outFile):

        self.dicPattern={'bing':r'<img class="mimg vi.*src="(.*?)"','baidu':r'"middleURL":"(.*?)"'} #下载小图匹配的正则表达式
        self.dicPatternEr = {'bing': r'murl&quot;:&quot;(.*?)&', 'baidu': r'"thumbURL":"(.*?)"'}   #下载原图匹配的正则表达式
        self.dicUrl={'bing':'https://cn.bing.com/images/search?q={}&form=HDRSC2&first={}&tsc=ImageHoverTitle','baidu':'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=7542812996841482750&ipn=rj&ct=201326592&is=&fp=result&fr=&word={}&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn={}&rn=30&gsm=1e&{}='}
        self.engine = engine  #检索引擎
        self.search =search   #检索词
        self.Dowdnum=0        #当前已经下载数量
        self.imgNum =maxNum   #下载数量
        self.outFile=outFile  #下载图片的地址

        try:
            # 确保当前目录位于search目录，图片将保存在这一目录
            os.chdir(self.outFile)

            if not os.path.isdir("./{}_{}".format(search,engine)):  # 确定文件夹一定存在
                os.mkdir("./{}_{}".format(search,engine))
            os.chdir("./{}_{}".format(search,engine))
        except:
            print("请输入正常的检索词")


    '''
    函数功能
        输入一个地址和，网页源码，
        将源码写入txt文本，便于浏览
    '''
    def writeHtml(self,outfile,html):
        with open(outfile,'w',encoding='utf-8') as f:
            f.write(str(html))

    '''
    函数功能
        返回一个url页面里面全部图片超链接的列表
    '''
    def geturls(self,baseurl,enginPattern):
        ImgUrlPattern = re.compile(enginPattern)  # 正则表达式匹配图片,匹配bing搜索

        # 响应头，假装我是浏览器访问的网页
        headers ={'User-Agent':UserAgent().random}
        #urllib3.disable_warnings()                         #忽略警告
        response = requests.get(baseurl, headers=headers)  # 获取网页信息

        html = response.text                  # 将网页信息转化为text形式
        #print(html)
        data=re.findall(ImgUrlPattern, html)  # 得到图片超链接的列表
        print(data)
        #print()
        return data                           # 返回一个包含该页面全部图片超链接的新列表

    '''
    根据路径打开文件
    '''
    def Openfile(self,file):
        try:
            os.startfile(file)
        except:
            print('Not Find the file')
    '''
    函数功能：
        遍历输入的图像urls
        并将其下载下来
    '''

    def DownloadImg(self,imgUrls):

        # 头，假装我是浏览器访问的网页
        headers={'User-Agent':UserAgent().random}

        for ImgUrl in imgUrls:
            if self.Dowdnum < self.imgNum:  #判断次数是否够了
                # 如果url是无效的，则查看下一个url
                try:
                    resp = requests.get(ImgUrl, headers=headers)    # 获取网页信息
                except requests.ConnectionError as e:
                    continue
                byte = resp.content                                 # 转化为content二进制
                with open("{:0>5d}.jpg".format(self.Dowdnum + 1), "wb") as f:  # 文件写入
                    if resp.status_code==200 and len(str(byte)) > 1000 :  # 访问成功200且返回页面字节长度大于1000
                        f.write(byte)
                        # print(len(str(byte)))
                        self.Dowdnum = self.Dowdnum + 1        # 递增，表示又多下载了一张图片
                        time.sleep(0.5)  # 每隔0.5秒下载一张图片，避免由于访问过快被反爬了，认为我在DDS攻击服务器
                        print("第{}张与{}有关的图片爬取成功!".format(self.Dowdnum, self.search))
            else:
                break


    def run(self):
        #print(self.Dowdnum,self.imgNum)
        index=0 #页数
        while(self.Dowdnum<self.imgNum):
            if self.engine=='baidu':
                decteUrl=self.dicUrl[self.engine].format(parse.quote(self.search),parse.quote(self.search),index*30,str(int(time.time()*1000)))
            elif self.engine=='bing':
                decteUrl=self.dicUrl[self.engine].format(self.search,index*35) #dicUrl保存着 引擎与搜索地址的映射
            imgUrls=self.geturls(decteUrl,self.dicPatternEr[self.engine])        #获取网页中所有图片地址
            #print(imgUrls)
            self.DownloadImg(imgUrls)  #输入地址，开始下载
            index+=1

        if(self.Dowdnum==self.imgNum):
            print("已基于搜索引擎{}爬取了{}张与{}相关的图片，保存在文件夹{}".format(self.engine,self.imgNum,self.search,os.getcwd()))




    def setOutFile(self,outFile):
        self.outFile=outFile

def Down_One_Img(url):
    header={'User-Agent':UserAgent().random}

    html=requests.get(url,headers=header).content
    print(os.getcwd())
    with open('../Images/10001.jpg','wb')as w:
        w.write(html)

def main():
    print('有效的引擎有：bing,baidu')
    engine = input('请输入引擎：')  # 要爬取的引擎，有效值有：bing,baidu
    search = input('请输入检索词：')  # 检索词
    imgNum = int(input('请输入爬取图片数量：'))  # 爬取图片数量

    outFile=os.getcwd()


    ImgG = ImgGenerate(engine,search,imgNum,outFile)
    ImgG.run()


if __name__ == '__main__':
   # ImgGen=ImgGenerate('bing','im1',23,'images')
    #url='https://img0.baidu.com/it/u=3965453168,289903526&fm=253&fmt=auto&app=138&f=JPEG?w=667&h=500'
    #Down_One_Img(url)
    main()
