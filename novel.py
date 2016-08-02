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
    """
    考虑到存在部分章节命名存在问题，但是章节都是连续的，所以在某章节存在问题时，可以使用前几章节来推导其章节号
    """
    prev=0

    count_all=0
    count_right=1

    fiveContinue=False

    ERROR_RANGE=10
    ERROR_PROBABILITY=0.85

    pattern_chi=re.compile(r'第[零一二三四五六七八九十百千两]+章')
    pattern_d=re.compile(r'第\d+章')
    lists=lists[::-1]
    for item in lists:
        count_all+=1
        try:
            chapter=item[1]
            
            print("wash "+chapter)

            #若全数字
            cha=pattern_d.search(chapter)
            if cha:
                rs=cha.group()[1:-1]
                if len(str(rs))>=1:
                    num=int(rs)
            #若其他
            else: 
                #中文标题:第一百章
                match_chi=pattern_chi.search(chapter)
                if match_chi:
                    chapter=match_chi.group()
                    pat=re.compile(r'[零一二三四五六七八九十百千两]+')
                    match_chi=pat.findall(chapter)
                    mxlen=0
                    for i in match_chi:
                        if len(i)>=mxlen:
                            chapter=i
                            mxlen=len(i)
                    if "两" in chapter:
                        chapter=chapter.replace("两","二")
                    try:
                        num=cn2.c2n(chapter)
                    #如果无法从中文转为数字，说明章节名混入了奇怪的字符
                    except Exception as e:
                        print(e)
                        string=""
                        for i in match_chi:
                            string+=i
                        num=cn2.c2n(string)
                        print("warning:当前章节[%s]:编号无法解析，已智能设置章节号为:%i" % (item[1],num))
            
            # #如果是连续的章节
            # if num-prev==1:
            #     print("连续的")
            #     count_right+=1
            #     prev+=1
            
            #不连续，但相差不大,并且到目前为止的章节连续性较好，尝试使用当前章节号
            print("num:%d prev:%d"%(num,prev-1))
            if abs(num-prev)>=ERROR_RANGE:
                tmp=prev
                prev=num
                num=tmp+1
                


            # #如果相差太大，如9->15,已经影响到阅读体验，建议更换源网站
            # else:
            #     print("right:"+str(count_right))
            #     print("all:"+str(count_all))
            #     print(count_right/count_all)
            #     if count_right/count_all>=ERROR_PROBABILITY:
            #         num=prev+1
            #         prev=num
            #         print("waring:当前章节[%s]:编号存在较大问题，已智能设置章节号为:%i" % (item[1],num))
            #     else:
            #         print("warning:该源网站章节编号问题较大，建议更换源")
            #         num=prev+1
            #         prev=num

            print("num:%d prev:%d"%(num,prev-1))

            if num>mx:
                mx=num
            if num>=nextChapter:
                l.append(item)

        except Exception as e:
            print(e)
    print(">>"*20)
    print(mx)

    start=nextChapter
    end=mx
    l=l[::-1]
    for i in l:
        print(i)
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
    print("save to file>>>>>>>>>")
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
    print("test: getAllChapterLinks && washNovelList ")
    links=getAllChapterLinks("http://www.shumilou.co/zoujinxiuxian")
    washNovelList(links)

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
    # test()
    sql.show()
    sql.setAtChapter("走进修仙",340)
    getNewChapters("http://www.shumilou.co/zoujinxiuxian")


            
    
        




