---
layout: post
title: Python爬虫遇上知乎(五)
description: 知乎的Python API，对答案进行抽象构建Answer类。
categories: Python
tags: Requests Termcolor

---

<p>
使用Python爬虫登录知乎，就可以轻松地进行一些监控、搜索、备份工作。慢慢地，你会发现Python真的很强大。
<font color="blue"><strong>
本文主要介绍在模拟登录知乎之后，如何用Python为知乎写一些API。主要是采用面向对象编程的思想，分别对Question、User、Answer、Collection
进行抽象，接前面开始介绍Answer类。
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
</pre>

