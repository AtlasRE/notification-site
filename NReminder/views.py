from django.shortcuts import render
import os
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

class Article():
    def __init__(self, title, id, date):
        self.title = title
        self.id = id
        self.date = date

def getfilelist():
    dir = 'NReminder/news/'
    article_list = []
    i = 1
    for title in os.listdir(dir):
        article = Article(title[11:-4], i, title[:10])
        article_list.append(article)
        i = i + 1
    article_list.reverse()
    return article_list


def homepage(request):
    article_list = getfilelist()
    paginator = Paginator(article_list, 20)
    page = request.GET.get('page')
    try:
        articlelist = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articlelist = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articlelist = paginator.page(paginator.num_pages)

    return render(request, "index.html", {"filelist": articlelist})

def get_content(request, article_id):
    article_list = getfilelist()
    article_content = []
    for article in article_list:
        if article_id == article.id:
            title = article.title
            path = 'NReminder/news/' + article.date + ' ' + article.title + '.txt'
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    article_content.append(line)
            break
        else:
            pass

    return render(request, "content.html", {"title": title, "article": article_content})

def archive(request):
    article_list = getfilelist()
    datelist = []
    for article in article_list:
        if article.date[:7] not in datelist:
            datelist.append(article.date[:7])


    return render(request, "archive.html", {"datelist": datelist, "filelist": article_list})