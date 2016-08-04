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
    '''
    return linksList=[link,name]
    '''
    print("\n"+"#"*30+"send2kindle"+"#"*30)
    print("正在获取章节列表".encode("utf-8")+">>>"+pageUrl)
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
            # print("getAllChapterLinks:error  "+str(e))
            pass
    linksList=linksList[:-1]
    return linksList

def getNovelName_chi(pageUrl):
    html = session.get(pageUrl,headers=headers)
    bsObj = BeautifulSoup(html.text,"html.parser")
    name=bsObj.find("div",{"class":"tit"}).b.get_text()
    return name

def getNovelName_en(pageUrl):
    '''
    >>> getNovelName_en("http://www.shumilou.co/test")
    'test'
    '''
    name=pageUrl.replace("http://www.shumilou.co/","")
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

def washNovelList(lists):
    "返回所有未读章节，与最新章节数；默认当前阅读到第一章，即返回所有章节"
    l=[]
    mx=0
    mi=1000000
    print(">"*5+"正在处理章节信息"+"<"*5)
    #考虑到存在部分章节命名存在问题，但是章节都是连续的，所以在某章节存在问题时，可以使用前几章节来推导其章节号
    prev=0

    #某些章节出现从1到200又从1开始，如 1 2 3 4 …… 368 1 2 3 ……256 ，因为分了卷名之类，所以检测是否章节名循环
    #如果进入新的循环，那么重置计数器mx=0 mi=1000000 newcircle=False 
    newcircle=False
    numOfChapterOne=0

    ERROR_RANGE=10
    ERROR_PROBABILITY=0.85

    print("待处理章节数%d" % len(lists))
    if len(lists)==1:
        num=getNumOfTitle(lists[0][1])
        mx=num
        mi=num
    else:
        for item in lists:
            try:
                chapter=item[1]
                # print("wash "+chapter)
                num=getNumOfTitle(chapter)
                
                #不连续，但相差不大,并且到目前为止的章节连续性较好，尝试使用当前章节号
                if abs(num-prev)>=ERROR_RANGE:
                    tmp=prev
                    prev=num
                    num=tmp+1

                #当前为第一章
                if 1==num:
                    #若第一章的计数不为0，说明存在多个第一章 即进入新的【卷】
                    if numOfChapterOne!=0:
                        newcircle=True
                        numOfChapterOne+=1
                if not newcircle:
                    if num>=mx:
                        mx=num
                    if num<=mi:
                        mi=num
                else:
                    mx=0
                    mi=1000000
                    newcircle=False

                l.append(item)
            except Exception as e:
                print(e)
    # print(">>"*20)
    print("max:%d min:%d" % (mx,mi))
    start=mi
    end=mx
    # for i in l:
    #     print(i)
    return l,start,end

def getNumOfTitle_chi(chapter):
    '''
    中文标题:如第一百章

    >>> getNumOfTitle_chi("第两百零一章")
    201
    >>> getNumOfTitle_chi("第两百测零试一章")
    201
    >>> getNumOfTitle_chi("两百")
    -1
    '''
    num=-1
    pattern_chi=re.compile(r'第.+章')
    match_chi=pattern_chi.search(chapter)
    if match_chi:
        chapter=match_chi.group()[1:-1]

        if "两" in chapter:
            chapter=chapter.replace("两","二")

        try:
            num=cn2.c2n(chapter)
        #如果无法从中文转为数字，说明章节名混入了奇怪的字符
        except Exception as e:
            string=""
            pat=re.compile(r'[零一二三四五六七八九十百千两]+')
            match_chi=pat.findall(chapter)
            for i in match_chi:
                string+=i
            num=cn2.c2n(string)
    return num

def getNumOfTitle_d(chapter):
    '''
    数字标题:如第100章

    >>> getNumOfTitle_d("第1029章")
    1029
    '''
    num=-1
    pattern_d=re.compile(r'第\d+章')
    cha=pattern_d.search(chapter)
    if cha:
        rs=cha.group()[1:-1]
        if len(str(rs))>=1:
            num=int(rs)
    return num

def getNumOfTitle(chapter):
    '''
    获得章节编号

    >>> getNumOfTitle("第1029章")
    1029
    >>> getNumOfTitle("第两百零一章")
    201
    >>> getNumOfTitle("第两百测零试一章")
    201
    '''
    num=-1
    #若全数字
    pattern_d=re.compile(r'第\d+章')
    cha=pattern_d.search(chapter)
    if cha:
        num=getNumOfTitle_d(chapter)
    #若其他
    else: 
        num=getNumOfTitle_chi(chapter)
    return num

def getNewChapters(pageUrl,charset="en"):
    lists=getAllChapterLinks(pageUrl)
    novelname_chi=getNovelName_chi(pageUrl)
    #当前读到了
    nowat=sql.readAtChapter(novelname_chi)

    #设置文件名语言en or chi
    if charset=="en":
        # print("using en novelname")
        filename=getNovelName_en(pageUrl)
    else:
        filename=novelname_chi

    l=[]
    isnew=False
    #将新章节的url和name放入l
    for i in lists:
        if i[1]==nowat:
            isnew=True
            continue
        if isnew:
            if not sql.hasChapter(novelname_chi,i[1]):
                l.append(i)
                sql.addChapter(novelname_chi,i[1])

    print("小说标题:%s" % novelname_chi)
    try:
        newest=l[-1][1]
        print("当前已读到%s" % nowat)
        print("最新章节为%s" % newest)
    except Exception as e:
        print("无新章节")
        return ""

    # 构造待发送的文件名：该处理很不健壮！！
    cleanlist=washNovelList(l)
    start=cleanlist[1]
    end=cleanlist[2]
    #构造文件名
    suf=suffix(start,end)
    filename=filename+"#"+suf+".txt"
    #抓取l内的文章
    chapterSpider(l,filename,limit=False)
    print("下载文件成功...")
    sql.setAtChapter(novelname_chi,newest)
    return filename

def suffix(start,end):
    '''
    start(int) end(int) 构造待发送的文件名后缀：230-235 表示从230章到235章

    >>> suffix(23,90)
    '23-90'
    '''
    suf=""
    if start==end:
        suf=str(start)
    else:
        suf=str(start)+"-"+str(end)
    return suf

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
            print("download:%s" %link[1])
            content=getOneChapter(url)
            save2file(filename,content)
            # time.sleep(500)
        except Exception as e:
            traceback.print_exc()

# def test():
    # print("test: getAllChapterLinks && washNovelList ")
    # links=getAllChapterLinks("http://www.shumilou.co/zoujinxiuxian")
    # washNovelList(links)

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
    # import doctest
    # doctest.testmod(verbose=True)
    sql.setAtChapter("惊悚乐园","月初预告之1608")
    sql.test_delChapter("惊悚乐园")
    # sql.setAtChapter("修真四万年","第1306章 文明")
    # NewCapters2kindle("http://www.shumilou.co/xiuzhensiwannian")

            
    
        




