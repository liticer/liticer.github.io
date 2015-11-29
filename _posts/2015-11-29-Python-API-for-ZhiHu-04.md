---
layout: post
title: Python爬虫遇上知乎(六)
description: 使用简单的Python脚本登录知乎，轻松地进行一些监控、搜索、备份工作
categories: Python
tags: Requests Termcolor

---

<p>
使用Python爬虫登录知乎，就可以轻松地进行一些监控、搜索、备份工作。慢慢地，你会发现Python真的很强大。
<font color="blue"><strong>
本文主要介绍在模拟登录知乎之后，如何用Python为知乎写一些API。主要是采用面向对象编程的思想，分别对Question、User、Answer、Collection
进行抽象，接前面开始介绍Collection类。
</strong></font>
</p>


最后贴上源代码。以下代码原来出自: <br/>
<https://github.com/egrcc/zhihu-python> <br/>
我对代码进行修改，并加了详细的注释：<br/>
<https://github.com/liticer/zhihu_python> <br/>
应该比较容易阅读，如发现问题可以及时留言。
<p/>
<br/>

<strong>附: zhihu.py</strong>

<pre class="prettyPrint lang=python">
# 抽象一个收藏夹类
class Collection:
    url = None
    soup = None

    # 初始化url、name、creator变量
    def __init__(self, url, name=None, creator=None):
        if url[0:len(url) - 8] != "http://www.zhihu.com/collection/":
            raise ValueError("\""+url+"\""+" : it isn't a collection url.")
        else:
            self.url = url
            if name != None:
                self.name = name
            if creator != None:
                self.creator = creator

    # 获取该收藏夹对应的网页并解析
    def parser(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content)
        self.soup = soup

    # 获取该收藏夹的名字
    def get_name(self):
        if not hasattr(self, 'name'):
            if self.soup == None:
                self.parser()
            soup = self.soup
            name_l = self.soup.find("h2", id="zh-fav-head-title")
            self.name = name_l.string.encode("utf-8").strip()
        if platform.system() == 'Windows':
            return self.name.decode('utf-8').encode('gbk')
        return self.name

    # 获取该收藏夹的创建者
    def get_creator(self):
        if not hasattr(self, 'creator'):
            if self.soup == None:
                self.parser()
            creator_l = self.soup.find("h2", class_="zm-list-content-title")
            creator_id = creator_l.a.string.encode("utf-8")
            creator_url = "http://www.zhihu.com" + creator_l.a["href"]
            creator = User(creator_url, creator_id)
            self.creator = creator
        return creator

    # 获取该收藏夹下的所有答案
    def get_all_answers(self):
        i = 1
        while True:
            r = requests.get(self.url + "?page=" + str(i))
            answer_soup = BeautifulSoup(r.content)
            answer_list = answer_soup.find_all("div", class_="zm-item")
            if len(answer_list) == 0:
                break
            for answer in answer_list:
                if answer.find("p", class_="note"):
                    continue
                question_l= answer.find("h2")
                if question_l != None:
                    question_u = "http://www.zhihu.com" + question_l.a["href"]
                    question_t = question_l.a.string.encode("utf-8")
                question = Question(question_u, question_t)
                answer_l = answer.find("span", class_="answer-date-link-wrap")
                answer_url = "http://www.zhihu.com" + answer_l.a["href"]
                author = None
                amswer_l = answer.find("h3", class_="zm-item-answer-author-wrap")
                if answer_l.string == u"匿名用户":
                    author_url = None
                    author = User(author_url)
                else:
                    author_tag = answer_l.find_all("a")[0]
                    author_id = author_tag.string.encode("utf-8")
                    author_url = "http://www.zhihu.com" + author_tag["href"]
                    author = User(author_url, author_id)
                yield Answer(answer_url, question, author)
        i = i + 1

    # 获取该收藏夹下前n个答案
    def get_top_i_answers(self, n):
        j = 0
        answers = self.get_all_answers()
        for answer in answers:
            j = j + 1
            if j > n:
                break
            yield answer
</pre>

