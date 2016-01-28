---
layout: post
title: Makefile学习笔记
description: 在编写Makefile文件的过程中，做的一些笔记。
categories: Tools
tags: Git

---

<link rel="stylesheet" type="text/css" href="/assets//css/style.css">


&ensp;&ensp;&ensp;&ensp;本篇文章是自己在学习Makefile时的笔记，旨在写出一篇简明扼要Makefile教程。要学的东西太多了，今天学，明天忘，也不是是个事。希望在以后都记不起来的时候，看一眼文章就能快速想起这些东西。
<p/>

<p class="my_header1">第1章  Makefile基础</p>


<strong>一、简要介绍</strong>

&ensp;&ensp;&ensp;&ensp;<code>C/C++</code>源文件，首先会被编译生成中间目标文件，再由中间目标文件链接生成执行文件。在编译时，编译器只检测程序语法，和函数/变量是否被声明；如果函数未被声明，编译器会给出一个警告，但可以生成<code>Object File</code>；在链接时，链接器会在所有的<code>Object File</code>中找寻函数的实现，如果找不到，那到就会报链接错误码，指出链接器未能找到函数的实现。

<strong>二、典型示例</strong>

&ensp;&ensp;&ensp;&ensp;在这个示例中，工程有8个C文件和3个H文件，我们要写一个<code>Makefile</code>来告诉<code>make</code>命令如何编译和链接这几个文件。规则如下：<br/>

* 如果这个工程没有编译过，那么所有的C文件都要编译并被链接。
* 如果这个工程的某几个C文件被修改，那么只编译被修改的C文件，并链接目标工程。
* 如果这个工程的头文件被改变了，那么只编译引用了这几个头文件的C文件，并链接目标程序。

按照上述规则，编写<code>Makefile</code>文件如下：

<pre class="prettyPrint lang=bash">
# 使用变量
OBJS = main.o kbd.o command.o display.o insert.o search.o files.o utils.o
# 第一个target为最终目标文件
edit : $(OBJS)
	cc -o edit $(OBJS)
# 分别指定各个目标的生成规则
main.o : main.c defs.h
	cc -c main.c	
kbd.o : kbd.c defs.h command.h
	cc -c kbd.c
command.o : command.c defs.h command.h
	cc -c command.c	
display.o : display.c defs.h buffer.h
	cc -c display.c
insert.o : insert.c defs.h buffer.h
	cc -c insert.c
search.o : search.c defs.h buffer.h
	cc -c search.c
files.o : files.c defs.h buffer.h command.h
	cc -c files.c
utils.o : utils.c defs.h
	cc -c utils.c
# 表示clean是个伪目标	
.PHONY : clean	
clean :
	rm edit $(OBJS)
</pre>


在默认的方式下，也就是我们只输入<code>make</code>命令，执行流程如下：

* 首先<code>make</code>会在当前目录下找名字叫<code>Makefile</code>或<code>makefile</code>的文件。<br/>
* 如果找到，它会找文件中的第一个<code>target</code>，并把这个文件作为最终的目标文件。<br/>
* 如果最终目标文件不存在，或其所依赖的<code>.o</code>文件修改时间比它更新，就会执行后面所定义的命令来生成这个文件。<br/>
* 如果最终目标文件所依赖的<code>.o</code>文件也不存在，或者<code>.o</code>文件比其依赖文件修改时间更早，就会根据其对应规则先生成<code>.o</code>文件。<br/>
* 重复上述的递推过程，直到遇到源代码文件，再按照逆序一步步地生成最终目标文件。<br/>

<strong>三、基本规则</strong>

1.&ensp;<code>Makefile</code>文件构成

* 显式规则。说明了如何生成一个或多的的目标文件。这是由<code>Makefile</code>的书写者明显指出，要生成的文件，文件的依赖文件，生成的命令。在<code>Makefile</code>中的命令，必须要以</code>[Tab]</code>键开始。
* 隐晦规则。可以让我们比较粗糙地简略地书写<code>Makefile</code>，这是由<code>make</code>所支持的。<br/>
* 变量定义。变量一般都是字符串，有点你C语言中的宏，当<code>Makefile</code>被执行时，其中的变量都会被扩展到相应的引用位置上。<br/>
* 文件指示。包括了三个部分：一个是在一个<code>Makefile</code>中引用另一个<code>Makefile</code>，就像<code>C</code>语言中的<code>include</code>一样；另一个是指根据某些情况指定<code>Makefile</code>中的有效部分，就像<code>C</code>语言中的预编译<code>#if</code>一样；还有就是定义一个多行的命令。<br/>
* 注释。只有行注释，和<code>UNIX</code>的<code>Shell</code>脚本一样，其注释是用<code>"#"</code>字符。<br/>


2.&ensp;<code>Makefile</code>注意事项

* 大多数的<code>make</code>都支持<code>makefile</code>和<code>Makefile</code>这两种默认文件名。如果要指定特定的<code>Makefile</code>，你可以使用<code>make</code>的<code>-f</code>和<code>--file</code>参数，如<code>make -f Make.Linux</code>。
* 在<code>Makefile</code>使用<code>include</code>关键字可以把别的<code>Makefile</code>包含进来，这很像<code>C</code>语言的<code>#include</code>，被包含的文件会原模原样的放在当前文件的包含位置。<code>make</code>命令开始时，如果文件都没有指定绝对路径或是相对路径的话，<code>make</code>会在当前目录下首先寻找，如果当前目录下没有找到，那么，<code>make</code>还会在下面的几个目录下找：(1)如果<code>make</code>执行时，有<code>-I</code>或<code>--include-dir</code>参数，那么<code>make</code>就会在这个参数所指定的目录下去寻找；(2)如果目录<code>[prefix]/include</code>（一般是：<code>/usr/local/bin</code>或<code>/usr/include</code>）存在的话，<code>make</code>也会去找。<br/>
* <code>GNU</code>的<code>make</code>工作时的执行步骤入下：
(1)读入所有的<code>Makefile</code>；(2)读入被<code>include</code>的其它<code>Makefile</code>；(3)初始化文件中的变量；(4)推导隐晦规则，并分析所有规则；(5)为所有的目标文件创建依赖关系链；(6)根据依赖关系，决定哪些目标要重新生成；(7)执行生成命令。


<strong>四、书写规则</strong>

1.&ensp;语法规则

&ensp;&ensp;&ensp;&ensp;包含两个部分，一个是依赖关系，一个是生成目标的方法:

<pre class="prettyPrint lang=bash">
targets : prerequisites
	command
</pre>


2.&ensp;通配符

&ensp;&ensp;&ensp;&ensp;<code>make</code>支持三各通配符：<code>*</code>，<code>?</code>和<code>[]</code>，这是和<code>Unix</code>的<code>B-Shell</code>是相同的。分别表示匹配零个或多个字符、匹配任意一个字符和匹配括弧 中的任意单一字符。

3.&ensp;文件搜寻

&ensp;&ensp;&ensp;&ensp;在一些大的工程中，通常是把这许多的源文件分类，并存放在不同的目录中。当<code>make</code>需要去找寻文件的依赖关系时，你可以在文件前加上路径，但最好的方法是把一个路径告诉<code>make</code>，让<code>make</code>自动去找。一般来说有两种方法：

* <code>Makefile</code>文件中的特殊变量<code>VPATH</code>。如果没有指明这个变量，<code>make</code>只会在当前的目录中去找寻依赖文件和目标文件。如果定义了这个变量，那么，<code>make</code>就会在当前目录找不到的情况下，到所指定的目录中去找寻，如：

<pre class="prettyPrint lang=bash">
VPATH = src:../headers
#上面的的定义指定两个目录，"src"和"../headers"，目录由冒号分隔。
# make会在当前目录搜索不到的情况下，按照上述顺序进行搜索。
</pre>

* 使用<code>make</code>的<code>vpath</code>关键字，这和上面提到的那个VPATH变量很类似。这种方法更为灵活，它可以指定不同的文件在不同的搜索目录中。

<pre class="prettyPrint lang=bash">
# 它的使用方法有三种：
vpath <pattern> <directories>
# 为符合模式<pattern>的文件指定搜索目录<directories>
vpath <pattern>
# 清除符合模式<pattern>的文件的搜索目录
vpath
# 清除所有已被设置好了的文件搜索目录

# vapth使用方法中的<pattern>需要包含"%”字符，“%”的意思是匹配零或若干字符
vpath %.h ../headers
# 该语句表示，要求make在“../headers”目录下搜索所有以“.h”结尾的文件

# 我们可以连续地使用vpath语句，以指定不同搜索策略：
vpath %.c foo
vpath % blish
vpath %.c bar
# 其表示“.c”结尾的文件，先在“foo”目录，然后是“blish”，最后是“bar”目录
vpath %.c foo:bar
vpath % blish
# 上面的语句则表示“.c”结尾的文件，先在“foo”目录，然后是“bar”目录，最后才是“blish”目录
</pre>
