---
layout: post
title:  "知乎Python API"
date:  2015-11-25 15:39:10
comments: true
categories: Python
tags: 知乎
archive: false
---


{% highlight python %}
# Build-in / Std
import os, sys, time, platform, random
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
        1. 身份验证由 'auth.py' 完成。
        2. 身份信息保存在当前目录的 'cookies' 文件中。
        3. 'requests' 对象可以直接使用，身份信息已经自动加载。
    By Luozijun (https://github.com/LuoZijun), 09/09 2015
"""
 
# 加载Cookies
requests = requests.Session()
requests.cookies = cookielib.LWPCookieJar('cookies')
# 检查是否已经登陆成功
try:
    requests.cookies.load(ignore_discard=True)
except:
    Logging.error(u"你还没有登录知乎哦 ...")
    Logging.info(u"执行 'python auth.py' 即可以完成登录。")
    raise Exception("无权限(403)")
if islogin() != True:
    Logging.error(u"你的身份信息已经失效，请重新生成身份信息( 'python auth.py' )。")
    raise Exception("无权限(403)")
# 设置文本默认编码为utf8
reload(sys)
sys.setdefaultencoding('utf8')
{% endhighlight %}


# 抽象一个问题类
class Question:
    url = None
    soup = None

    # 初始化该问题的url、title
    def __init__(self, url, title=None):
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
        f = open('log/question_soup.txt', 'w')
        f.writelines(self.soup.prettify())
        f.close()

    # 获取网页的标题
    def get_title(self):
        if hasattr(self, "title"):
            if platform.system() == 'Windows':
                title = self.title.decode('utf-8').encode('gbk')
                return title
            else:
                return self.title
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            title = soup.find("h2", class_="zm-item-title").string.encode("utf-8").replace("\n", "")
            self.title = title
            if platform.system() == 'Windows':
                title = title.decode('utf-8').encode('gbk')
                return title
            else:
                return title

    # 获取问题的详细描述
    def get_detail(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        detail = soup.find("div", id="zh-question-detail").div.get_text().encode("utf-8")
        if platform.system() == 'Windows':
            detail = detail.decode('utf-8').encode('gbk')
            return detail
        else:
            return detail

    # 获取答案的数目
    def get_answers_num(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        answers_num = 0
        if soup.find("h3", id="zh-question-answer-num") != None:
            answers_num = int(soup.find("h3", id="zh-question-answer-num")["data-num"])
        return answers_num

    # 获取问题的关注者数目
    def get_followers_num(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        followers_num = int(soup.find("div", class_="zg-gray-normal").a.strong.string)
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
            print "No answer."
            return
        else:
            # 每一次请求会返回50个答案
            error_answer_count = 0
            my_answer_count = 0
            for i in xrange((answers_num - 1) / 50 + 1):
                # 前50个答案，只要抓取对应的URL就可以获得答案
                if i == 0:

                    for j in xrange(min(answers_num, 50)):
                        print j
                        if self.soup == None:
                            self.parser()
                        soup = BeautifulSoup(self.soup.encode("utf-8"))
                        # 这个答案是自己写的
                        is_my_answer = False
                        if soup.find_all("div", class_="zm-item-answer")[j].find("span", class_="count") == None:
                            my_answer_count += 1
                            is_my_answer = True
                        # 这个答案有问题
                        if soup.find_all("div", class_="zm-item-answer")[j].find("div", class_="zm-editable-content clearfix") == None:
                            error_answer_count += 1
                            continue
                        author = None
                        # 这个答案是匿名用户写的
                        anoy_name_span = soup.find_all("div", class_="zm-item-answer-author-info")[j].find("span", class_="name")
                        if anoy_name_span and anoy_name_span.string == u"匿名用户":
                            author_url = None
                            author = User(author_url)
                        # 这个答案是非匿名用户写的
                        else:
                            author_tag = soup.find_all("div", class_="zm-item-answer-author-info")[j].find_all("a")[1]
                            author_id = author_tag.string.encode("utf-8")
                            author_url = "http://www.zhihu.com" + author_tag["href"]
                            author = User(author_url, author_id)
                        # 这个答案有多少赞
                        if is_my_answer == True:
                            count = soup.find_all("div", class_="zm-item-answer")[j].find("a", class_="zm-item-vote-count").string
                        else:
                            count = soup.find_all("span", class_="count")[j - my_answer_count].string
                        if count[-1] == "K":
                            upvote = int(count[0:(len(count) - 1)]) * 1000
                        elif count[-1] == "W":
                            upvote = int(count[0:(len(count) - 1)]) * 10000
                        else:
                            upvote = int(count)
                        # 这个答案的URL和内容
                        answer_url = "http://www.zhihu.com" + soup.find_all("a", class_="answer-date-link")[j]["href"]
                        answer = soup.find_all("div", class_="zm-editable-content clearfix")[j - error_answer_count]
                        soup.body.extract()
                        soup.head.insert_after(soup.new_tag("body", **{'class': 'zhi'}))
                        soup.body.append(answer)
                        # 这个答案中的图片
                        img_list = soup.find_all("img", class_="content_image lazy")
                        for img in img_list:
                            img["src"] = img["data-actualsrc"]
                        img_list = soup.find_all("img", class_="origin_image zh-lightbox-thumb lazy")
                        for img in img_list:
                            img["src"] = img["data-actualsrc"]
                        noscript_list = soup.find_all("noscript")
                        for noscript in noscript_list:
                            noscript.extract()
                        content = soup
                        # 用生成器返回一个Answer，这样避免了一次生成耗时间耗内存的问题
                        answer = Answer(answer_url, self, author, upvote, content)
                        yield answer

                else:

                    # 超过50个答案，需要点击“加载更多”的情况
                    # 从浏览器中按F12，可以看到是一个post请求，对应的URL如下：
                    post_url = "http://www.zhihu.com/node/QuestionAnswerListV2"
                    # 从该问题的URL中可以找到_xsrf的值
                    _xsrf = self.soup.find("input", attrs={'name': '_xsrf'})["value"]
                    offset = i * 50
                    # 发送post请求参数的一部分
                    params = json.dumps(
                        {"url_token": int(self.url[-8:-1] + self.url[-1]), "pagesize": 50, "offset": offset})
                    # 发送post请求的表单数据
                    data = {
                        '_xsrf': _xsrf,
                        'method': "next",
                        'params': params
                    }
                    # 发送post请求的消息头
                    header = {
                        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
                        'Host': "www.zhihu.com",
                        'Referer': self.url
                    }
                    # 发送post请求
                    r = requests.post(post_url, data=data, headers=header)

                    # 对这次请求得到的答案进行解析，并返回
                    answer_list = r.json()["msg"]
                    for j in xrange(min(answers_num - i * 50, 50)):
                        print i*50+j
                        # 该问题URL的soup解析
                        soup = BeautifulSoup(self.soup.encode("utf-8"))
                        # 这次请求中的一个答案的soup解析
                        answer_soup = BeautifulSoup(answer_list[j])
                        # Debug
                        # fx = open('log/question_soup_x.txt', 'w')
                        # fx.writelines(answer_soup.prettify())
                        # fx.close()
                        # raw_input("Pause, press <Enter> to continue...")
                        # 这个答案有问题，直接跳过
                        if answer_soup.find("div", class_="zm-editable-content clearfix") == None:
                            continue
                        # 这个答案的作者
                        author = None
                        anoy_name = answer_soup.find("div", class_="zm-item-answer-author-info").find("span", class_="name")
                        if anoy_name and anoy_name.string == u"匿名用户":
                            author_url = None
                            author = User(author_url)
                        else:
                            author_tag = answer_soup.find("div", class_="zm-item-answer-author-info").find_all("a")[1]
                            author_id = author_tag.string.encode("utf-8")
                            author_url = "http://www.zhihu.com" + author_tag["href"]
                            author = User(author_url, author_id)
                        # 这个答案的赞数
                        if answer_soup.find("span", class_="count") == None:
                            count = answer_soup.find("a", class_="zm-item-vote-count").string
                        else:
                            count = answer_soup.find("span", class_="count").string
                        if count[-1] == "K":
                            upvote = int(count[0:(len(count) - 1)]) * 1000
                        elif count[-1] == "W":
                            upvote = int(count[0:(len(count) - 1)]) * 10000
                        else:
                            upvote = int(count)
                        # 这个答案的URL和内容
                        answer_url = "http://www.zhihu.com" + answer_soup.find("a", class_="answer-date-link")["href"]
                        answer = answer_soup.find("div", class_="zm-editable-content clearfix")
                        # 这个答案中的图片
                        soup.body.extract()
                        soup.head.insert_after(soup.new_tag("body", **{'class': 'zhi'}))
                        soup.body.append(answer)
                        img_list = soup.find_all("img", class_="content_image lazy")
                        for img in img_list:
                            img["src"] = img["data-actualsrc"]
                        img_list = soup.find_all("img", class_="origin_image zh-lightbox-thumb lazy")
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
        # if n > self.get_answers_num():
        # n = self.get_answers_num()
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



# 抽象一个用户类
class User:
    user_url = None
    soup = None

    # 初始化该用户的url、user_id
    def __init__(self, user_url, user_id=None):
        if user_url == None:
            self.user_id = "匿名用户"
        elif user_url[0:28] != "http://www.zhihu.com/people/":
            raise ValueError("\"" + user_url + "\"" + " : it isn't a user url.")
        else:
            self.user_url = user_url
            if user_id != None:
                self.user_id = user_id

    # 获取用户主页并解析
    def parser(self):
        r = requests.get(self.user_url)
        soup = BeautifulSoup(r.content)
        self.soup = soup

    # 获取用户名
    def get_user_id(self):
        if self.user_url == None:
            # print "I'm anonymous user."
            if platform.system() == 'Windows':
                return "匿名用户".decode('utf-8').encode('gbk')
            else:
                return "匿名用户"
        else:
            if hasattr(self, "user_id"):
                if platform.system() == 'Windows':
                    return self.user_id.decode('utf-8').encode('gbk')
                else:
                    return self.user_id
            else:
                if self.soup == None:
                    self.parser()
                soup = self.soup
                user_id = soup.find("div", class_="title-section ellipsis") \
                    .find("span", class_="name").string.encode("utf-8")
                self.user_id = user_id
                if platform.system() == 'Windows':
                    return user_id.decode('utf-8').encode('gbk')
                else:
                    return user_id

    # 获取关注该用户的人总数
    def get_followees_num(self):
        if self.user_url == None:
            # print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            followees_num = int(soup.find("div", class_="zm-profile-side-following zg-clear") \
                                .find("a").strong.string)
            return followees_num

    # 获取该用户关注的人总数
    def get_followers_num(self):
        if self.user_url == None:
            # print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            followers_num = int(soup.find("div", class_="zm-profile-side-following zg-clear") \
                                .find_all("a")[1].strong.string)
            return followers_num

    # 获取该用户获得赞数
    def get_agree_num(self):
        if self.user_url == None:
            # print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            agree_num = int(soup.find("span", class_="zm-profile-header-user-agree").strong.string)
            return agree_num

    # 获取该用户获得的感谢数
    def get_thanks_num(self):
        if self.user_url == None:
            #print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            thanks_num = int(soup.find("span", class_="zm-profile-header-user-thanks").strong.string)
            return thanks_num

    # 获取该用户提问的问题数
    def get_asks_num(self):
        if self.user_url == None:
            # print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            asks_num = int(soup.find_all("span", class_="num")[0].string)
            return asks_num

    # 获取该用户回答的问题数
    def get_answers_num(self):
        if self.user_url == None:
            # print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            answers_num = int(soup.find_all("span", class_="num")[1].string)
            return answers_num

    # 获取该用户收藏夹数
    def get_collections_num(self):
        if self.user_url == None:
            print "I'm anonymous user."
            return 0
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            collections_num = int(soup.find_all("span", class_="num")[3].string)
            return collections_num

    # 获取关注该用户的人
    def get_followees(self):
        if self.user_url == None:
            # print "I'm anonymous user."
            return
            # yield
        else:
            followees_num = self.get_followees_num()
            if followees_num == 0:
                return
                # yield
            else:
                # 获取关注该用户的用户页页面并解析
                followee_url = self.user_url + "/followees"
                r = requests.get(followee_url)
                soup = BeautifulSoup(r.content)
                # 对于每20个用户发送一次请求
                for i in xrange((followees_num - 1) / 20 + 1):
                    # 首次不用发送请求，因为已经获取到页面了
                    if i == 0:
                        user_url_list = soup.find_all("h2", class_="zm-list-content-title")
                        for j in xrange(min(followees_num, 20)):
                            yield User(user_url_list[j].a["href"], user_url_list[j].a.string.encode("utf-8"))
                    # 发送post请求，再获取20个关注者
                    else:
                        # 将要发送post请求的URL
                        post_url = "http://www.zhihu.com/node/ProfileFolloweesListV2"
                        # 准备发送该post请求的参数
                        _xsrf = soup.find("input", attrs={'name': '_xsrf'})["value"]
                        offset = i * 20
                        hash_id = re.findall("hash_id&quot;: &quot;(.*)&quot;},", r.text)[0]
                        params = json.dumps({"offset": offset, "order_by": "created", "hash_id": hash_id})
                        data = {
                            '_xsrf': _xsrf,
                            'method': "next",
                            'params': params
                        }
                        # 准备发送该post请求的消息头
                        header = {
                            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
                            'Host': "www.zhihu.com",
                            'Referer': followee_url
                        }
                        # 发送post请求
                        r_post = requests.post(post_url, data=data, headers=header)
                        # 获取关注者列表
                        followee_list = r_post.json()["msg"]
                        for j in xrange(min(followees_num - i * 20, 20)):
                            followee_soup = BeautifulSoup(followee_list[j])
                            user_link = followee_soup.find("h2", class_="zm-list-content-title").a
                            yield User(user_link["href"], user_link.string.encode("utf-8"))

    # 获取该用户关注的用户列表
    def get_followers(self):
        if self.user_url == None:
            # print "I'm anonymous user."
            return
            # yield
        else:
            followers_num = self.get_followers_num()
            if followers_num == 0:
                return
                # yield
            else:
                # 获取关注者页面并解析
                follower_url = self.user_url + "/followers"
                r = requests.get(follower_url)
                soup = BeautifulSoup(r.content)
                for i in xrange((followers_num - 1) / 20 + 1):
                    # 首次不用再get，因为前面已经获取过了
                    if i == 0:
                        user_url_list = soup.find_all("h2", class_="zm-list-content-title")
                        for j in xrange(min(followers_num, 20)):
                            yield User(user_url_list[j].a["href"], user_url_list[j].a.string.encode("utf-8"))
                    # 发送post请求，再获取20个关注者
                    else:
                        # 发送post请求的地址
                        post_url = "http://www.zhihu.com/node/ProfileFollowersListV2"
                        # 发送post请求的参数
                        _xsrf = soup.find("input", attrs={'name': '_xsrf'})["value"]
                        offset = i * 20
                        hash_id = re.findall("hash_id&quot;: &quot;(.*)&quot;},", r.text)[0]
                        params = json.dumps({"offset": offset, "order_by": "created", "hash_id": hash_id})
                        data = {
                            '_xsrf': _xsrf,
                            'method': "next",
                            'params': params
                        }
                        # 发送post请求的消息头
                        header = {
                            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
                            'Host': "www.zhihu.com",
                            'Referer': follower_url
                        }
                        # 发送post请求
                        r_post = requests.post(post_url, data=data, headers=header)
                        # 解析请求的结果，得到关注者列表
                        follower_list = r_post.json()["msg"]
                        for j in xrange(min(followers_num - i * 20, 20)):
                            follower_soup = BeautifulSoup(follower_list[j])
                            user_link = follower_soup.find("h2", class_="zm-list-content-title").a
                            yield User(user_link["href"], user_link.string.encode("utf-8"))

    # 获取该用户提问的问题
    def get_asks(self):
        if self.user_url == None:
            # print "I'm anonymous user."
            return
            # yield
        else:
            asks_num = self.get_asks_num()
            if asks_num == 0:
                return
                yield
            else:
                for i in xrange((asks_num - 1) / 20 + 1):
                    # 每20个问题发送一次get请求，得到请求结果并解析
                    ask_url = self.user_url + "/asks?page=" + str(i + 1)
                    r = requests.get(ask_url)
                    soup = BeautifulSoup(r.content)
                    for question in soup.find_all("a", class_="question_link"):
                        url = "http://www.zhihu.com" + question["href"]
                        title = question.string.encode("utf-8")
                        yield Question(url, title)

    # 获取该用户写过的答案
    def get_answers(self):
        if self.user_url == None:
            # print "I'm anonymous user."
            return
            # yield
        else:
            answers_num = self.get_answers_num()
            if answers_num == 0:
                return
                # yield
            else:
                for i in xrange((answers_num - 1) / 20 + 1):
                    # 每20个答案发送一次get请求，获得结果并解析
                    answer_url = self.user_url + "/answers?page=" + str(i + 1)
                    r = requests.get(answer_url)
                    soup = BeautifulSoup(r.content)
                    for answer in soup.find_all("a", class_="question_link"):
                        question_url = "http://www.zhihu.com" + answer["href"][0:18]
                        question_title = answer.string.encode("utf-8")
                        question = Question(question_url, question_title)
                        yield Answer("http://www.zhihu.com" + answer["href"], question, self)

    # 获取该用户的收藏夹
    def get_collections(self):
        if self.user_url == None:
            # print "I'm anonymous user."
            return
            # yield
        else:
            collections_num = self.get_collections_num()
            if collections_num == 0:
                return
                # yield
            else:
                for i in xrange((collections_num - 1) / 20 + 1):
                    # 每20个收藏夹发送一次post请求，获取结果并解析
                    collection_url = self.user_url + "/collections?page=" + str(i + 1)  
                    r = requests.get(collection_url)
                    soup = BeautifulSoup(r.content)
                    for collection in soup.find_all("div", class_="zm-profile-section-item zg-clear"):
                        url = "http://www.zhihu.com" + \
                              collection.find("a", class_="zm-profile-fav-item-title")["href"]
                        name = collection.find("a", class_="zm-profile-fav-item-title").string.encode("utf-8")
                        yield Collection(url, name, self)



# 抽象一个答案类
class Answer:
    answer_url = None
    soup = None

    # 初始化该答案的url、question、author、upvote、content
    def __init__(self, answer_url, question=None, author=None, upvote=None, content=None):
        self.answer_url = answer_url
        if question != None:
            self.question = question
        if author != None:
            self.author = author
        if upvote != None:
            self.upvote = upvote
        if content != None:
            self.content = content

    # 获取答案页面并解析
    def parser(self):
        r = requests.get(self.answer_url)
        soup = BeautifulSoup(r.content)
        self.soup = soup

    # 获取答案对应的问题
    def get_question(self):
        if hasattr(self, "question"):
            return self.question
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            question_link = soup.find("h2", class_="zm-item-title zm-editable-content").a
            url = "http://www.zhihu.com" + question_link["href"]
            title = question_link.string.encode("utf-8")
            question = Question(url, title)
            return question

    # 获取答案的作者
    def get_author(self):
        if hasattr(self, "author"):
            return self.author
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            if soup.find("h3", class_="zm-item-answer-author-wrap").string == u"匿名用户":
                author_url = None
                author = User(author_url)
            else:
                author_tag = soup.find("h3", class_="zm-item-answer-author-wrap").find_all("a")[1]
                author_id = author_tag.string.encode("utf-8")
                author_url = "http://www.zhihu.com" + author_tag["href"]
                author = User(author_url, author_id)
            return author

    def get_upvote(self):
        if hasattr(self, "upvote"):
            return self.upvote
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            count = soup.find("span", class_="count").string
            if count[-1] == "K":
                upvote = int(count[0:(len(count) - 1)]) * 1000
            elif count[-1] == "W":
                upvote = int(count[0:(len(count) - 1)]) * 10000
            else:
                upvote = int(count)
            return upvote

    def get_content(self):
        if hasattr(self, "content"):
            return self.content
        else:
            if self.soup == None:
                self.parser()
            soup = BeautifulSoup(self.soup.encode("utf-8"))
            answer = soup.find("div", class_="zm-editable-content clearfix")
            soup.body.extract()
            soup.head.insert_after(soup.new_tag("body", **{'class': 'zhi'}))
            soup.body.append(answer)
            img_list = soup.find_all("img", class_="content_image lazy")
            for img in img_list:
                img["src"] = img["data-actualsrc"]
            img_list = soup.find_all("img", class_="origin_image zh-lightbox-thumb lazy")
            for img in img_list:
                img["src"] = img["data-actualsrc"]
            noscript_list = soup.find_all("noscript")
            for noscript in noscript_list:
                noscript.extract()
            content = soup
            self.content = content
            return content

    def to_txt(self):

        content = self.get_content()
        body = content.find("body")
        br_list = body.find_all("br")
        for br in br_list:
            br.insert_after(content.new_string("\n"))
        li_list = body.find_all("li")
        for li in li_list:
            li.insert_before(content.new_string("\n"))

        if platform.system() == 'Windows':
            anon_user_id = "匿名用户".decode('utf-8').encode('gbk')
        else:
            anon_user_id = "匿名用户"
        if self.get_author().get_user_id() == anon_user_id:
            if not os.path.isdir(os.path.join(os.path.join(os.getcwd(), "text"))):
                os.makedirs(os.path.join(os.path.join(os.getcwd(), "text")))
            if platform.system() == 'Windows':
                file_name = self.get_question().get_title() + "--" + self.get_author().get_user_id() + "的回答.txt".decode(
                    'utf-8').encode('gbk')
            else:
                file_name = self.get_question().get_title() + "--" + self.get_author().get_user_id() + "的回答.txt"
            print file_name
            # if platform.system() == 'Windows':
            # file_name = file_name.decode('utf-8').encode('gbk')
            # print file_name
            # else:
            # print file_name
            if os.path.exists(os.path.join(os.path.join(os.getcwd(), "text"), file_name)):
                f = open(os.path.join(os.path.join(os.getcwd(), "text"), file_name), "a")
                f.write("\n\n")
            else:
                f = open(os.path.join(os.path.join(os.getcwd(), "text"), file_name), "a")
                f.write(self.get_question().get_title() + "\n\n")
        else:
            if not os.path.isdir(os.path.join(os.path.join(os.getcwd(), "text"))):
                os.makedirs(os.path.join(os.path.join(os.getcwd(), "text")))
            if platform.system() == 'Windows':
                file_name = self.get_question().get_title() + "--" + self.get_author().get_user_id() + "的回答.txt".decode(
                    'utf-8').encode('gbk')
            else:
                file_name = self.get_question().get_title() + "--" + self.get_author().get_user_id() + "的回答.txt"
            print file_name
            # if platform.system() == 'Windows':
            # file_name = file_name.decode('utf-8').encode('gbk')
            # print file_name
            # else:
            # print file_name
            f = open(os.path.join(os.path.join(os.getcwd(), "text"), file_name), "wt")
            f.write(self.get_question().get_title() + "\n\n")
        if platform.system() == 'Windows':
            f.write("作者: ".decode('utf-8').encode('gbk') + self.get_author().get_user_id() + "  赞同: ".decode(
                'utf-8').encode('gbk') + str(self.get_upvote()) + "\n\n")
            f.write(body.get_text().encode("gbk"))
            link_str = "原链接: ".decode('utf-8').encode('gbk')
            f.write("\n" + link_str + self.answer_url.decode('utf-8').encode('gbk'))
        else:
            f.write("作者: " + self.get_author().get_user_id() + "  赞同: " + str(self.get_upvote()) + "\n\n")
            f.write(body.get_text().encode("utf-8"))
            f.write("\n" + "原链接: " + self.answer_url)
        f.close()

    # def to_html(self):
    # content = self.get_content()
    # if self.get_author().get_user_id() == "匿名用户":
    # file_name = self.get_question().get_title() + "--" + self.get_author().get_user_id() + "的回答.html"
    # f = open(file_name, "wt")
    # print file_name
    # else:
    # file_name = self.get_question().get_title() + "--" + self.get_author().get_user_id() + "的回答.html"
    # f = open(file_name, "wt")
    # print file_name
    # f.write(str(content))
    # f.close()

    def to_md(self):
        content = self.get_content()
        if platform.system() == 'Windows':
            anon_user_id = "匿名用户".decode('utf-8').encode('gbk')
        else:
            anon_user_id = "匿名用户"
        if self.get_author().get_user_id() == anon_user_id:
            if platform.system() == 'Windows':
                file_name = self.get_question().get_title() + "--" + self.get_author().get_user_id() + "的回答.md".decode(
                    'utf-8').encode('gbk')
            else:
                file_name = self.get_question().get_title() + "--" + self.get_author().get_user_id() + "的回答.md"
            print file_name
            # if platform.system() == 'Windows':
            # file_name = file_name.decode('utf-8').encode('gbk')
            # print file_name
            # else:
            # print file_name
            if not os.path.isdir(os.path.join(os.path.join(os.getcwd(), "markdown"))):
                os.makedirs(os.path.join(os.path.join(os.getcwd(), "markdown")))
            if os.path.exists(os.path.join(os.path.join(os.getcwd(), "markdown"), file_name)):
                f = open(os.path.join(os.path.join(os.getcwd(), "markdown"), file_name), "a")
                f.write("\n")
            else:
                f = open(os.path.join(os.path.join(os.getcwd(), "markdown"), file_name), "a")
                f.write("# " + self.get_question().get_title() + "\n")
        else:
            if not os.path.isdir(os.path.join(os.path.join(os.getcwd(), "markdown"))):
                os.makedirs(os.path.join(os.path.join(os.getcwd(), "markdown")))
            if platform.system() == 'Windows':
                file_name = self.get_question().get_title() + "--" + self.get_author().get_user_id() + "的回答.md".decode(
                    'utf-8').encode('gbk')
            else:
                file_name = self.get_question().get_title() + "--" + self.get_author().get_user_id() + "的回答.md"
            print file_name
            # file_name = self.get_question().get_title() + "--" + self.get_author().get_user_id() + "的回答.md"
            # if platform.system() == 'Windows':
            # file_name = file_name.decode('utf-8').encode('gbk')
            # print file_name
            # else:
            # print file_name
            f = open(os.path.join(os.path.join(os.getcwd(), "markdown"), file_name), "wt")
            f.write("# " + self.get_question().get_title() + "\n")
        if platform.system() == 'Windows':
            f.write("## 作者: ".decode('utf-8').encode('gbk') + self.get_author().get_user_id() + "  赞同: ".decode(
                'utf-8').encode('gbk') + str(self.get_upvote()) + "\n")
        else:
            f.write("## 作者: " + self.get_author().get_user_id() + "  赞同: " + str(self.get_upvote()) + "\n")
        text = html2text.html2text(content.decode('utf-8')).encode("utf-8")

        r = re.findall(r'\*\*(.*?)\*\*', text)
        for i in r:
            if i != " ":
                text = text.replace(i, i.strip())

        r = re.findall(r'_(.*)_', text)
        for i in r:
            if i != " ":
                text = text.replace(i, i.strip())

        r = re.findall(r'!\[\]\((?:.*?)\)', text)
        for i in r:
            text = text.replace(i, i + "\n\n")

        if platform.system() == 'Windows':
            f.write(text.decode('utf-8').encode('gbk'))
            link_str = "#### 原链接: ".decode('utf-8').encode('gbk')
            f.write(link_str + self.answer_url.decode('utf-8').encode('gbk'))
        else:
            f.write(text)
            f.write("#### 原链接: " + self.answer_url)
        f.close()

    def get_visit_times(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        for tag_p in soup.find_all("p"):
            if "所属问题被浏览" in tag_p.contents[0].encode('utf-8'):
                return int(tag_p.contents[1].contents[0])

    def get_voters(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        data_aid = soup.find("div", class_="zm-item-answer ")["data-aid"]
        request_url = 'http://www.zhihu.com/node/AnswerFullVoteInfoV2'
        # if session == None:
        #     create_session()
        # s = session
        # r = s.get(request_url, params={"params": "{\"answer_id\":\"%d\"}" % int(data_aid)})
        r = requests.get(request_url, params={"params": "{\"answer_id\":\"%d\"}" % int(data_aid)})
        soup = BeautifulSoup(r.content)
        voters_info = soup.find_all("span")[1:-1]
        if len(voters_info) == 0:
            return
            yield
        else:
            for voter_info in voters_info:
                if voter_info.string == ( u"匿名用户、" or u"匿名用户"):
                    voter_url = None
                    yield User(voter_url)
                else:
                    voter_url = "http://www.zhihu.com" + str(voter_info.a["href"])
                    voter_id = voter_info.a["title"].encode("utf-8")
                    yield User(voter_url, voter_id)


class Collection:
    url = None
    # session = None
    soup = None

    def __init__(self, url, name=None, creator=None):

        if url[0:len(url) - 8] != "http://www.zhihu.com/collection/":
            raise ValueError("\"" + url + "\"" + " : it isn't a collection url.")
        else:
            self.url = url
            # print 'collection url',url
            if name != None:
                self.name = name
            if creator != None:
                self.creator = creator
    def parser(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content)
        self.soup = soup

    def get_name(self):
        if hasattr(self, 'name'):
            if platform.system() == 'Windows':
                return self.name.decode('utf-8').encode('gbk')
            else:
                return self.name
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            self.name = soup.find("h2", id="zh-fav-head-title").string.encode("utf-8").strip()
            if platform.system() == 'Windows':
                return self.name.decode('utf-8').encode('gbk')
            return self.name

    def get_creator(self):
        if hasattr(self, 'creator'):
            return self.creator
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            creator_id = soup.find("h2", class_="zm-list-content-title").a.string.encode("utf-8")
            creator_url = "http://www.zhihu.com" + soup.find("h2", class_="zm-list-content-title").a["href"]
            creator = User(creator_url, creator_id)
            self.creator = creator
            return creator

    def get_all_answers(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
	#print soup.prettify()  
        answer_list = soup.find_all("div", class_="zm-item")
        if len(answer_list) == 0:
            print "the collection is empty."
            return
            yield
        else:
            question_url = None
            question_title = None
            for answer in answer_list:
                if not answer.find("p", class_="note"):
                    question_link = answer.find("h2")
                    if question_link != None:
                        question_url = "http://www.zhihu.com" + question_link.a["href"]
                        question_title = question_link.a.string.encode("utf-8")
                    question = Question(question_url, question_title)
                    answer_url = "http://www.zhihu.com" + answer.find("span", class_="answer-date-link-wrap").a["href"]
                    author = None
                
                    if answer.find("h3", class_="zm-item-answer-author-wrap").string == u"匿名用户":
                        author_url = None
                        author = User(author_url)
                    else:
                        author_tag = answer.find("h3", class_="zm-item-answer-author-wrap").find_all("a")[0]
                        author_id = author_tag.string.encode("utf-8")
                        author_url = "http://www.zhihu.com" + author_tag["href"]
                        author = User(author_url, author_id)
                    yield Answer(answer_url, question, author)
            i = 2
            while True:
                r = requests.get(self.url + "?page=" + str(i))
                answer_soup = BeautifulSoup(r.content)
                answer_list = answer_soup.find_all("div", class_="zm-item")
                if len(answer_list) == 0:
                    break
                else:
                    for answer in answer_list:
                        if not answer.find("p", class_="note"):
                            question_link = answer.find("h2")
                            if question_link != None:
                                question_url = "http://www.zhihu.com" + question_link.a["href"]
                                question_title = question_link.a.string.encode("utf-8")
                            question = Question(question_url, question_title)
                            answer_url = "http://www.zhihu.com" + answer.find("span", class_="answer-date-link-wrap").a[
                                "href"]
                            author = None
                            if answer.find("h3", class_="zm-item-answer-author-wrap").string == u"匿名用户":
                                # author_id = "匿名用户"
                                author_url = None
                                author = User(author_url)
                            else:
                                author_tag = answer.find("h3", class_="zm-item-answer-author-wrap").find_all("a")[0]
                                author_id = author_tag.string.encode("utf-8")
                                author_url = "http://www.zhihu.com" + author_tag["href"]
                                author = User(author_url, author_id)
                            yield Answer(answer_url, question, author)
                i = i + 1

    def get_top_i_answers(self, n):
        j = 0
        answers = self.get_all_answers()
        for answer in answers:
            j = j + 1
            if j > n:
                break
            yield answer
