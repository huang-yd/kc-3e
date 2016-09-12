# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import os
#import time
import sys
import socket

socket.setdefaulttimeout(60)

reload(sys)
sys.setdefaultencoding("utf-8")


def filenameFilter(filename):
    result, number = re.subn(r'[\/:*?"><|’]', '', filename)
    return result

""""
def downPaper(url, filename):
    #r = requests.get(url)
    try:
        _filename, number = re.subn(r'[<>:"/\\|?*]', ' ', filename)
        urllib.urlretrieve(url, _filename)
    except socket.timeout as e:
        print e
        return
    except urllib.ContentTooShortError as ctse:
        print ctse
        print u'Error: ' + _filename
        return
    #f = urllib2.urlopen(url)
    #data = f.read()
    #with open(filename, "wb") as code:
    #    code.write(data)
"""

def getKeyword():
    keyDic = []
    #keyStr = str(raw_input(u'Please input the KEYWORDS you want to search(whitespace-separated):\n'))
    keyStr = u''
    for key in keyStr.split():
        keyDic.append(key)
    return keyDic


def getPaperUrl(rooturl):
    response = urllib2.urlopen(rooturl)
    html = response.read()
    pattern = r'<p><a href=.+>.+</a>.*: <b>.*</b><br>.*<i>.+</i>'
    regex = re.compile(pattern)
    urlList = re.findall(regex, html)
    return urlList


def getPaperSeq(url):
    #regexpr = re.compile(r'<p><a href=["]*(.*?)["]*>(.*?)</a>[: ]', re.DOTALL)
    regexpr = re.compile(r'<p><a href=["]*(.*?)["]*>(.*?)</a>', re.DOTALL)
    filename = regexpr.search(url)
    #	print filename.group(1),filename.group(2)
    #print url
    #print regexpr.pattern
    #print filename
    #print filename.group(1)
    return filename.group(1)


def getAuthor(url):
    regexpr = re.compile(r': <b>(.*?)</b><br>', re.DOTALL)
    authors = regexpr.search(url)
    #	print authors.group(1)
    return authors.group(1)


def getPaperName(url):
    regexpr = re.compile(r'<br><i>(.*?)</i>', re.DOTALL)
    papername = regexpr.search(url)
    #	print papername.group(1)
    return papername.group(1)


def filterUrl(urlList, keywordDic):
    newUrlList = []
    #filterFlag = str(raw_input(u'Filter keyword ? y or n:\n'))
    filterFlag = u'n'
    print filterFlag
    if cmp(filterFlag, u'n') == 0:
        return urlList
    for url in urlList:
        filename = getPaperSeq(url)
        authors = getAuthor(url)  # 可用于过滤作者
        papername = getPaperName(url)
        if len(keywordDic) != 0:
            flag = 0
            for i in range(0, len(keywordDic)):
                ret = papername.lower().find(keywordDic[i].lower())
                if ret == -1:
                    flag = 1
            if flag == 0:
                newUrlList.append(url)
    return newUrlList


def downloadPaper(rooturl, urlList, dic, loc):
    no = 0
    u = urllib2.urlopen(rooturl)
    newRooturl = u.geturl()
    newRooturl, number = re.subn(r'/#[0-9]*[/]', '/', newRooturl)
    for url in urlList:
        paperSeq = getPaperSeq(url)
        authors = getAuthor(url)
        papername = getPaperName(url)
        #firstauthor = authors.split(';')[0]
        author = ''
        for people in authors.split(';'):
            author = author + people + '_'
        #print newRooturl + paperSeq
        """only for sequence L"""
        print paperSeq
        """only for sequence L"""
        papername = filenameFilter(papername)
        _author = re.sub(r'[<>:"/\\|?*]', '_', author)
        _papername = re.sub(r'[<>:"/\\|?*]', '_', papername)
        #print _author
        #print _papername
        #fileName = dic + loc[2:5] + u'_' + _author + _papername
        #fileName = dic + loc[2:5] + u'_' + _papername
        _paperSeq = re.sub(r'[<>:"/\\|?*]', '_', paperSeq)
        fileName = dic + _paperSeq
        #print fileName
        if len(fileName) > 200:
            fileName = fileName[0:200]
        fileName += u'.pdf'
        fileName = fileName.decode("utf-8")
        #fileName = fileName.decode("GBK")
        no += 1
        if os.path.exists(fileName):
            print str(no) + u' The paper "' + _paperSeq + u'" has already been downloaded.'
        elif os.path.exists(fileName) == False:
            #downPaper(newRooturl + paperSeq, fileName)
            try:
                #urllib.urlretrieve(newRooturl + paperSeq, fileName)
                """only for sequence L"""
                urllib.urlretrieve(paperSeq, fileName)
                """only for sequence L"""
                print str(no) + u' Finish downloading the paper：' + _paperSeq
            except socket.timeout as e:
                print e
                print u'retry downloading the paper: ' + _paperSeq + u' soon.'
                urlList.append(url)
                if os.path.exists(fileName):
                    os.remove(fileName)
            except urllib.ContentTooShortError as ctse:
                print ctse
                print u'retry downloading the paper: ' + _paperSeq + u' soon.'
                urlList.append(url)
                if os.path.exists(fileName):
                    os.remove(fileName)


def getConfLoc(url):
    regexpr = re.compile(r'<a href="(.*?)">.*</a>', re.DOTALL)
    loc = regexpr.search(url)
    return loc.group(1)


def getConfTime(url):
    regexpr = re.compile(r'<a href=".*">(.*?)</a>', re.DOTALL)
    years = regexpr.search(url)
    time = years.group(1)
    if time == '74-79':
        return '1974-1979'
    else:
        if int(time) > 50:
            return '19' + time
        else:
            return '20' + time


def showOneConf(pattern, html, regex, locMap):
    regexpr = re.compile(pattern, re.DOTALL)
    #print regexpr.pattern
    block = regexpr.search(html)
    #print block.group(1)
    List = re.findall(regex, block.group(1))
    no = len(locMap) + 1
    for i in range(len(List)):
        print '[' + str(no) + ']:' + getConfTime(List[i]),
        if getConfLoc(List[i]).endswith('/') == False:
            #			print List[i]
            locMap[no] = getConfLoc(List[i]) + '/'
        else:
            locMap[no] = getConfLoc(List[i])
        no += 1
    print '\n'


def showAllConference(rooturl, locMap):
    response = urllib2.urlopen(rooturl)
    html = response.read()
    pattern = r'<a href="[A-Z0-9/]+">[-0-9]+</a>'
    regex = re.compile(pattern)
    no = 1
    CLpattern = r'<tr><th title="Computational Linguistics Journal">CL:</th>(.*?)</td></tr>'
    TACLpattern = r'<tr><th title="Transactions of the Association of the Computational Linguistics">TACL:</th>(.*?)</td></tr>'
    ACLpattern = r'<tr><th title="ACL Annual Meeting">ACL:</th>(.*?)</td></tr>'
    EACLpattern = r'<tr><th title="European Chapter of ACL">EACL:</th>(.*?)</td></tr>'
    NAACLpattern = r'<tr><th title="North American Chapter of ACL">NAACL:</th>(.*?)</td></tr>'
    EMNLPpattern = r'<tr><th title=.*>EMNLP:</th>(.*?)</td></tr>'
    CoNLLpattern = r'<tr><th title="Conference on Computational Natural Language Learning">CoNLL:</th>(.*?)</td></tr>'
    SemEvalpattern = r'<tr><th title="Lexical and Computational Semantics and Semantic Evaluation.*">\*Sem.*SemEval:</th>(.*?)</td>'
    ANLPpattern = r'<tr><th title="Applied Natural Language Processing Conference">ANLP:</th>(.*?)</td></tr>'
    Workshopspattern = r'<tr><th title="Complete workshop listing, sorted by year">Workshops:</th>(.*?)</td></tr>'
    SIGspattern = r'<tr><th title="Special Interest Group Meetings">SIGs:</th>(.*?)</td></tr>'
    COLINGpattern = r'<tr><th title=.*>COLING:</th>(.*?)</td></tr>'
    HLTpattern = r'<tr><th title=.*>HLT:</th>(.*?)</td></tr>'
    IJCNLPpattern = r'<tr><th title=.*>IJCNLP:</th>(.*?)</td>'
    LRECpattern = r'<tr><th title=.*>LREC:</th>(.*?)</td>'
    PACLICpattern = r'<tr><th title=.*>PACLIC</th>(.*?)</td>'
    Rocling_IJCLCLPpattern = r'<tr><th title=.*>Rocling/IJCLCLP</th>(.*?)</td>'
    TINLAPpattern = r'<tr><th title=.*>TINLAP:</th>(.*?)</td>'
    ALTApattern = r'<tr><th title=.*>ALTA</th>(.*?)</td>'
    RANLPpattern = r'<th title=.*>RANLP</th>(.*?)</tr>'
    JEP_TALN_RECITALpattern = r'<tr><th title=.*>JEP/TALN/RECITAL</th>(.*?)</td>'
    MUCpattern = r'<tr><th title=.*>MUC:</th>(.*?)</td>'
    Tipsterpattern = r'<tr><th title=.*>Tipster:</th>(.*?)</td>'

    """
    print 'CL:'
    showOneConf(CLpattern, html, regex, locMap)
    print 'TACL:'
    showOneConf(TACLpattern, html, regex, locMap)
    print 'ACL:'
    showOneConf(ACLpattern, html, regex, locMap)
    print 'EACL:'
    showOneConf(EACLpattern, html, regex, locMap)
    print 'NAACL:'
    showOneConf(NAACLpattern, html, regex, locMap)
    print 'EMNLP:'
    showOneConf(EMNLPpattern, html, regex, locMap)
    print 'CoNLL:'
    showOneConf(CoNLLpattern, html, regex, locMap)
    print '*Sem/SemEval:'
    showOneConf(SemEvalpattern, html, regex, locMap)
    print 'ANLP:'
    showOneConf(ANLPpattern, html, regex, locMap)
    print 'Workshops:'
    showOneConf(Workshopspattern, html, regex, locMap)
    #print 'SIGs:'
    #showOneConf(SIGspattern, html, regex, locMap)
    print 'COLING:'
    showOneConf(COLINGpattern, html, regex, locMap)
    print 'HLT:'
    showOneConf(HLTpattern, html, regex, locMap)
    print 'IJCNLP:'
    showOneConf(IJCNLPpattern, html, regex, locMap)
    """
    print 'LREC:'
    showOneConf(LRECpattern, html, regex, locMap)
    """
    print 'PACLIC:'
    showOneConf(PACLICpattern, html, regex, locMap)
    print 'Rocling/IJCLCLP:'
    showOneConf(Rocling_IJCLCLPpattern, html, regex, locMap)
    print 'TINLAP:'
    showOneConf(TINLAPpattern, html, regex, locMap)
    print 'ALTA:'
    showOneConf(ALTApattern, html, regex, locMap)
    print 'RANLP:'
    showOneConf(RANLPpattern, html, regex, locMap)
    print 'JEP/TALN/RECITAL:'
    showOneConf(JEP_TALN_RECITALpattern, html, regex, locMap)
    print 'MUC:'
    showOneConf(MUCpattern, html, regex, locMap)
    print 'Tipster:'
    showOneConf(Tipsterpattern, html, regex, locMap)
    """


def getLocation(rooturl):
    locMap = {}
    locList = []
    showAllConference(rooturl, locMap)
    begin = 1
    end = len(locMap)
    #print begin, end
    #idStr = str(raw_input(
    #    u'Please input the conference [ID],splited by whitespace. You can input consecutive ID by \'-\',such as \'1-30\':\n'))
    idStr = str(begin) + '-' + str(end)
    #print idStr
    #return locList
    idList = idStr.split()
    for id in idList:
        spanSet = id.split('-')
        if len(spanSet) == 2:
            for i in range(int(spanSet[0]), int(spanSet[1]) + 1):
                locList.append(locMap[i])
        else:
            locList.append(locMap[int(id)])
    return locList


def getKeyStr(keywordDic):
    ss = ''
    for key in keywordDic:
        ss += key
        ss += '_'
    return ss


root_url = 'http://aclweb.org/anthology/'

if __name__ == '__main__':
    locList = getLocation(root_url)
    keywordDic = getKeyword()
    no = 1
    #dic = getKeyStr(keywordDic)
    #currTime = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
    #dic += currTime
    #dic = 'G:/gongkechuang-3e/NLPPaperCrawler/PaperAnthology'
    #print sys.argv[1]
    dic = sys.argv[1]
    if os.path.exists(dic) == False:
        os.mkdir(dic)
    dic += '/'
    for loc in locList:
        downurl = root_url + loc
        print u'Please CHECK the URL:', downurl
        urlList = getPaperUrl(downurl)
        print len(urlList)
        new_urlList = filterUrl(urlList, keywordDic)
        print u'filter complete ' + str(len(urlList)) + ' -> ' + str(len(new_urlList))
        _dic = dic + loc[2:5]
        if os.path.exists(_dic) == False:
            os.mkdir(_dic)
        _dic += '/'
        downloadPaper(downurl, new_urlList, _dic, loc)
        print u'Download ' + str(no) + u' tasks successfully'
        no += 1
    print 'Done!^_^'
