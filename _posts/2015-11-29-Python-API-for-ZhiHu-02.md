---
layout: post
title: Python爬虫遇上知乎(4)
description: 知乎的Python API，对用户进行抽象构建User类。
categories: Python
tags: Requests Termcolor

---

<p>
使用Python爬虫登录知乎，就可以轻松地进行一些监控、搜索、备份工作。慢慢地，你会发现Python真的很强大。<font color="blue"><strong>本文主要介绍在模拟登录知乎之后，如何用Python为知乎写一些API。主要是采用面向对象编程的思想，分别对Question、User、Answer、Collection进行抽象，接前面开始介绍User类。
</strong></font>
</p>


最后贴上源代码。以下代码原来出自: <br/>
<https://github.com/egrcc/zhihu-python> <br/>
我对代码进行修改，并加了详细的注释：<br/>
<https://github.com/liticer/zhihu_python> <br/>
应该比较容易阅读，如发现问题可以及时留言。
<p/>
<br/>

<strong>附: <a href="{{ site.BASE_PATH}}/assets/source/zhihu.py" download>zhihu.py</a> </strong>

<pre class="prettyPrint lang=python">
# 抽象一个用户类
class User:
    user_url = None
    soup = None

    # 初始化该用户的url、user_id
    def __init__(self, user_url, user_id=None):
        if user_url == None:
            self.user_id = "匿名用户"
        elif user_url[0:28] != "http://www.zhihu.com/people/":
            raise ValueError('"'+user_url+'": it isn\'t a user url.')
        else:
            self.user_url = user_url
            if user_id != None:
                self.user_id = user_id

    # 获取用户主页并解析
    def parser(self):
        r = requests.get(self.user_url)
        soup = BeautifulSoup(r.content)
        self.soup = soup

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

    # 获取用户名
    @encode_on_windows
    def get_user_id(self):
        if self.user_url == None:
            return "匿名用户"
        if hasattr(self, "user_id"):
            return self.user_id
        if self.soup == None:
            self.parser()
        user_l = self.soup.find("div", class_="title-section ellipsis")
        user_id = user_lb.find("span", class_="name").string.encode("utf-8")
        self.user_id = user_id
        return user_id

    # 获取关注该用户的人总数
    def get_followees_num(self):
        if self.user_url == None:
            return 0
        if self.soup == None:
            self.parser()
        followees_c = "zm-profile-side-following zg-clear"
        followees_l = self.soup.find("div", class_=followees_c)
        followees_num = int(followees_l.find("a").strong.string)
        return followees_num

    # 获取该用户关注的人总数
    def get_followers_num(self):
        if self.user_url == None:
            return 0
        if self.soup == None:
            self.parser()
        followers_c = "zm-profile-side-following zg-clear"
        followers_l = self.soup.find("div", class_=followers_c)
        followers_num = int(followers_l.find_all("a")[1].strong.string)
        return followers_num

    # 获取该用户获得赞数
    def get_agree_num(self):
        if self.user_url == None:
            return 0
        if self.soup == None:
            self.parser()
        agree_c = "zm-profile-header-user-agree"
        agree_l = self.soup.find("span", class_=agree_c)
        agree_num = int(agree_l.find("span",).strong.string)
        return agree_num

    # 获取该用户获得的感谢数
    def get_thanks_num(self):
        if self.user_url == None:
            return 0
        if self.soup == None:
            self.parser()
        thanks_c = "zm-profile-header-user-thanks"
        thanks_l = self.soup.find("span", class_= thanks_c)
        thanks_num = int(thanks_l.strong.string)
        return thanks_num

    # 获取该用户提问的问题数
    def get_asks_num(self):
        if self.user_url == None:
            return 0
        if self.soup == None:
            self.parser()
        asks_l = self.soup.find_all("span", class_="num")
        asks_num = int(asks_l[0].string)
        return asks_num

    # 获取该用户回答的问题数
    def get_answers_num(self):
        if self.user_url == None:
            return 0
        if self.soup == None:
            self.parser()
        answers_l = self.soup.find_all("span", class_="num")
        answers_num = int(answers_l[1].string)
        return answers_num

    # 获取该用户收藏夹数
    def get_collections_num(self):
        if self.user_url == None:
            return 0
        if self.soup == None:
            self.parser()
        collections_l = self.soup.find_all("span", class_="num")
        collections_num = int(collections_l[3].string)
        return collections_num

    # 获取关注该用户的人
    def get_followees(self):
        if self.user_url == None:
            return
        followees_num = self.get_followees_num()
        if followees_num == 0:
            return
        # 获取关注该用户的用户页页面并解析
        followee_url = self.user_url + "/followees"
        r = requests.get(followee_url)
        soup = BeautifulSoup(r.content)
        # 对于每20个用户发送一次请求
        # 首次不用发送请求，因为已经获取到页面了
        user_url_list = soup.find_all("h2", class_="zm-list-content-title")
        for j in xrange(min(followees_num, 20)):
            user_url = user_url_list[j].a["href"],
            user_id = user_url_list[j].a.string.encode("utf-8")
            yield User(user_url, user_id)
        # 处理剩下的关注该用户的人
        for i in xrange((followees_num - 21) / 20 + 1):
            # 发送post请求，再获取20个关注者
            i += 1
            # 将要发送post请求的URL
            post_url = "http://www.zhihu.com/node/ProfileFolloweesListV2"
            # 准备发送该post请求的参数
            _xsrf = soup.find("input", attrs={'name': '_xsrf'})["value"]
            offset = i * 20
            hash_id = re.findall('hash_id&quot;: &quot;(.*)&quot;},', r.text)[0]
            dumps_p = {
                "offset": offset, 
                "order_by": "created", 
                "hash_id": hash_id
            }
            params = json.dumps(dumps_p)
            data = {
                '_xsrf': _xsrf,
                'method': "next",
                'params': params
            }
            # 准备发送该post请求的消息头
            header = {
                'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0)"\
                              + " Gecko/20100101 Firefox/34.0",
                'Host': "www.zhihu.com",
                'Referer': followee_url
            }
            # 发送post请求
            r_post = requests.post(post_url, data=data, headers=header)
            # 获取关注者列表
            followee_list = r_post.json()["msg"]
            for j in xrange(min(followees_num - i * 20, 20)):
                soup_f = BeautifulSoup(followee_list[j])
                user_l = soup_f.find("h2", class_="zm-list-content-title").a
                yield User(user_l["href"], user_l.string.encode("utf-8"))

    # 获取该用户关注的用户列表
    def get_followers(self):
        if self.user_url == None:
            return
        followers_num = self.get_followers_num()
        if followers_num == 0:
            return
        # 获取关注者页面并解析
        follower_url = self.user_url + "/followers"
        r = requests.get(follower_url)
        soup = BeautifulSoup(r.content)
        # 首次不用再get，因为前面已经获取过了
        user_ul = soup.find_all("h2", class_="zm-list-content-title")
        for j in xrange(min(followers_num, 20)):
            user_url = user_ul[j].a["href"]
            user_id  = user_ul[j].a.string.encode("utf-8")
            yield User(user_url, user_id)
        for i in xrange((followers_num - 21) / 20 + 1):
            # 发送post请求，再获取20个关注者
            i += 1
            # 发送post请求的地址
            post_url = "http://www.zhihu.com/node/ProfileFollowersListV2"
            # 发送post请求的参数
            _xsrf = soup.find("input", attrs={'name': '_xsrf'})["value"]
            offset = i * 20
            hash_id = re.findall('hash_id&quot;: &quot;(.*)&quot;},', r.text)[0]
            dumps_p = {
                "offset": offset, 
                "order_by": "created", 
                "hash_id": hash_id
            }
            params = json.dumps(dumps_p)
            data = {
                '_xsrf': _xsrf,
                'method': "next",
                'params': params
            }
            # 发送post请求的消息头
            header = {
                'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0)"\
                              + "Gecko/20100101 Firefox/34.0",
                'Host': "www.zhihu.com",
                'Referer': follower_url
            }
            # 发送post请求
            r_post = requests.post(post_url, data=data, headers=header)
            # 解析请求的结果，得到关注者列表
            follower_list = r_post.json()["msg"]
            for j in xrange(min(followers_num - i * 20, 20)):
                soup_f = BeautifulSoup(follower_list[j])
                user_l = soup_f.find("h2", class_="zm-list-content-title").a
                yield User(user_l["href"], user_l.string.encode("utf-8"))

    # 获取该用户提问的问题
    def get_asks(self):
        if self.user_url == None:
            return
        asks_num = self.get_asks_num()
        if asks_num == 0:
            return
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
            return
        answers_num = self.get_answers_num()
        if answers_num == 0:
            return
        for i in xrange((answers_num - 1) / 20 + 1):
            # 每20个答案发送一次get请求，获得结果并解析
            answer_url = self.user_url + "/answers?page=" + str(i + 1)
            r = requests.get(answer_url)
            soup = BeautifulSoup(r.content)
            for answer in soup.find_all("a", class_="question_link"):
                question_url = "http://www.zhihu.com" + answer["href"][0:18]
                question_title = answer.string.encode("utf-8")
                question = Question(question_url, question_title)
                answer_url = "http://www.zhihu.com" + answer["href"]
                yield Answer(answer_url, question, self)

    # 获取该用户的收藏夹
    def get_collections(self):
        if self.user_url == None:
            return
        collections_num = self.get_collections_num()
        if collections_num == 0:
            return
        for i in xrange((collections_num - 1) / 20 + 1):
            # 每20个收藏夹发送一次post请求，获取结果并解析
            collection_url = self.user_url + "/collections?page=" + str(i + 1)
            r = requests.get(collection_url)
            soup = BeautifulSoup(r.content)
            collection_c = "zm-profile-section-item zg-clear"
            collection_l = soup.find_all("div", class_=collection_c)
            for collection in collection_l:
                label = collection.find("a", class_="zm-profile-fav-item-title")
                url = "http://www.zhihu.com" + label["href"]
                name = label.string.encode("utf-8")
                yield Collection(url, name, self)
</pre>

