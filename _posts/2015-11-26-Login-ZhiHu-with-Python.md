---
layout: post
title: Python爬虫采集知乎信息
description: 使用简单的Python脚本登录知乎，轻松地进行一些监控、搜索、备份工作。
categories: Python
tags: Requests Termcolor BS4

---


<p style="font-weight:700;font-size:20px;color:Magenta;text-align:center;padding:20px 0">第1章  登录知乎</p>

<p>
使用Python爬虫登录知乎，就可以轻松地进行一些监控、搜索、备份工作。<font color="blue"><strong>本文首先介绍如何使用Python登录知乎，然后还会介绍一些Python写的API。
</strong></font>
</p>


<p>
要想使用Python爬虫去做一些自动化的管理工作，首先需要写一段脚本模拟登录过程。就像你要上知乎之前需要登录一样，这部分工作当然得由脚本自己完成。其实，Python模拟登录知乎的代码可以在100行之内，甚至50行之内完成。不过要是考虑到出错处理、交互友好、代码可读性等因素，可能代码量要稍微大些。
</p>


<p>
<font color="#B22222"><strong>
登录过程主要可以分为三步：<br/>
1. 获取将要post的表单中的参数：如用户名、密码、验证码等。<br/>
2. 根据参数构造表单，发送post请求上传表单。<br/>
3. 解析表单返回结果，保存Cookies，这样就不用每次访问都登录了。<br/>
</strong></font>
</p>
要理解登录过程可能需要一点Web基础，不过幸运的是这些知识都比较简单。打开Firefox，按下F12，一边登录，一边去看，很快就明白了。



<p style="font-weight:700;font-size:20px;color:Magenta;text-align:center;padding:20px 0">第2章  爬取信息</p>

<p>
在使用API爬取信息之前，首先要检查是否已经成功登陆。<font color="blue"><strong>在成功登录的基础上，采用面向对象编程的思想，分别对Question、User、Answer、Collection进行抽象。
</strong></font>
</p>



最后附上源代码链接。以下代码原来出自: <br/>
<https://github.com/egrcc/zhihu-python> <br/>
我对代码进行修改，并加了详细的注释：<br/>
<https://github.com/liticer/zhihu_python> <br/>
应该比较容易阅读，如发现问题可以及时留言。
<p/>
<br/>

<strong>附: <a href="{{ site.BASE_PATH}}/assets/source/auth.py" download>auth.py</a> </strong><br/>
<strong>&ensp;&ensp;&ensp;&ensp;<a href="{{ site.BASE_PATH}}/assets/source/zhihu.py" download>zhihu.py</a> </strong>
