# -*- coding: utf-8 -*-
'''

                                                                                         ;$$;       
                                                                                    #############   
                                                                               #############;#####o 
                                                      ##                 o######################### 
                                                      #####         $###############################
                                                      ##  ###$ ######!    ##########################
                           ##                        ###    $###          ################### ######
                           ###                      ###                   ##o#######################
                          ######                  ;###                    #### #####################
                          ##  ###             ######                       ######&&################ 
                          ##    ###      ######                            ## ############ #######  
                         o##      ########                                  ## ##################   
                         ##o                ###                             #### #######o#######    
                         ##               ######                             ###########&#####      
                         ##                ####                               #############!        
                        ###                                                     #########           
               #####&   ##                                                      o####               
             ######     ##                                                   ####*                  
                  ##   !##                                               #####                      
                   ##  ##*                                            ####; ##                      
                    #####                                          #####o   #####                   
                     ####                                        ### ###   $###o                    
                      ###                                            ## ####! $###                  
                      ##                                            #####                           
                      ##                                            ##                              
                     ;##                                           ###                           ;  
                     ##$                                           ##                               
                #######                                            ##                               
            #####   &##                                            ##                               
          ###       ###                                           ###                               
         ###      ###                                             ##                                
         ##     ;##                                               ##                                
         ##    ###                                                ##                                
          ### ###                                                 ##                                
            ####                                                  ##                                
             ###                                                  ##                                
             ##;                                                  ##                                
             ##$                                                 ##&                                
              ##                                                 ##                                 
              ##;                                               ##                                  
               ##                                              ##;                                  
                ###                                          ###         ##$                        
                  ###                                      ###           ##                         
   ######################                              #####&&&&&&&&&&&&###                         
 ###        $#####$     ############&$o$&################################                           
 #                               $&########&o                                                       
'''

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
            hash_id = re.findall("hash_id&quot;: &quot;(.*)&quot;},", r.text)[0]
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
            hash_id = re.findall("hash_id&quot;: &quot;(.*)&quot;},", r.text)[0]
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



# 抽象一个答案类
class Answer:
    answer_url = None
    soup = None

    # 初始化该答案的url、question、author、upvote、content
    def __init__(self, answer_url, question=None,\
                 author=None, upvote=None, content=None):
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
        if self.soup == None:
            self.parser()
        soup = self.soup
        question_c = "zm-item-title zm-editable-content"
        question_l = soup.find("h2", class_= question_c).a
        url = "http://www.zhihu.com" + question_l["href"]
        title = question_l.string.encode("utf-8")
        question = Question(url, title)
        return question

    # 获取答案的作者
    def get_author(self):
        if hasattr(self, "author"):
            return self.author
        if self.soup == None:
            self.parser()
        soup = self.soup
        author_c = "zm-item-answer-author-wrap"
        author_l = soup.find("h3", class_=author_c)
        if author_l.string == u"匿名用户":
            author_url = None
            author = User(author_url)
        else:
            author_tag = author_l.find_all("a")[1]
            author_id = author_tag.string.encode("utf-8")
            author_url = "http://www.zhihu.com" + author_tag["href"]
            author = User(author_url, author_id)
        return author

    # 获取该答案所获得的赞数
    def get_upvote(self):
        if hasattr(self, "upvote"):
            return self.upvote
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

    # 获取该答案的内容
    def get_content(self):
        if hasattr(self, "content"):
            return self.content
        if self.soup == None:
            self.parser()
        soup = BeautifulSoup(self.soup.encode("utf-8"))
        # 为Answer查找并构建一个新的html
        answer = soup.find("div", class_="zm-editable-content clearfix")
        soup.body.extract()
        soup.head.insert_after(soup.new_tag("body", **{'class': 'zhi'}))
        soup.body.append(answer)
        # 改变其中image的src属性，并去掉一些不执行的代码
        img_list = soup.find_all("img", class_="content_image lazy")
        for img in img_list:
            img["src"] = img["data-actualsrc"]
        img_c    = "origin_image zh-lightbox-thumb lazy"
        img_list = soup.find_all("img", class_=img_list)
        for img in img_list:
            img["src"] = img["data-actualsrc"]
        noscript_list = soup.find_all("noscript")
        for noscript in noscript_list:
            noscript.extract()
        content = soup
        self.content = content
        return content

    # 将答案保存成TXT格式
    def to_txt(self):
        content = self.get_content()
        body = content.find("body")
        # 分别在br和li后面插入换行符
        br_list = body.find_all("br")
        for br in br_list:
            br.insert_after(content.new_string("\n"))
        li_list = body.find_all("li")
        for li in li_list:
            li.insert_before(content.new_string("\n"))
        # 获取答案被保存的路径和文件名
        file_path = os.path.join(os.path.join(os.getcwd(), "text"))
        file_name = self.get_question().get_title() + "--"\
                        + self.get_author().get_user_id() + "的回答.txt"
        # 创建路径，处理文件名编码
        if not os.path.isdir(file_path):
            os.makedirs(file_path)
        if platform.system() == 'Windows':
            file_name = file_name.decode('utf-8').encode('gbk')
        print file_name
        # 先处理匿名用户的情况
        if self.get_author().user_url == None:
            if os.path.exists(os.path.join(file_path, file_name)):
                f = open(os.path.join(file_path, file_name), "a")
                f.write("\n\n")
            else:
                f = open(os.path.join(file_path, file_name), "a")
                f.write(self.get_question().get_title() + "\n\n")
        # 处理非匿名用户的情况
        else:
            f = open(os.path.join(file_path, file_name), "wt")
            f.write(self.get_question().get_title() + "\n\n")
        # 按照平台不同，使用不同编码格式开始写文件
        file_header = "作者: " + self.get_author().get_user_id()\
                      + " 赞同: " + str(self.get_upvote()) + "\n\n"
        file_ender  = "\n" + "原链接: " + self.answer_url
        if platform.system() == 'Windows':
            f.write(file_header.decode('utf-8').encode('gbk'))
            f.write(body.get_text().encode("gbk"))
            f.write(file_ender.decode('utf-8').encode('gbk'))
        else:
            f.write(file_header)
            f.write(body.get_text().encode("utf-8"))
            f.write(file_ender)
        f.close()

    # 将该答案保存成md格式
    def to_md(self):
        content = self.get_content()
        # 获取答案被保存的路径和文件名
        file_path = os.path.join(os.path.join(os.getcwd(), "markdown"))
        file_name = self.get_question().get_title() + "--"\
                        + self.get_author().get_user_id() + "的回答.md"
        # 创建路径，处理文件名编码
        if not os.path.isdir(file_path):
            os.makedirs(file_path)
        if platform.system() == 'Windows':
            file_name = file_name.decode('utf-8').encode('gbk')
        print file_name
        # 先处理匿名用户的情况
        if self.get_author().user_url == None:
            if os.path.exists(os.path.join(file_path, file_name)):
                f = open(os.path.join(file_path, file_name), "a")
                f.write("\n")
            else:
                f = open(os.path.join(file_path, file_name), "a")
                f.write("# " + self.get_question().get_title() + "\n")
        # 再处理非匿名用户的情况
        else:
            f = open(os.path.join(file_path, file_name), "wt")
            f.write("# " + self.get_question().get_title() + "\n")
        # 对Anwser的html文件内容进行处理
        text = html2text.html2text(content.decode('utf-8')).encode("utf-8")
        # 处理步骤1
        r = re.findall(r'\*\*(.*?)\*\*', text)
        for i in r:
            if i != " ":
                text = text.replace(i, i.strip())
        # 处理步骤2
        r = re.findall(r'_(.*)_', text)
        for i in r:
            if i != " ":
                text = text.replace(i, i.strip())
        # 处理步骤3
        r = re.findall(r'!\[\]\((?:.*?)\)', text)
        for i in r:
            text = text.replace(i, i + "\n\n")
        # 按照平台不同，使用不同编码格式开始写文件
        file_header = "## 作者: " + self.get_author().get_user_id()\
                      + "  赞同: " + str(self.get_upvote()) + "\n"
        file_ender  = "#### 原链接： " + self.answer_url
        if platform.system() == 'Windows':
            f.write(file_header.decode('utf-8').encode('gbk'))
            f.write(text.decode('utf-8').encode('gbk'))
            f.write(file_ender.decode('utf-8').encode('gbk'))
        else:
            f.write(file_header)
            f.write(text)
            f.write(file_ender)
        f.close()

    # 获取该答案被访问的次数
    def get_visit_times(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        for tag_p in soup.find_all("p"):
            if "所属问题被浏览" in tag_p.contents[0].encode('utf-8'):
                return int(tag_p.contents[1].contents[0])

    # 获取该答案的支持者
    def get_voters(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        data_aid = soup.find("div", class_="zm-item-answer ")["data-aid"]
        request_url = 'http://www.zhihu.com/node/AnswerFullVoteInfoV2'
        params={"params": "{\"answer_id\":\"%d\"}" % int(data_aid)}
        r = requests.get(request_url, params=params) 
        soup = BeautifulSoup(r.content)
        voters_info = soup.find_all("span")[1:-1]
        if len(voters_info) == 0:
            return
        for voter_info in voters_info:
            if voter_info.string == ( u"匿名用户、" or u"匿名用户"):
                voter_url = None
                yield User(voter_url)
            else:
                voter_url = "http://www.zhihu.com" + str(voter_info.a["href"])
                voter_id = voter_info.a["title"].encode("utf-8")
                yield User(voter_url, voter_id)



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
                question_link = answer.find("h2")
                if question_link != None:
                    question_url = "http://www.zhihu.com" + question_link.a["href"]
                    question_title = question_link.a.string.encode("utf-8")
                question = Question(question_url, question_title)
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
