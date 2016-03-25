---
layout: post
title: Makefile学习笔记
description: 在编写Makefile文件的过程中，做的一些笔记。
categories: Tools
tags: Git

---

<link rel="stylesheet" type="text/css" href="/assets//css/style.css">


&ensp;&ensp;&ensp;&ensp;本篇文章是自己在学习Makefile时的笔记，旨在编写一部简明扼要Makefile使用手册。要学的东西太多了，今天学，明天忘，多做笔记总是好的。希望在以后都记不起来的时候，看一眼文章就能快速想起这些东西。
<p/>

<p class="my_header1">第1章  Makefile基础</p>


<strong>一、简要介绍</strong>

&ensp;&ensp;&ensp;&ensp;C/C++源文件，首先会被编译生成中间目标文件，再由中间目标文件链接生成执行文件。在编译时，编译器只检测程序语法，和函数/变量是否被声明；如果函数未被声明，编译器会给出一个警告，但可以生成Object File；在链接时，链接器会在所有的Object File中找寻函数的实现，如果找不到，那到就会报链接错误码，指出链接器未能找到函数的实现。

<strong>二、典型示例</strong>

&ensp;&ensp;&ensp;&ensp;在这个示例中，工程有8个C文件和3个H文件，我们要写一个Makefile来告诉make命令如何编译和链接这几个文件。规则如下：<br/>
&ensp;&ensp;&ensp;&ensp;A.如果这个工程没有编译过，那么所有的C文件都要编译并被链接。<br/>
&ensp;&ensp;&ensp;&ensp;B.如果这个工程的某几个C文件被修改，那么只编译被修改的C文件，并链接目标工程。<br/>
&ensp;&ensp;&ensp;&ensp;C.如果这个工程的头文件被改变了，那么只编译引用了这几个头文件的C文件，并链接目标程序。<br/>
按照上述规则，编写Makefile文件如下：

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


&ensp;&ensp;&ensp;&ensp;在默认的方式下，也就是我们只输入make命令，执行流程如下：<font style="color:red;">(1)</font>首先make会在当前目录下找名字叫Makefile或makefile的文件。<font style="color:red;">(2)</font>如果找到，它会找文件中的第一个target，并把这个文件作为最终的目标文件。<font style="color:red;">(3)</font>如果最终目标文件不存在，或其所依赖的.o文件修改时间比它更新，就会执行后面所定义的命令来生成这个文件。<font style="color:red;">(4)</font>如果最终目标文件所依赖的.o文件也不存在，或者.o文件比其依赖文件修改时间更早，就会根据其对应规则先生成.o文件。<font style="color:red;">(5)</font>重复上述的递推过程，直到遇到源代码文件，再按照逆序一步步地生成最终目标文件。

<strong>三、基本规则</strong>

1.&ensp;Makefile文件构成

&ensp;&ensp;&ensp;&ensp;包含五个部分：<font style="color:red;">(1)</font>显式规则。说明了如何生成一个或多的的目标文件。这是由Makefile的书写者明显指出，要生成的文件，文件的依赖文件，生成的命令。在Makefile中的命令，必须要以[Tab]键开始。<font style="color:red;">(2)</font>隐晦规则。可以让我们比较粗糙地简略地书写Makefile，这是由make所支持的。<font style="color:red;">(3)</font>变量定义。变量一般都是字符串，有点你C语言中的宏，当Makefile被执行时，其中的变量都会被扩展到相应的引用位置上。<font style="color:red;">(4)</font>文件指示。包括了三个部分：一个是在一个Makefile中引用另一个Makefile，就像C语言中的include一样；另一个是指根据某些情况指定Makefile中的有效部分，就像C语言中的预编译#if一样；还有就是定义一个多行的命令。<font style="color:red;">(5)</font>注释。只有行注释，和UNIX的Shell脚本一样，其注释是用"#"字符。

2.&ensp;Makefile注意事项

&ensp;&ensp;&ensp;&ensp;大多数的make都支持makefile和Makefile这两种默认文件名。如果要指定特定的Makefile，你可以使用make的-f和--file参数，如make -f Make.Linux。<br/>
&ensp;&ensp;&ensp;&ensp;在Makefile使用include关键字可以把别的Makefile包含进来，这很像C语言的#include，被包含的文件会原模原样的放在当前文件的包含位置。make命令开始时，如果文件都没有指定绝对路径或是相对路径的话，make会在当前目录下首先寻找，如果当前目录下没有找到，那么，make还会在下面的几个目录下找：<font style="color:red;">(1)</font>如果make执行时，有-I或--include-dir参数，那么make就会在这个参数所指定的目录下去寻找；<font style="color:red;">(2)</font>如果目录[prefix]/include（一般是：/usr/local/bin或/usr/include）存在的话，make也会去找。<br/>
&ensp;&ensp;&ensp;&ensp;GNU的make工作时的执行步骤入下：<font style="color:red;">(1)</font>读入所有的Makefile；<font style="color:red;">(2)</font>读入被include的其它Makefile；<font style="color:red;">(3)</font>初始化文件中的变量；<font style="color:red;">(4)</font>推导隐晦规则，并分析所有规则；<font style="color:red;">(5)</font>为所有的目标文件创建依赖关系链；<font style="color:red;">(6)</font>根据依赖关系，决定哪些目标要重新生成；<font style="color:red;">(7)</font>执行生成命令。


<p class="my_header1">第2章  Makefile进阶</p>

<strong>四、书写规则</strong>

1.&ensp;语法规则

&ensp;&ensp;&ensp;&ensp;包含两个部分，一个是依赖关系，一个是生成目标的方法:

<pre class="prettyPrint lang=bash">
targets : prerequisites
	command
</pre>


2.&ensp;通配符

&ensp;&ensp;&ensp;&ensp;make支持三各通配符：*，?和[]，这是和Unix的B-Shell是相同的。分别表示匹配零个或多个字符、匹配任意一个字符和匹配括弧 中的任意单一字符。

3.&ensp;文件搜寻

&ensp;&ensp;&ensp;&ensp;在一些大的工程中，通常是把这许多的源文件分类，并存放在不同的目录中。当make需要去找寻文件的依赖关系时，你可以在文件前加上路径，但最好的方法是把一个路径告诉make，让make自动去找。一般来说有两种方法：<br/>
第一种，Makefile文件中的特殊变量VPATH。如果没有指明这个变量，make只会在当前的目录中去找寻依赖文件和目标文件。如果定义了这个变量，那么，make就会在当前目录找不到的情况下，到所指定的目录中去找寻，如：

<pre class="prettyPrint lang=bash">
VPATH = src:../headers
#上面的的定义指定两个目录，"src"和"../headers"，目录由冒号分隔。
# make会在当前目录搜索不到的情况下，按照上述顺序进行搜索。
</pre>

第二种，使用make的vpath关键字，这和上面提到的那个VPATH变量很类似。这种方法更为灵活，它可以指定不同的文件在不同的搜索目录中。如：

<pre class="prettyPrint lang=bash">
# 它的使用方法有三种：
vpath &lt;pattern&gt; &lt;directories&gt;
# 为符合模式pattern的文件指定搜索目录directories
vpath &lt;pattern&gt;
# 清除符合模式pattern的文件的搜索目录
vpath
# 清除所有已被设置好了的文件搜索目录

# vapth使用方法中的pattern需要包含"%”字符，“%”的意思是匹配零或若干字符
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

4.&ensp;伪目标

&ensp;&ensp;&ensp;&ensp;“伪目标”并不是一个文件，只是一个标签。由于“伪目标”不是文件，所以make无法生成它的依赖关系和决定它是否要执行,只有通过显示地指明这个“目标”才能让其生效。当然，“伪目标”的取名不能和文件名重名，不然其就失去了“伪目标”的意义。为了避免和文件重名的这种情况，可以使用一个特殊的标记.PHONY来显式地指明一个目标是“伪目标”，向make说明，不管是否有这个文件，这个目标就是“伪目标”。

&ensp;&ensp;&ensp;&ensp;伪目标一般没有依赖的文件。但是，也可以为伪目标指定所依赖的文件。伪目标同样可以作为“默认目标”，只要将其放在第一个。一个示例就是，如果你的Makefile需要一口气生成若干个可执行文件，但你只想简单地敲一个make完事，并且，所有的目标文件都写在一个Makefile中，那么你可以使用“伪目标”这个特性：

<pre class="prettyPrint lang=bash">
all : prog1 prog2 prog3
.PHONY : all

prog1 : prog1.o utils.o
	cc -o prog1 prog1.o utils.o
prog2 : prog2.o
	cc -o prog2 prog2.o
prog3 : prog3.o sort.o utils.o
	cc -o prog3 prog3.o sort.o utils.o
</pre>

其中，Makefile中的第一个目标会被作为其默认目标。我们声明了一个all的伪目标，其依赖于其它三个目标。由于伪目标的特性是，总是被执行的，所以其依赖的那三个目标就总是不如all这个目标新。所以，其它三个目标的规则总是会被决议。也就达到了我们一口气生成多个目标的目的。

&ensp;&ensp;&ensp;&ensp;随便提一句，从上面的例子我们可以看出，目标也可以成为依赖。所以，伪目标同样也可成为依赖。看下面的例子，其中，make clean将清除所有要被清除的文件。cleanobj和cleandiff这两个伪目标有点像“子程序”的意思。我们可以输入make cleanall和make cleanobj和make cleandiff命令来达到清除不同种类文件的目的。

<pre class="prettyPrint lang=bash">
.PHONY: cleanall cleanobj cleandiff
cleanall : cleanobj cleandiff
	rm program
cleanobj :
	rm *.o
cleandiff :
	rm *.diff
</pre>


5.&ensp;静态模式

&ensp;&ensp;&ensp;&ensp;静态模式可以更加容易地定义多目标的规则，可以让规则变得更加的有弹性和灵活。语法如下：

<pre class="prettyPrint lang=bash">
&lt;targets ...&gt;: &lt;target-pattern&gt;: &lt;rereq-patterns ...&gt;
	&lt;commands&gt;
# targets定义了一系列的目标文件，可以有通配符。是目标的一个集合。
# target-parrtern是指明了targets的模式，也就是的目标集模式。
# prereq-parrterns是目标的依赖模式，它对target-parrtern模式再进行一次依赖目标的定义。
</pre>

&ensp;&ensp;&ensp;&ensp;如果target-parrtern定义成%.o，意思是target集合中都是以.o结尾的；而如果prereq-parrterns定义成%.c，意思是对target-parrtern所形成的目标集进行二次定义。其计算方法是，取target-parrtern模式中的%，并为其加上.c这个结尾，形成的新集合。看一个例子：

<pre class="prettyPrint lang=bash">
# $(objects)指明了我们的目标从$object中获取
# %.o表明要所有以.o结尾的目标，也就是[foo.o bar.o]
# %.c则取模式%.o的%，也就是[foo bar]，并为其加下.c的后缀，依赖目标就是[foo.c bar.c]
objects = foo.o bar.o
all: $(objects)
$(objects): %.o: %.c
$(CC) -c $(CFLAGS) $< -o $@
# $<和$@则是自动化变量，$<表示所有的依赖目标集，$@表示目标集
# 于是，上面的规则展开后等价于下面的规则：
foo.o : foo.c
$(CC) -c $(CFLAGS) foo.c -o foo.o
bar.o : bar.c
$(CC) -c $(CFLAGS) bar.c -o bar.o
</pre>

&ensp;&ensp;&ensp;&ensp;试想，如果我们的%.o有几百个，那种我们只要用这种很简单的静态模式规则就可以写完一堆规则，实在是太有效率了。静态模式规则的用法很灵活，如果用得好，那会一个很强大的功能。再看一个例子：

<pre class="prettyPrint lang=bash">
files = foo.elc bar.o lose.o
$(filter %.o,$(files)): %.o: %.c
$(CC) -c $(CFLAGS) $< -o $@
$(filter %.elc,$(files)): %.elc: %.el
emacs -f batch-byte-compile $<
# $(filter %.o,$(files))表示调用Makefile的filter函数
# 过滤$files集，只要其中模式为%.o的内容
</pre>


6.&ensp;自动生成依赖

&ensp;&ensp;&ensp;&ensp;在Makefile中，依赖关系可能会需要包含一系列的头文件。但是，如果是一个比较大型的工程，你必需清楚哪些C文件包含了哪些头文件，并且，你在加入或删除头文件时，也需要小心地修改Makefile，这是一个很没有维护性的工作。为了避免这种繁重而又容易出错的事情，我们可以使用C/C++编译的一个功能。大多数的C/C++编译器都支持一个-M的选项，即自动找寻源文件中包含的头文件，并生成一个依赖关系。例如，如果我们执行下面的命令：

<pre class="prettyPrint lang=bash">
cc -M main.c
# 其输出是：
main.o : main.c defs.h
# 如果是GNU的C/C++编译器，得用-MM参数；-M参数会把标准库的头文件也包含进来
gcc -MM main.c
# 其输出是：
main.o : main.c defs.h
</pre>


&ensp;&ensp;&ensp;&ensp;那么，编译器的这个功能如何与我们的Makefile联系在一起，让Makefile自已依赖于源文件呢？GNU组织建议把编译器为每一个源文件自动生成的依赖关系放到一个文件中，为每一个name.c的文件都生成一个name.d的Makefile文件。于是，我们可以写出.c/.h文件和.d文件的依赖关系，并让make自动生成和更新.d文件，并把其包含在我们的主Makefile中，这样，我们就可以自动化地生成每个文件的依赖关系。

<pre class="prettyPrint lang=bash">
# 这里，我们给出了一个模式规则来产生[.d]文件：
%.d: %.c
	@set -e; rm -f $@; \
	$(CC) -M $(CPPFLAGS) $< > $@.$$$$; \
	sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $@.$$$$ > $@; \
	rm -f $@.$$$$
sources = foo.c bar.c
include $(sources:.c=.d)
# 1. 第一行所有的[.d]文件依赖于[.c]文件
# 2. 第二行@关键字告诉make不输出该行命令；set -e是说当后面的命令的返回值非0时立即退出
# 3. 第二行"rm -f $@"的意思是删除所有的目标，也就是[.d]文件
# 4. 第三行是为每个依赖文件“$<”，也就是[.c]文件生成依赖文件，“$@”表示模式“%.d”文件
# 5. 第三行的“$$$$”为一个随机编号，表示生成结果存储在一个形如"name.d.1234"临时文件中
# 6. 第四行使用sed命令做了一个替换，将"name.d"加入到目标集合中
# 7. 第五行是删除临时文件
# 8. 第六行"$(sources:.c=.d)"是把变量$(sources)所有[.c]的字串都替换成[.d]
# 9. 第七行表示将.d文件包含到主Makefile文件中

# 总而言之，这个模式要做的事就是在编译器生成的依赖关系中加入[.d]文件的依赖
# 即把依赖关系(以foo的依赖关系为例)：
foo.o : foo.c defs.h
# 转成：
foo.o foo.d : foo.c defs.h
# 于是，我们的[.d]文件也会自动更新了，并会自动生成了
</pre>

<br/><br/>
参考资料：

1.&ensp;<a href="{{ site.BASE_PATH}}/assets/source/20080330Makefile.pdf" download>跟我一起写Makefile(陈皓)</a><br/>
