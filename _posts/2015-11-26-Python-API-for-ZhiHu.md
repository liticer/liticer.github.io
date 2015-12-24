---
layout: post
title: Python爬虫遇上知乎(二)
description: 检查是否登录，为后续API的正常运行提供基础。
categories: Python
tags: BS4 Requests

---

<p>
使用Python爬虫登录知乎，就可以轻松地进行一些监控、搜索、备份工作。慢慢地，你会发现Python真的很强大。<font color="blue"><strong>本文主要介绍在模拟登录知乎之后，如何用Python为知乎写一些API。主要是采用面向对象编程的思想，分别对Question、User、Answer、Collection进行抽象，在写API之前首先得检查是否已经成功登陆。
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

<pre class="prettyPrint">
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
</pre>

