---
layout: post
title:  "GNU/Linux下使用Github搭建博客"
date:  2015-03-28
comments: true
tags: github jekyll blog
archive: false
---

<strong>历经无数艰辛，终于开启了个人博客之路，在此深深地感谢各位网络技术大神们各种各样的博客指引。此文适合那些想使用搭建个人博客的新手们，大神可以忽略。</strong>


<strong>一. Git Pages简介</strong>

Github是一个具有版本管理功能的代码仓库，许多重要的项目都托管在上面。每个项目都有一个主页，列出项目的源文件。为了让人们对项目迅速上手，Github就设计了Pages功能，可以为每个项目一个简明易懂的网页来说明该项目大概情况。同时也为每个Github用户提供了一个个人主页，该主页可以让人们对该用户有一个大概的了解。我们之所以能建立博客，就是利用了可以对这两种主页随意定制的特点。

建立博客有两种形式：
第一种是建立个人主页，可以使用username.github.io进行访问，每个用户名下面只能建立一个个人主页；
第二种是建立项目主页, 可以使用如下的链接访问username.github.io/projectname，每个项目都可以建立一个项目主页。


```
```

<strong>二. 注册Github帐户和建立博客仓库</strong>

首先需要注册一个Github帐户，如username，建立帐户之后需要按照网站要求对注册邮箱进行验证，不然在博客建立过程中会报错(报错信息会发送至注册邮箱)。

然后打开Github网站，使用用户名和密码进行登录，并建立一个形如username.github.io的仓库(本教程都是使用第一种方式建立个人博客)。


<strong>三. 上传博客源码到Github仓库</strong>

博主使用的系统是Ubuntu 12.04

1.建立目录并初始化为仓库

```
$ mkdir username.github.io
$ cd username.github.io
$ git init
```
该命令是在建立并初始化一个本地仓库，会在目录下新建一个.git的隐藏文件夹。


2.建立如下文件和文件夹

username.github.io  
|--\_includes：默认的在模板中可以引用的文件的位置  
|--\_layouts：默认的公共页面的位置  
|--\_posts：博客文章默认的存放位置    
|--.gitignore：这个文件夹中列出的文件或文件夹，不会纳入源码管理  
|--\_config.yml：关于jekyll模板引擎的配置文件  
`-- index.html：默认的主页  

编辑_config.yml:


```
baseurl: /username.github.io
encoding: utf-8
```

编辑_layouts/default.html:

```html
{% raw %}
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <title>{{ page.title }}</title>
</head>
<body>
    {{ content }}
</body>
</html>
{% endraw %}
```
编辑index.html:

```html
{% raw %}
---
layout: default
title: My blog
---
<h2>{{ page.title }}</h2>
<p>Recent articles</p>
<ul>
　　{% for post in site.posts %} 
        <li>{{ post.date | date_to_string }} 
            <a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a>
        </li>
　　{% endfor %}
</ul>
{% endraw %}
```

编辑_post/2015-03-28.test.html:

```html
{% raw %}
---
layout: default
title: test
---
<h2>{{ page.title }}</h2>
<p>My first article</p>
<p>{{ page.date | date_to_string }}</p>
{% endraw %}
```

3.传送到Github远程仓库

```
# 将当前的改动暂存在本地仓库
$ git add .
# 将暂存的改动提交到本地仓库，并写入本次提交的注释是”first post“
$ git commit -m "first post"
# 将远程仓库在本地添加一个引用origin
$ git remote add origin https://github.com/username/username.github.io.git
# 向origin推送master分支
$ git push origin master
```

注1：如果是初次安装git的话，在commit的时候会提示需要配置username和email，请读者注意根据提示配置一下，至于username和email可以随便填。

注2：在Git中，分支(branch)的概念非常重要，Git之所以强大，很大程度上就是因为它强大的分支体系。Github规定，在个人主页类型的仓库中，只有master分支中的页面才会生成网页文件；在项目主页类型的仓库中，只有gh-pages分支中的页面才会生成网页文件。
 
大约10分钟的时间，访问username.github.io就可以看到自己的博客了。无论生成失败还是成功，Github会向你的邮箱发送一封邮件说明原因，请注意查收。

