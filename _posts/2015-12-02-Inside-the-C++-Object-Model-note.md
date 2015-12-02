---
layout: post
title: 深度探索C++对象模型学习笔记
description: 阅读侯捷老师翻译的Lippman大作《Inside the C++ Object Mode》过程中，在自己理解和体会的基础上做了一些笔记。
categories: Python
tags: Requests Termcolor

---

**第1章 关于对象**

1.&ensp;C++对象的布局成本<br/>

   * C++中单纯地使用封装和继承，并不会增加存取时间和存储空间上的成本。
   * C++真正需要的额外成本是由Virtual引起的(包括Virtual function和Virtual base class)。

2.&ensp;C++对象模型<br/>

  * 数据成员：Nonstatic data members被配置于每一个class object之内；Static data members 被存放在个别的class object之外。
  * 非虚函数成员：Nostatic/Static function members均被置于个别的class object 之外，同一般的非成员函数处理机制类似。
  * 虚函数成员：
    * 每一个class产生出一堆指向virtual functions的指针，存放在一个叫做virtual table(vtbl)的表格之中。通常一个class所关联的type_info object被存放在该表格的第一个slot中。
    * 每一个class object被安插一个叫做virtual pointer(vptr)的指针，指向相关的virtual table。通常vptr会被每一个class的constructor、destructor和copy assignment等函数自动地进行设定和重置。

3.&ensp;C++对象模型<br/>

<br/>

**第2章 构造函数语意学**

1.&ensp;Default Constructor的构造操作<br/>

&ensp;&ensp;对于一个类，如果没有任何user-declared constructor，那么在编译器有需要的时候，会为它合成一个nontrival default constructor。通常，有如下4种情况需要合成constructor:

  * 该class有"带Default Constructor"的Data member
    * 需要在构造函数中调用该Data member的默认构造函数初始化该成员。
  * 该class有"带Default Constructor"的Base class
    * 需要在构造函数中调用Base class的默认构造函数初始化Base class subobject。
  * 该class有"Virtual Function"
    * 需要在构造函数中生成或维护vtbl，并设置或修改vptr。
  * 该class有"Virtual base class"
    * 需要在构造函数中维护vtbl和vptr，保证virtual base class在每一个derived class object中的位置在执行期准备妥当。

&ensp;&ensp;至于没有存在上述4种情况且没有声明任何constructor的class，我们说它拥有的是implicit trivial default constructor，它们实际上不会被合成出来。

&ensp;&ensp;C++新手一般有两个常见的误解：

  * 任何class，如果没有定义default constructor，就会被合成出来一个。
  * 编译器默认合成出来的default constructor会显式地设定"class内每一个data member的默认值"。


2.&ensp;Copy Constructor的构造操作<br/>

&ensp;&ensp;调用Copy constructor三种情况分别是：初始化、传参和返回值。和default construtor一样，copy constructor也分为trivial和nontrivial两种，只有nontrivial的class才会合成它。倘若一个class展现出所谓的"bitwise copy semantics"，那么它的copy constructor就是trivival的。一个class不展现出"bitwise copy semantics"的4种情况如下：<br/>

  * 当class内含有一个member object，而后者的class声明有一个copy constructor时(不论是被class设计者显式声明，还是被编译器合成都算)，该class的copy constructor需要调用该member object的copy constructor完成该成员的拷贝构造。
  * 当class继承自一个base class，而后者存在一个显式声明的copy constructor时，该class的copy constructor需要调用base class的copy constructor完成base class subobject的拷贝构造。
  * 当class声明了一个或多个virtual functions时，该class的copy constructor需要维护vptr指针，保证其指向对应的class的vtbl。
  * 当class派生于一个继承串链，其中有一个或多个virtual base classes时，该class的copy constructor需要拷贝构造virtual base subobject，同时维护vptr指针确保其指向对应的class的vtbl。




















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

<strong>附: <a href="{{ site.BASE_PATH}}/assets/source/zhihu.py" download>zhihu.py</a> </strong>

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

