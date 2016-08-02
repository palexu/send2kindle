#coding=utf-8
from  urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
import os
import traceback

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
    print("getAllChapterLinks>>>>>>>>>>:"+pageUrl)
    html = session.get(pageUrl,headers=headers)
    bsObj = BeautifulSoup(html.text,"html.parser")

    novelList=bsObj.findAll("li")

    linksList=[]
    regx=pageUrl.replace("http://www.shumilou.co","")
    pattern=re.compile(regx)
    for novel in novelList:
        try:
            link=novel.a['href']
            name=novel.get_text()
            match=pattern.search(link)
            if match:
                # print(link)
                l=["http://www.shumilou.co"+link,name]
                linksList.append(l)
        except Exception as e:
            print("getAllChapterLinks:error  "+str(e))
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

def washNovelList(lists,nextChapter=0):
    "返回所有未读章节，与最新章节数；默认当前阅读到第一章，即返回所有章节"
    l=[]
    mx=0
    print(">>>>>>><<<<<<<<<<<"+str(nextChapter))
    for item in lists:
        if "第" in item[1] and "章" in item[1]:
            try:
                chapter=item[1].split()[0]
                if "两" in chapter:
                    chapter=chapter.replace("两","二")
                # print("wash "+chapter)
                chapter=chapter.replace("第","")
                chapter=chapter.replace("章","")

                #若全数字
                if chapter.isdigit()==True:
                    num=int(chapter)
                #若其他
                else:
                    num=cn2.c2n(chapter)
                if num>mx:
                    mx=num
                    if num>=nextChapter:
                        l.append(item)
            except Exception as e:
                traceback.print_exc()
    start=nextChapter
    end=mx
    return l,end,start

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

    #尝试对标题进行处理
    cleanlist=washNovelList(lists,nextChapter)
    l=cleanlist[0]
    mx=cleanlist[1]

    print("当前已读到%s" % str(nextChapter-1))
    print("最新章节为%s" % mx)

    if nextChapter>mx:
        print("无未读章节")
        return ""
    else:
        for i in l:
            print(i[1])

        # 构造待发送的文件名：该处理很不健壮！！
        start=cleanlist[2]
        end=mx

        if start==end:
            suf=start
        else:
            suf=str(start)+"-"+str(end)
        print(suf)

        filename=filename+"#"+suf+".txt"
        chapterSpider(l,filename,limit=False)
        sql.setAtChapter(novelname_chi,mx)
        return filename


def getAllChapters(novelUrl):
    links=getAllChapterLinks(novelUrl)
    #从第一章开始加载
    cleanlist=washNovelList(links)
    l=cleanlist[0]
    mx=cleanlist[1]
    novelname_chi=getNovelName_chi(novelUrl)
    filename=getNovelName_en(novelUrl)
    print("2 file>>>>>>>>>")
    chapterSpider(l,filename+".txt",limit=False)
    sql.setAtChapter(novelname_chi,mx)
    return filename+".txt"
    

def chapterSpider(links,filename,limit=True):
    "若不解除限制，则只发送前30章 为测试方便,定为3章"
    if limit==True:
        # times=30
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
            print(link[1])
            content=getOneChapter(url)
            save2file(filename,content)
            # time.sleep(500)
        except Exception as e:
            print(e)


def test():
    print("test:getAllChapterLinks")
    getAllChapters("http://www.shumilou.co/heianxueshidai")

    # print("test:getNovelName_chi")
    # print(getNovelName_chi("http://www.shumilou.co/xiuzhensiwannian"))

    # print("""test:getNewChapters
    #     设置当前阅读到:1294
    #     """)
    # sql.setAtChapter("修真四万年",1294)
    # sql.show()
    # filename=getNewChapters("http://www.shumilou.co/xiuzhensiwannian")
    # sql.show()
    # kindle.send2kindle(filename)


def is_chi(self,text):
    "判断是否为中文"
    return all('\u4e00' <= char <= '\u9fff' for char in text)

#+++++++++++++++++++++++++++++++++++++++++
def NewCapters2kindle(pageUrl):
    filename=getNewChapters(pageUrl)
    if filename!="":
        kindle.send2kindle(filename)

def AllCapters2kindle(pageUrl):
    filename=getAllChapters(pageUrl)
    kindle.send2kindle(filename)

if __name__ == '__main__':
    test()


            
    
        




