---
layout: post
title:  "GNU/Linux下使用Jekyll搭建博客"
date:  2015-03-28
comments: true
tags: github jekyll blog
archive: false
---

前言：历经无数艰辛，终于开启了个人博客之路，在此深深地感谢各位网络技术大神们各种各样的博客指引。此文适合那些想使用搭建个人博客的新手们，大神可以忽略。


一. Git Pages简介

Github是一个具有版本管理功能的代码仓库，许多重要的项目都托管在上面。每个项目都有一个主页，列出项目的源文件。为了让人们对项目迅速上手，Github就设计了Pages功能，可以为每个项目一个简明易懂的网页来说明该项目大概情况。同时也为每个Github用户提供了一个个人主页，该主页可以让人们对该用户有一个大概的了解。我们之所以能建立博客，就是利用了可以对这两种主页随意定制的特点。

建立博客有两种形式：
第一种是建立个人主页，可以使用username.github.io进行访问，每个用户名下面只能建立一个个人主页；
第二种是建立项目主页, 可以使用如下的链接访问username.github.io/projectname，每个项目都可以建立一个项目主页。


```
```

二. 注册Github帐户和建立博客仓库

首先需要注册一个Github帐户，如username，建立帐户之后需要按照网站要求对注册邮箱进行验证，不然在博客建立过程中会报错(报错信息会发送至注册邮箱)。

然后打开Github网站，使用用户名和密码进行登录，并建立一个形如username.github.io的仓库(本教程都是使用第一种方式建立个人博客)。


三. 上传博客源码到Github仓库

博主使用的系统是Ubuntu 12.04，后续所有操作均在bash命令行中完成。

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

四. 搭建jekyll本地调试环境

在编写完博客之后，可以不经调试直接上传至Github。但是其中可能存在错误，发现错误之后再修改，修改之后再上传，这个过程不但耗时而且麻烦。如果想在本地进行调试，就需要搭建jekyll环境了，下面来介绍环境搭建过程。

1.安装gem

```
$ sudo apt-get install rubygems
$ gem sources --remove https://rubygems.org/
$ gem sources --remove http://rubygems.org/
$ gem sources -a https://ruby.taobao.org/
$ gem sources -l
\*** CURRENT SOURCES ***

https://ruby.taobao.org
# 请确保只有ruby.taobao.org
```   
Rubygems是一个复杂的ruby安装包管理软件，具体请man gem。

2.安装rvm和ruby

```
$ sudo apt-get install curl
$ curl -L https://get.rvm.io | sudo bash -s stable  
$ /bin/bash --login
$ sudo rvm install ruby-2.1.2
$ rvm use ruby-2.1.2
```
注1：Ubuntu 12.04源里的ruby版本太低，jekyll要求的ruby版本必须大于1.9.2。  
注2：如果出现错误：  
&ensp;&ensp;&ensp;&ensp;&ensp;`curl: (77) error setting certificate verify locations:`  
&ensp;&ensp;&ensp;&ensp;&ensp;解决方法如下：  
&ensp;&ensp;&ensp;&ensp;&ensp;`$ sudo apt-get install ca-certificates`  
&ensp;&ensp;&ensp;&ensp;&ensp;`$ sudo mkdir -p /etc/pki/tls/certs`  
&ensp;&ensp;&ensp;&ensp;&ensp;`$ sudo cp /etc/ssl/certs/ca-certificates.crt /etc/pki/tls/certs/`  

3.安装nodejs和execjs

```
$ sudo apt-get install nodejs
$ sudo gem install execjs
```

4.安装jekyll

```
sudo gem install jekyll -V
```

注：等待时间较长，-V可以显示安装过程。

五. 本地jekyll调试和模板使用

1.本地jekyll调试

```
$ cd username.github.io
$ /bin/bash --login
$ rvm use ruby-2.1.2
$ jekyll serve --watch
```

注：运行完上述命令后，打开127.0.0.1:4000就能在本地看到博客调试的结果。

2.使用jekyll模板

如果你想迅速开始写博客，而不去纠结在一些简单的界面设置中，就可以直接使用<a href="http://jekyllthemes.org" target="_blank">jekyll提供的模板</a>。
模板使用的方式(以jekyll-clean模板为例)如下:

```
$ git clone https://github.com/scotte/jekyll-clean.git
$ rm -rf jekyll-clean/.git
$ cp -r jekyll-clean username.git.io
```
之后就是以别人模板中的文件建立仓库、调试、上传了。最后只需要学习一些简单的Markdown语法，Html基础就可以自己写博客了。每次只需要在_post目录当中编写html或者markdown格式的博客，然后再推送到Github就可以发表自己的博客了。

后记：个人博客最大的好处就是随心所欲，文字、图片、表格、公式，你想要它显示什么样，就可以什么样，一切都在自己不断地挖掘。另外，还有强大的Github给你的博客做后端，不能再放心了。
