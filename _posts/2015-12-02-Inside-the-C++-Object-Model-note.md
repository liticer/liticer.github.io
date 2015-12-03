---
layout: post
title: 深度探索C++对象模型学习笔记
description: 阅读侯捷老师翻译的Lippman大作《Inside the C++ Object Mode》过程中，在自己理解和体会的基础上做了一些笔记。
categories: CPP
tags: Object Model

---

##<font color="blue">第1章 关于对象</font>##

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

##<font color="blue">第2章 构造函数语意学</font>##

1.&ensp;Default Constructor的构造操作<br/>

&ensp;&ensp;对于一个类，如果没有任何user-declared constructor，那么在编译器有需要的时候，会为它合成一个nontrival default constructor。通常，有如下4种情况需要合成copy constructor:

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


3.&ensp;程序转化语意学<br/>

  * 参数初始化：在非引用参数传入之前，可能会先创建一个临时变量存储参数。然后在调用函数时以引用方式传入这个临时变量，当然函数的声明也会做相应的修改。
  * 返回值初始化：如果函数的返回值不是引用变量，会在函数调用前创建一个临时变量存储返回值。然后在调用函数时以引用方式传入这个临时变量，当然函数的声明也会作相应的修改。
  * 使用者层面的优化：如果函数的返回值不是引用变量，则在函数return时创建临时变量比在函数开始处创建临时变量要好，有可能会减少一次copy constructor的调用。如果不懂，可以联系上一条结论理解。
  * 编译器层面的优化：如果函数中所有return指令传回相同的变量，编译器有可能会以返回值result参数取代named return value, 这个过程也被叫做NRV优化。
  * Copy constructor的取舍：当class的default copy constructor被时为trivial的时候，一般情况下不需要为其提供emplicit的copy constructor。然而如果class需要大量的memberwise的初始化操作，那么就可以给它提供一个copy constructor；一方面结合编译器作NRV优化，另一方面可以用memcpy函数提高拷贝效率。


4.&ensp;成员初始化<br/>

  * Member initialization list必需的情况：初始化一个reference member；初始化一个const member；初始化member object时需要调用含参构造函数；初始化base class时需要调用含参构造函数。
  * Member initialization list的初始化顺序：一个object的构造总是先构造其base subobject部分，而member的初始化总是要按顺序被安插在任何explicit user code之前。在每一个constrctor中的member初始化时，需要先调用base class的constructor，然后在按成员在class中的顺序逐一初始化各个成员，最后执行explicit user code
。
  * 初始化的一些特殊情况：以member function的结果初始化member; 以member function的结果作为base class constructor的参数。Member function的调用是合法的，因为在object相关的this指针在构建时已经准备妥当，但还是要尽量避免上述情况。具体原因时，构造函数调用前，object的data member有可能还未被全部初始化；而在调用构造base class subobject时，通过this指针调用虚函数时将有可能发生异常的动态绑定过程。


##<font color="blue">第3章 Data语意学</font>##















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
</pre>

