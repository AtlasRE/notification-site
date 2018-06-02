import os
import requests
from bs4 import BeautifulSoup
import re



def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getNewsList(url, newsTitle, hrefList):
    html = getHTMLText(url)
    soup = BeautifulSoup(html, 'html.parser')
    dList = soup.find_all('p', class_="day")
    mList = soup.find_all('p', class_="month")
    nList = soup.find_all('a', href=re.compile("[0-9]{6}\.htm"))
    hList = []
    nTitle = []

    for i in range(len(dList)):
        dData = dList[i].string
        mData = mList[i].string
        Date = mData + '-' + dData
        hList.append(nList[i].attrs['href'])
        title = Date + ' ' + nList[i].string
        nTitle.append(title)

    for title in nTitle:
        newsTitle.append(title.replace('/', '-'))

    for url in hList:
        if url[0] == '.':
            hrefList.append("http://jwc.bit.edu.cn" + url[2:])
        else:
            hrefList.append("http://jwc.bit.edu.cn/tzgg/" + url)

def getNewsDetail(hrefList, newsTitle):
    num = 0
    #fileindex = 'news/newsindex.txt'
    #os.remove(fileindex)
    for i in range(len(hrefList)):
        html = getHTMLText(hrefList[i])
        tag = "<p>1</p>"
        temp = BeautifulSoup(tag, "html.parser")
        p = temp.find('p')
        soup = BeautifulSoup(html, "html.parser")
        article = soup.find('div', class_="article")
        sList = article.contents
        filename = 'NReminder/news/' + newsTitle[i] + '.txt'

        if not os.path.exists(filename):
            num = num + 1
            #with open(fileindex, 'a', encoding='utf-8') as index:
            #    index.write(newsTitle[i] + '.txt\n')

            with open(filename, 'w', encoding='utf-8') as file:
                for sentence in sList:
                    if isinstance(sentence, type(p.next_element)):
                        file.write(sentence)
                    else:
                        for line in sentence.stripped_strings:
                            file.write(line)
            print("File saved successfully: " + newsTitle[i])

    return num

def main():
    menuUrl = "http://jwc.bit.edu.cn/tzgg/index.htm"
    newsTitle = []
    hrefList = []
    getNewsList(menuUrl, newsTitle, hrefList)
    num = getNewsDetail(hrefList, newsTitle)
    print(num, "new files downloaded.\n")

main()