#coding=utf-8
from  urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
import os

import cnconvert as cn2
import sql 
import send2kindle as kindle

#还需要对其他组件提供api，所以需要良好设计

pages=set()
session=requests.Session()
headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding":"gzip, deflate",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

def getAllChapterLinks(pageUrl):
    "return linksList=[link,name]"
    html = session.get(pageUrl,headers=headers)
    bsObj = BeautifulSoup(html.text,"html.parser")

    novelList=bsObj.findAll("li")

    linksList=[]
    pattern=re.compile(r'/xiuzhensiwannian')
    for novel in novelList:
        try:
            link=novel.a['href']
            name=novel.get_text()
            match=pattern.search(link)
            if match:
                l=["http://www.shumilou.co"+link,name]
                linksList.append(l)
        except Exception:
            print("getAllChapterLinks:error")
    linksList=linksList[:-1]
    return linksList

def getNovelName_chi(pageUrl):
    html = session.get(pageUrl,headers=headers)
    bsObj = BeautifulSoup(html.text,"html.parser")
    name=bsObj.find("div",{"class":"tit"}).b.get_text()
    return name

def getNovelName_en(pageUrl):
    name=pageUrl.replace("http://www.shumilou.co/","")
    print(name)
    return name

#测试用：打印链接列表
def printl(linksList):
    for i in linksList:
        print("#"*10)
        for j in i:
            print(j)
        print("#"*10)

#获得一篇文章的正文
def getOneChapter(link):
    pattern=re.compile(r'shumilou')

    html = session.get(link,headers=headers)
    bsObj=BeautifulSoup(html.text,"html.parser")

    content=bsObj.findAll("p")
    title=bsObj.find("div",{"class":"title"}).h2.get_text()
    novel=""+title+"\n"

    for p in content:
        match=pattern.search(p.get_text())
        if match:
            pass
        else:
            novel=novel+p.get_text()
    novel=novel+"\n\n"
    return novel

def save2file(filename,content):
    #保存为电子书文件
    filename=filename
    f=open(filename,'a')
    f.write(content)
    f.close()

def getNewChapters(pageUrl,charset="en"):
    lists=getAllChapterLinks(pageUrl)
    novelname_chi=getNovelName_chi(pageUrl)

    if charset=="en":
        print("using en novelname")
        filename=getNovelName_en(pageUrl)
    else:
        filename=novelname_chi

    #获取数据库的记录
    nextChapter=sql.nextChapter(novelname_chi)

    mx=0
    l=[] #未阅读列表
    #尝试对标题进行处理
    for item in lists:
        try:
            chapter=item[1].split()[0]
            chapter=chapter[1:-1]
            #若全数字
            if chapter.isdigit()==True:
                num=int(chapter)
            #若其他
            else:
                num=cn2.c2n(chapter)
            if num>=nextChapter:
                l.append(item)
                if num>mx:
                    mx=num
        except Exception as e:
            print(e)

    for i in l:
        print(i[1])

    # 构造待发送的文件名：该处理很不健壮！！
    #作用： 第1章 测试章节 --> 1
    start=l[0][1].split()[0][1:-1]
    end=l[-1][1].split()[0][1:-1]

    if start==end:
        suf=start
    else:
        suf=start+"-"+end
    print(suf)

    filename=filename+"#"+suf+".txt"
    chapterSpider(l,filename,limit=False)
    sql.setAtChapter(novelname_chi,mx)
    return filename


def getAllChapters(novelUrl):
    links=getAllChapterLinks(novelUrl)
    filename=getNovelName_chi(novelUrl)
    chapterSpider(links,filename)
    

def chapterSpider(links,filename,limit=True):
    "若不解除限制，则只发送3章"
    if limit==True:
        times=3
    else:
        times=1000000
    for link in links:
        #test times limit
        times=times-1
        if times<0:
            break
        #================
        try:
            url=link[0]
            print(url)
            content=getOneChapter(url)
            save2file(filename,content)
            # time.sleep(500)
        except Exception as e:
            print(e)


def test():
    print("test:getAllChapterLinks")
    getAllChapters("http://www.shumilou.co/xiuzhensiwannian")

    print("test:getNovelName_chi")
    print(getNovelName_chi("http://www.shumilou.co/xiuzhensiwannian"))

def is_chi(self,text):
    "判断是否为中文"
    return all('\u4e00' <= char <= '\u9fff' for char in text)

if __name__ == '__main__':
    # test()
    sql.setAtChapter("修真四万年",1294)
    # sql.show()
    filename=getNewChapters("http://www.shumilou.co/xiuzhensiwannian")
    print(filename)
    # sql.show()
    # filename="修真四万年1295-1299.txt"
    kindle.send2kindle(filename)
            
    
        




