---
layout: post
title: 知乎Python API
description: 为知乎写的Python API，有全部代码及详细解释
categories: Python
tags: 知乎

---

刚学会Python不久，想着做点东西。偶然看到Github上一个为知乎写的Python API，就对其代码做了部分更改并加了详细注释。
下面对代码进行了分析，可以从中体会一下Python中的面向对象编程。
<br/>


### 1. 模拟登录
检查是否已经登录，如果登录继续运行，否则提示其先登录:

{% highlight python %}
#!/usr/bin/python
# -*- encoding: utf-8 -*-
# Build-in / Std
import os, sys, time, platform, random, functools
import re, json, cookielib
# Requirements
import requests, termcolor, html2text
try:
    from bs4 import BeautifulSoup
except:
    import BeautifulSoup
# Some modules written by us
from auth import islogin
from auth import Logging
"""
    Note:
        1. 身份验证由 `auth.py` 完成。
        2. 身份信息保存在当前目录的 `cookies` 文件中。
        3. `requests` 对象可以直接使用，身份信息已经自动加载。

    By Luozijun (https://github.com/LuoZijun), 09/09 2015

"""

# 指示是否运行调试
DEBUG = True


# 加载Cookies
requests = requests.Session()
requests.cookies = cookielib.LWPCookieJar('cookies')
# 检查是否已经登陆成功
try:
    requests.cookies.load(ignore_discard=True)
except:
    Logging.error(u"你还没有登录知乎哦 ...")
    Logging.info(u"执行 `python auth.py` 即可以完成登录。")
    raise Exception("无权限(403)")
if islogin() != True:
    Logging.error(u"你的身份信息已经失效，请重新生成身份信息( `python auth.py` )。")
    raise Exception("无权限(403)")
# 设置文本默认编码为utf8
reload(sys)
sys.setdefaultencoding('utf8')
{% endhighlight %}



### 2. 抽象一个问题类

{% highlight python %}
# 抽象一个问题类
class Question:
    url = None
    soup = None

    # 初始化该问题的url、title
    def __init__(self, url, title=None):
        # 所有问题的url前面都相同，后8位是问题的编号
        if url[0:len(url) - 8] != "http://www.zhihu.com/question/":
            raise ValueError("\"" + url + "\"" + " : it isn't a question url.")
        else:
            self.url = url
        if title != None: self.title = title

    # 获取网页并解析
    def parser(self):
        # 获取该问题的网页
        r = requests.get(self.url)
        # 对问题网页进行解析
        self.soup = BeautifulSoup(r.content)
        # 调试-->将soup结果输出到文件
        if DEBUG:
            f = open('log/question_soup.txt', 'w')
            f.writelines(self.soup.prettify())
            f.close()

    # 装饰器处理Windows下默认的字符编码问题
    def encode_on_windows(func):
        '''
        Decorator for encode result of func on Windows.
        @encode_on_windows
        def func:
            ...
        '''
        @functools.wraps(func)
        def _wrapper(*args, **kw):
            result = func(*args, **kw)
            if platform.system() == 'Windows':
                return result.decode('utf-8').encode('gbk')
            return result
        return _wrapper

    # 获取网页的标题
    @encode_on_windows
    def get_title(self):
        if hasattr(self, "title"):
            return self.title
        if self.soup == None:
            self.parser()
        soup = self.soup
        title = soup.find("h2", class_="zm-item-title")\
                    .string.encode("utf-8").replace("\n", "")
        self.title = title
        return self.title

    # 获取问题的详细描述
    @encode_on_windows
    def get_detail(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        detail = soup.find("div", id="zh-question-detail")\
                     .div.get_text().encode("utf-8")
        return detail

    # 获取答案的数目
    def get_answers_num(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        answers_num = 0
        answers_num_label = soup.find("h3", id="zh-question-answer-num")
        if answers_num_label != None:
            answers_num = int(answers_num_label["data-num"])
        else: 
            raise ValueError('Unexcepted label when get_answer_num')
        return answers_num

    # 获取问题的关注者数目
    def get_followers_num(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        followers_num = 0
        followers_num_label = soup.find("div", class_="zg-gray-normal")
        if followers_num_label != None:
            followers_num = int(followers_num_label.a.strong.string)
        else: 
            raise ValueError('Unexcepted label when get_followers_num')
        return followers_num

    # 获取问题所属的话题
    def get_topics(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        topic_list = soup.find_all("a", class_="zm-item-tag")
        topics = []
        for i in topic_list:
            topic = i.contents[0].encode("utf-8").replace("\n", "")
            if platform.system() == 'Windows':
                topic = topic.decode('utf-8').encode('gbk')
            topics.append(topic)
        return topics

    # 获取该问题对应的所有答案
    def get_all_answers(self):
        answers_num = self.get_answers_num()
        if answers_num == 0:
            # print "No answer."
            return
        error_answer_count = 0
        my_answer_count = 0

        # 每一次请求会返回50个答案
        # 前50个答案，只要抓取对应的URL就可以获得答案
        for j in xrange(min(answers_num, 50)):
            if DEBUG:
                print j
            if self.soup == None:
                self.parser()
            soup = BeautifulSoup(self.soup.encode("utf-8"))
            # DEBUG，输出中间结果
            if DEBUG:
                f = open('log/question_soup_x.txt', 'w')
                f.writelines(soup.prettify())
                f.close()
                # raw_input("Pause, press <Enter> to continue...")
            # 这个答案是自己写的
            is_my_answer = False
            item_answer = soup.find_all("div", class_="zm-item-answer")[j]
            if not item_answer.find("span", class_="count"):
                my_answer_count += 1
                is_my_answer = True
            # 这个答案有问题
            if not item_answer.find("div", class_="zm-editable-content clearfix"):
                error_answer_count += 1
                continue
            author = None
            # 这个答案是匿名用户写的
            author_class = "zm-item-answer-author-info"
            author_info = soup.find_all("div", class_=author_class)[j]
            anoy_name = author_info.find("span", class_="name")
            if anoy_name and anoy_name.string == u"匿名用户":
                author_url = None
                author = User(author_url)
            # 这个答案是非匿名用户写的
            else:
                author_tag = author_info.find_all("a")[1]
                author_id = author_tag.string.encode("utf-8")
                author_url = "http://www.zhihu.com" + author_tag["href"]
                author = User(author_url, author_id)
            # 这个答案有多少赞
            count = ""
            if is_my_answer == True:
                count = item_answer.find("a", class_="zm-item-vote-count").string
            else:
                count = soup.find_all("span", class_="count")\
                            [j - my_answer_count].string
            if count[-1] == "K":
                upvote = int(count[0:(len(count) - 1)]) * 1000
            elif count[-1] == "W":
                upvote = int(count[0:(len(count) - 1)]) * 10000
            else:
                upvote = int(count)
            # 这个答案的URL和内容
            answer_id = soup.find_all("a", class_="answer-date-link")[j]["href"]
            answer_url = "http://www.zhihu.com" + answer_id
            answer = soup.find_all("div", class_=\
                         "zm-editable-content clearfix")[j - error_answer_count]
            soup.body.extract() # 删除soup中网页的body部分并加入一个新的body
            soup.head.insert_after(soup.new_tag("body", **{'class': 'zhi'}))
            soup.body.append(answer) # 添加Answer的内容到body部分
            # 这个答案中的图片，修改每张图片的URL，并删除一些不必要的代码
            img_list = soup.find_all("img", class_="content_image lazy")
            for img in img_list:
                img["src"] = img["data-actualsrc"]
            img_list = soup.find_all("img", \
                           class_="origin_image zh-lightbox-thumb lazy")
            for img in img_list:
                img["src"] = img["data-actualsrc"]
            noscript_list = soup.find_all("noscript")
            for noscript in noscript_list:
                noscript.extract()
            content = soup
            # 用生成器返回一个Answer，这样避免了一次生成耗时间耗内存的问题
            answer = Answer(answer_url, self, author, upvote, content)
            yield answer

        # 超过50个答案，需要点击“加载更多”的情况
        for i in xrange((answers_num-51)/50 + 1):
            # 下标应该从1开始记起
            i += 1
            # 从浏览器中按F12，可以看到是一个post请求，对应的URL如下：
            post_url = "http://www.zhihu.com/node/QuestionAnswerListV2"
            # 从该问题的URL中可以找到_xsrf的值
            _xsrf = self.soup.find("input", attrs={'name': '_xsrf'})["value"]
            # 这是一个偏移量，指示这次请求需要跳过前面多少个答案
            offset = i * 50
            # 发送post请求参数的一部分
            params = json.dumps({"url_token": int(self.url[-8:]),\
                                 "pagesize": 50,\
                                 "offset": offset})
            # 发送post请求的表单数据
            data = {
                '_xsrf': _xsrf,
                'method': "next",
                'params': params
            }
            # 发送post请求的消息头
            header = {
                'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0)"\
                              + " Gecko/20100101 Firefox/34.0",
                'Host': "www.zhihu.com",
                'Referer': self.url
            }
            # 发送post请求
            r = requests.post(post_url, data=data, headers=header)

            # 对这次请求得到的答案进行解析，并返回
            answer_list = r.json()["msg"]
            for j in xrange(min(answers_num-i*50, 50)):
                if DEBUG:
                    print i*50+j
                # 该问题URL的soup解析
                soup = BeautifulSoup(self.soup.encode("utf-8"))
                # 这次请求中的一个答案的soup解析
                answer_soup = BeautifulSoup(answer_list[j])
                # DEBUG，输出中间结果
                if DEBUG:
                    f = open('log/question_soup_x.txt', 'w')
                    f.writelines(answer_soup.prettify())
                    f.close()
                    # raw_input("Pause, press <Enter> to continue...")
                # 这个答案有问题，直接跳过
                if answer_soup.find("div",\
                    class_="zm-editable-content clearfix") == None:
                    continue
                # 这个答案的作者
                author = None
                author_class = "zm-item-answer-author-info"
                author_info = answer_soup.find("div", class_=author_class)
                anoy_name = author_info.find("span", class_="name")
                if anoy_name and anoy_name.string == u"匿名用户":
                    author_url = None
                    author = User(author_url)
                else:
                    author_tag = author_info.find_all("a")[1]
                    author_id = author_tag.string.encode("utf-8")
                    author_url = "http://www.zhihu.com" + author_tag["href"]
                    author = User(author_url, author_id)
                # 这个答案的赞数
                count = answer_soup.find("span", class_="count")
                if count == None:
                    count = answer_soup.find("a", \
                                class_="zm-item-vote-count").string
                else:
                    count = count.string
                if count[-1] == "K":
                    upvote = int(count[0:(len(count) - 1)]) * 1000
                elif count[-1] == "W":
                    upvote = int(count[0:(len(count) - 1)]) * 10000
                else:
                    upvote = int(count)
                # 这个答案的URL和内容
                answer_id = answer_soup.find("a", class_="answer-date-link")["href"]
                answer_url = "http://www.zhihu.com" + answer_id
                answer = answer_soup.find("div", \
                             class_="zm-editable-content clearfix")
                soup.body.extract() # 删除soup中网页的body部分并加入一个新的body
                soup.head.insert_after(soup.new_tag("body", **{'class': 'zhi'}))
                soup.body.append(answer) # 添加Answer的内容到body部分
                # 这个答案中的图片，修改每张图片的URL，并删除一些不必要的代码
                img_list = soup.find_all("img", class_="content_image lazy")
                for img in img_list:
                    img["src"] = img["data-actualsrc"]
                img_list = soup.find_all("img", \
                               class_="origin_image zh-lightbox-thumb lazy")
                for img in img_list:
                    img["src"] = img["data-actualsrc"]
                noscript_list = soup.find_all("noscript")
                for noscript in noscript_list:
                    noscript.extract()
                content = soup
                # 用生成器返回一个Answer，这样避免了一次生成耗时间耗内存的问题
                answer = Answer(answer_url, self, author, upvote, content)
                yield answer

    # 获取前i个答案
    def get_top_i_answers(self, n):
        j = 0
        answers = self.get_all_answers()
        for answer in answers:
            j = j + 1
            if j > n:
                break
            yield answer

    # 获取第1个答案
    def get_top_answer(self):
        for answer in self.get_top_i_answers(1):
            return answer

    # 获取该问题被浏览的次数
    def get_visit_times(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        return int(soup.find("meta", itemprop="visitsCount")["content"])
{% endhighlight %}

