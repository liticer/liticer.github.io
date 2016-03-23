---
layout: post
title: 深度探索C++对象模型学习笔记
description: 阅读侯捷老师翻译的Lippman大作《Inside the C++ Object Model》过程中，在自己理解和体会的基础上做了一些笔记。
categories: CPP
tags: Object Model

---


<p style="font-weight:700;font-size:20px;color:Magenta;text-align:center;padding:20px 0">第1章 关于对象</p>

>**C++对象的布局成本**

* C++中单纯地使用封装和继承，并不会增加存取时间和存储空间上的成本。
* C++真正需要的额外成本是由<code>Virtual</code>引起的(包括<code>Virtual function</code>和<code>Virtual base class</code>)。

>**C++对象模型**

* 数据成员：<br/><code>Nonstatic data members</code>被配置于每一个<code>class object</code>之内；<code>Static data members</code>被存放在个别的<code>class object</code>之外。
* 非虚函数成员：<br/><code>Nostatic/Static function members</code>均被置于个别的<code>class object</code>之外，同一般的非成员函数处理机制类似。
* 虚函数成员：<br/>
(1)每一个<code>class</code>产生出一堆指向<code>virtual functions</code>的指针，存放在一个叫做<code>virtual table(vtbl)</code>的表格之中。通常一个<code>class</code>所关联的<code>type_info object</code>被存放在该表格的第一个<code>slot</code>中。<br/>
(2)每一个<code>class object</code>被安插一个叫做<code>virtual pointer(vptr)</code>的指针，指向相关的<code>virtual table</code>。通常<code>vptr</code>会被每一个<code>class</code>的<code>constructor</code>，<code>destructor</code>和<code>copy assignment</code>等函数自动地进行设定和重置。







<p style="font-weight:700;font-size:20px;color:Magenta;text-align:center;padding:20px 0">第2章 构造函数语意学</p>

>**Default Constructor的构造操作**

&ensp;&ensp;&ensp;&ensp;对于一个类，如果没有任何<code>user-declared constructor</code>，那么在编译器有需要的时候，会为它合成一个<code>nontrival default constructor</code>。通常，有如下4种情况需要合成<code>copy constructor</code>：

  * 该<code>class</code>有"带<code>Default Constructor</code>"的<code>Data member</code>：<br/>需要在构造函数中调用该<code>Data member</code>的默认构造函数初始化该成员。
  * 该<code>class</code>有"带<code>Default Constructor</code>"的<code>Base class</code>：<br/>需要在构造函数中调用<code>Base class</code>的默认构造函数初始化<code>Base class subobject</code>。
  * 该<code>class</code>有"<code>Virtual Function</code>"：<br/>需要在构造函数中生成或维护<code>vtbl</code>，并设置或修改<code>vptr</code>。
  * 该<code>class</code>有"<code>Virtual base class</code>"：<br/>需要在构造函数中维护<code>vtbl</code>和<code>vptr</code>，保证<code>virtual base class</code>在每一个<code>derived class object</code>中的位置在执行期准备妥当。

&ensp;&ensp;&ensp;&ensp;至于没有存在上述4种情况且没有声明任何<code>constructor</code>的<code>class</code>，我们说它拥有的是<code>implicit trivial default constructor</code>，它们实际上不会被合成出来。

&ensp;&ensp;&ensp;&ensp;C++新手一般有两个常见的误解：
(1)任何<code>class</code>，如果没有定义<code>default constructor</code>，就会被合成出来一个。
(2)编译器默认合成出来的<code>default constructor</code>会显式地设定“<code>class</code>内每一个<code>data member</code>的默认值”。


>**Copy Constructor的构造操作**

&ensp;&ensp;&ensp;&ensp;调用<code>Copy constructor</code>三种情况分别是：初始化，传参和返回值。和<code>default construtor</code>一样，<code>copy constructor</code>也分为<code>trivial</code>和<code>nontrivial</code>两种，只有<code>nontrivial</code>的<code>class</code>才会合成它。倘若一个<code>class</code>展现出所谓的"<code>bitwise copy semantics</code>"，那么它的<code>copy constructor</code>就是<code>trivival</code>的。一个<code>class</code>不展现出"<code>bitwise copy semantics</code>"的4种情况如下：<br/>

  * 当<code>class</code>内含有一个<code>member object</code>，而后者的<code>class</code>声明有一个<code>copy constructor</code>时(不论是被<code>class</code>设计者显式声明，还是被编译器合成都算)，该<code>class</code>的<code>copy constructor</code>需要调用该<code>member object</code>的<code>copy constructor</code>完成该成员的拷贝构造。
  * 当<code>class</code>继承自一个<code>base class</code>，而后者存在一个显式声明的<code>copy constructor</code>时，该<code>class</code>的<code>copy constructor</code>需要调用<code>base class</code>的<code>copy constructor</code>完成<code>base class subobject</code>的拷贝构造。
  * 当<code>class</code>声明了一个或多个<code>virtual functions</code>时，该<code>class</code>的<code>copy constructor</code>需要维护<code>vptr</code>指针，保证其指向对应的<code>class</code>的<code>vtbl</code>。
  * 当<code>class</code>派生于一个继承串链，其中有一个或多个<code>virtual base classes</code>时，该<code>class</code>的<code>copy constructor</code>需要拷贝构造<code>virtual base subobject</code>，同时维护<code>vptr</code>指针确保其指向对应的<code>class</code>的<code>vtbl</code>。


>**程序转化语意学**

  * 参数初始化：在非引用参数传入之前，可能会先创建一个临时变量存储参数。然后在调用函数时以引用方式传入这个临时变量，当然函数的声明也会做相应的修改。
  * 返回值初始化：如果函数的返回值不是引用变量，会在函数调用前创建一个临时变量存储返回值。然后在调用函数时以引用方式传入这个临时变量，当然函数的声明也会作相应的修改。
  * 使用者层面的优化：如果函数的返回值不是引用变量，则在函数<code>return</code>时创建临时变量比在函数开始处创建临时变量要好，有可能会减少一次<code>copy constructor</code>的调用。如果不懂，可以联系上一条结论理解。
  * 编译器层面的优化：如果函数中所有<code>return</code>指令传回相同的变量，编译器有可能会以返回值<code>result</code>参数取代<code>named return value</code>， 这个过程也被叫做NRV优化。
  * <code>Copy constructor</code>的取舍：当<code>class</code>的<code>default copy constructor</code>被时为<code>trivial</code>的时候，一般情况下不需要为其提供<code>emplicit</code>的<code>copy constructor</code>。然而如果<code>class</code>需要大量的<code>memberwise</code>的初始化操作，那么就可以给它提供一个<code>copy constructor</code>；一方面结合编译器作NRV优化，另一方面可以用<code>memcpy</code>函数提高拷贝效率。


>**成员初始化**

  * <code>Member initialization list</code>必需的情况：初始化一个<code>reference member</code>；初始化一个<code>const member</code>；初始化<code>member object</code>时需要调用含参构造函数；初始化<code>base class</code>时需要调用含参构造函数。
  * <code>Member initialization list</code>的初始化顺序：一个<code>object</code>的构造总是先构造其<code>base subobject</code>部分，而<code>member</code>的初始化总是要按顺序被安插在任何<code>explicit user code</code>之前。在每一个<code>constrctor</code>中的<code>member</code>初始化时，需要先调用<code>base class</code>的<code>constructor</code>，然后在按成员在<code>class</code>中的顺序逐一初始化各个成员，最后执行<code>explicit user code</code>
。
  * 初始化的一些特殊情况：以<code>member function</code>的结果初始化<code>member</code>；以<code>member function</code>的结果作为<code>base class constructor</code>的参数。<code>Member function</code>的调用是合法的，因为在<code>object</code>相关的<code>this</code>指针在构建时已经准备妥当，但还是要尽量避免上述情况。具体原因时，构造函数调用前，<code>object</code>的<code>data member</code>有可能还未被全部初始化；而在调用构造<code>base class subobject</code>时，通过<code>this</code>指针调用虚函数时将有可能发生异常的动态绑定过程。

  
  
  
  
  
  
  
<p style="font-weight:700;font-size:20px;color:Magenta;text-align:center;padding:20px 0">第3章 Data语意学</p>

>**Data member的绑定**

&ensp;&ensp;&ensp;&ensp;编译器对于一个<code>inline member function</code>的本体的分析，会在整个<code>class</code>的声明都出现了才开始；然而对于<code>member function</code>的<code>argument list</code>，则是在它们第一次出现时被适当地进行决议完成的。因此上，在现代C++程序设计中，需要将"<code>nested type</code>声明"放在<code>class</code>的起始处，这是一种安全的防御性程序设计风格。

>**Data member的布局**

&ensp;&ensp;&ensp;&ensp;<code>C++ Standard</code>要求，在同一个<code>access session</code>中，较晚出现的<code>members</code>在<code>class object</code>中有较高的地址。同时，编译器还可能会合成一些内部使用的<code>data member</code>(如<code>vptr),传统上它们通常被放在所有显式声明的<code>members</code>之前或者之后。

>**Data member的存取**

   * <code>Static data members</code>对每个<code>class</code>来说只有一个实例，存放在从<code>class</code>之外的<code>data segment</code>中，并被视为一个<code>global</code>变量；不论通过实例访问，还是通过类名访问，都会在内部被转化成类名的访问形式。

   * <code>Nonstatic data members</code>直接存放在每一个<code>object</code>当中。每一个<code>nonstatic data member</code>的偏移位置在编译时期即可获知，因此存取一个<code>nonstatic data member</code>的效率和存取一个<code>C struct member</code>的效率是一样的。唯一的例外是，当使用指针或引用访问<code>member</code>时，该指针或引用指向的<code>class</code>的继承结构中有一个<code>virtual base class</code>，且该<code>member</code>是从该<code>virtual base class</code>继承而来的。这种情况下，因为不知道该指针或引用指向哪一种<code>class type</code>，因此存取操作必须延迟至执行期，经由一个额外的间接引导才能解决。

>**继承与data member**
   
   * 单一继承不含<code>virtual functions</code>：
      * 一个<code>object</code>由两部分构成，<code>base class subobject</code>和本身的<code>data members</code>。这种情况下并不会增加空间或者时间上的额外负担。
   * 单一继承且含<code>virtual functions</code>：
      * 为每一个<code>class</code>导入一个<code>virtual table</code>，用来存放它所声明的每一个<code>virtual function</code>的地址。
      * 在每一个<code>class object</code>种导入一个<code>vptr</code>，提供执行期的链接，使每一个<code>object</code>都能找到相应的<code>virtual table</code>。对<code>base class</code>来说，<code>vptr</code>在<code>object</code>中的位置通常在所有<code>data members</code>之后；而<code>derived class object</code>会继承<code>base class</code>的<code>vptr</code>，不用单独再留存储空间。
      * 加强<code>constructor</code>，使它能够为<code>vptr</code>设定初值，让它指向<code>class</code>所对应的<code>virtual table</code>。这可能意味者在<code>derived class</code>和每一个<code>base class</code>的<code>constructor</code>中，会重新设定<code>vptr</code>的值。
      * 加强<code>destructor</code>，使它能够矫正<code>vptr</code>，让它指向<code>class</code>所对应的<code>virtual table</code>。因为，<code>vptr</code>很可能已经在<code>derived class destructor</code>中被设定为<code>derived class</code>的<code>virtual table</code>的地址了。
   * 多重继承：
      * 对于多重继承来说，一个<code>derived class object</code>由几部分组成：<code>base class1 subobject，base class2 subobject， ..., data members</code>。在这种情况下，把一个<code>derived object</code>转换为其<code>base</code>类型，就需要编译器的介入，用以调整地址。
      * 多重继承的情况下，如果一个<code>derived class object</code>有<code>vptr</code>，那么其<code>vptr</code>就存放在其继承列表中第一个含有<code>vptr</code>的<code>subobject</code>的<code>vptr</code>处，否则在<code>data members</code>之后新增一个<code>vptr</code>域。
   * 虚拟继承：
      * 对于虚拟继承来说，它跟多重继承的情况类似。只是它需要指出<code>shared base subobject</code>的偏移位置，而这个偏移量通常会被放置在<code>virtual table</code>最前面的<code>slot</code>中。在将<code>derived object</code>赋值给<code>base object</code>时，需要通过<code>virtual table</code>查找这个偏移量，并进行复制构造。
      * 当通过<code>object</code>来存取一个从<code>virtual base class</code>的<code>member</code>，可以被优化成一个直接存取操作；然而通过指针或引用来访问上述<code>member</code>时，就需要在执行期通过查找<code>virtual table</code>中的<code>offset</code>，经过两次间接引导才能访问到。因此上，<code>virtual base class</code>最有效的一种运用形式就是：一个抽象的<code>virtual base class</code>，没有任何的<code>data member</code>。

>**指向data members的指针**

   * 对<code>class</code>的<code>nonstatic member</code>取地址得到的是一个偏移值，表示该<code>member</code>在<code>class</code>中的偏移位置，可以将该值赋给一个指向该<code>class</code>的<code>data member</code>的指针；而对<code>object</code>的<code>nonstatic member</code>取地址得到的是一个地址值，表示该<code>object</code>中的<code>data member</code>的地址，可以将该值赋给一个指向该<code>member</code>类型的指针。
   * 对<code>class</code>或者<code>object</code>中的<code>static member</code>取地址得到的是一个地址值，表示该<code>class</code>中<code>static member</code>的在内存中的位置，可以将该值赋给一个指向该<code>member</code>类型的指针。
   * 为了区分一个"没有指向任何<code>data member</code>的指针"和"一个指向第一个<code>data member</code>的指针",每一个真正的<code>member offset</code>值都会被加上1，而在使用该<code>offset</code>取值之前，需要减掉1。


   
   
   
   
<p style="font-weight:700;font-size:20px;color:Magenta;text-align:center;padding:20px 0">第4章 Function语意学</p>

>**Member function的各种调用方式**<br/>
   
   * <code>Nonstatic member functions：
      * C++的设计准则之一就是：<code>nonstatic member function</code>至少必须和一般的<code>nonmember function</code>有相同的效率。
      * 在编译器内部，会将<code>member function</code>实例转换为对等的<code>nonmember function</code>实例。通常<code>member function</code>的函数名称会被"<code>mangling</code>"为程序中独一无二的名称，其函数原型会被安插一个额外的<code>this</code>指针参数，其"对<code>nonstatic data member</code>的存取操作"会被改写成通过<code>this</code>指针的存取操作。
   
   * <code>Virtual member functions</code>：
      * 如果通过指针或引用去访问一个<code>virtual member function</code>，将在编译器内部被转换为通过查询<code>virtual table</code>进行访问的形式。
      * 如果通过<code>object</code>取访问一个<code>virtual member function</code>，其在编译器内部的转换方式跟<code>nonstatic member function</code>相同。
   
   * <code>Static member functions</code>：
      * 无论通过何种形式访问一个<code>static member function</code>，总是会被转化一个对对等的<code>nonmember function</code>的访问形式。通常<code>static member function</code>的函数名称会被"<code>mangling</code>"为程序中独一无二的名字。
      * <code>Static member functions</code>的主要特性就是它没有<code>this</code>指针。因此上，它不可以访问<code>class</code>中的<code>nonstatic members</code>，也不能够被声明为<code>const</code>，<code>volatile</code>或<code>virtual</code>。

>**Virtual member functions**<br/>
   
   * 单一继承下的<code>virtual functions</code>：
      * 含有<code>virtual functions</code>的单一继承下，一个<code>class</code>只会有一个<code>virtual table</code>，每一个<code>table</code>中含有该从<code>class</code>的类型信息和对应<code>class object</code>中所有<code>active virtual functions</code>函数实例的地址。其中的<code>active virtual functions</code>包括继承自<code>base class</code>的<code>virtual functions</code>，重写的<code>base class</code>的<code>virtual functions</code>，自己定义的<code>virtual functions</code>。
      * 含有<code>virtual functions</code>的单一继承下，一个<code>class object</code>中会被安插一个指向该<code>class virtual table</code>的指针。为了找到函数地址，编译器会为每一个<code>virtual function</code>指派一个表格索引值。
  
   * 多重继承下的<code>virtual functions</code>：
      * 含有<code>virtual functions</code>的多重继承下，一个<code>derived class</code>内含有n个<code>virtual tables</code>，n表示其上一层的<code>base class</code>的个数。其中包含1个主要实例(由<code>derived class</code>于<code>base1 class</code>共享),n-1个次要实例(除<code>base1 class</code>之外的每个<code>base class</code>各享一个).针对每一个<code>virtual table</code>，<code>derived</code>对象中都有一个对应的<code>vptr</code>，需要在构造，复制，析构时进行适当的维护。为了调节执行期链接器的效率，编译器或许会将多个<code>virtual tables</code>连锁为一个，指向次要表格的指针，可以主要表格名称加上一个<code>offset</code>获得。
      * 在多重继承中支持<code>virtual functions</code>，其复杂度围绕在第二个及后继的<code>base  class</code>身上，以及必须在执行期调整<code>this</code>指针这一点上。具体地有三种情况，第二或后继的<code>base class</code>会影响对<code>virtual function</code>的支持:(1) 通过一个指向"第二个<code>base class</code>或后继"的指针，调用<code>derived class virtual function</code>;(2) 通过一个指向"<code>derived class</code>"的指针，调用第二个<code>base class</code>或后继中继承而来的<code>virtual function</code>;(3)允许一个<code>virtual function</code>的返回值类型有所变化，可能时<code>base type</code>，也可能时<code>derived type</code>。

   * 虚拟继承下的<code>virtual functions</code>：
      * 含有<code>virtual functions</code>的虚拟继承下，编译器会在生成<code>virtual table</code>的时，在<code>table</code>的首部加入一个额外的<code>slot</code>(索引为-1),指出<code>virtual base</code>的偏移量。
      * 强烈建议，不要在一个<code>virtual base class</code>中声明<code>nonstatic data members</code>，只将它作为一个接口使用即可。


>**指向member function的指针**<br/>
  
   * <code>Nonvirtual member function</code>指针：对一个<code>nonstatic member function</code>取地址得到的是一个带有相同参数+额外参数(<code>this</code>指针)的普通函数指针；而对一个<code>static member function</code>取地址得到的是一个相同参数的普通函数指针。
   * <code>Virtual member function</code>指针：
      * 对一个单一继承下的<code>virtual member function</code>取地址得到的它在<code>virtual table</code>中的索引值；对一个多重继承下的<code>virtual member function</code>取地址得到的是一个结构体，除了反应<code>virtual table</code>索引值之外，还要反应<code>this</code>指针的<code>offset</code>值。

>**Inline functions**<br/>
  
   * 定义在类内的函数，隐式为内联的；在类外声明的内联函数，须加<code>inline</code>声明。并非所有的<code>inline</code>声明都会变成<code>inline</code>函数，代码过多的话，编译器可能会拒绝，转而将它作为普通函数。
   * 内联函数的形参：传入参数，直接替换为参数名；传入常量，直接替换为常量值；传入函数运行结果，则需要导入临时变量。
   * 内联函数的局部变量：局部变量会被"<code>mangling</code>",以便<code>inline</code>函数被替换后局部变量名字唯一。也就是说，一次性调用N次，就会出现N个临时变量，程序体积会暴增。总之，<code>inline</code>的使用要小心处理。

   
   
   
   
   
<p style="font-weight:700;font-size:20px;color:Magenta;text-align:center;padding:20px 0">第5章 构造，析构，拷贝语意学</p>
  
>**关于纯虚函数**<br/>
   
&ensp;&ensp;&ensp;&ensp; 原则上允许定义和调用一个<code>pure virtual function</code>。不过它只能被静态调用(即通过类名调用),不能经由虚拟机制调用(即通过指针或引用调用).不过<code>pure virtual destructor</code>必须被定义，因为每一个<code>derived class destructor</code>都会被编译器加以扩张，以静态方式调用其"每一个<code>virtual base class</code>"和"上一层<code>base class</code>"的<code>destructor</code>。所以一个比较好的替代方案是，不要把<code>virtual destructor</code>声明为<code>pure</code>。

>**无继承情况下的对象构造**<br/>
  
   * <code>Plain OI Data</code>声明形式：在这种情况下，该类的<code>constructor</code>和<code>destructor</code>被视为<code>trival</code>的，不是没被定义就是没被调用。此时的<code>copy assignment operator</code>会直接进行像C那样的纯粹位搬移操作。
   * <code>Abstract Data Type</code>声明形式：在这种情况下，该类的表现与上一种情况类似。简单的封装并没有给C++带来任何额外的负担。
   * 含有<code>virtual function</code>的情况：在这种情况下，<code>destructor</code>仍然是<code>trival</code>的，而<code>constrcutor</code>和<code>copy operator</code>不再是<code>trival</code>的了。因为<code>virtual functions</code>的出现，使得每一个<code>object</code>含有一个<code>vptr</code>，所以<code>constructor</code>，<code>copy constructor</code>和<code>copy operator</code>都需要被编译器安插代码初始化<code>object</code>的<code>vptr</code>指针。

>**继承体系下的对象构造**<br/>
   
&ensp;&ensp;&ensp;&ensp;继承体系下<code>constructor</code>的扩充步骤： 

   * 如果有，调用所有的<code>virtual base class constructors</code>，从左到右，从深到浅。
       * 如果<code>class</code>被列于<code>member initialization list</code>中，那么任何显式指定的参数都应该被传递过去；否则，调用<code>class</code>的<code>default constructor</code>，如果没有，就报错。
       * 此外，<code>class</code>中的每一个<code>virtual base class subobject</code>的偏移位置必须在执行期可被存取，以便在进行上述操作时移动<code>this</code>指针。
       * 如果<code>class object</code>时最底层的<code>class</code>，其<code>constructors</code>可能被调用。用以支持这一行为的机制必须被放进来。
   * 如果有，调用上一层的<code>base class constructors</code>，以<code>base class</code>的声明顺序为顺序。
       * 如果<code>class</code>被列于<code>member initialization list</code>中，那么任何显式指定的参数都应该被传递过去；否则，调用<code>class</code>的<code>default constructor</code>，如果没有，就报错。
       * 如果<code>base class</code>是多重继承下的第二或后继的<code>base class</code>，必须根据情况调整<code>this</code>指针以指向正确的位置。
   * 如果有，指定<code>vptr</code>的初值，以便指向正确的<code>virtual table</code>。
   * 如果有，如果类中有<code>member</code>出现在<code>member initialization list</code>或者含有一个<code>default constructor</code>，按照它们在类中被声明的顺序依次进行初始化。
   * 如果有，执行用户显式指定的代码部分，即构造函数的显式函数体。

&ensp;&ensp;&ensp;&ensp;继承体系下构造过程中需要注意的地方： 

   * 虚拟继承下的<code>virtual base class</code>构造：这种情况下，<code>virtual base subobject</code>的构造总是由继承链中最底层的<code>class</code>来否则。因此需要在构造函数中额外加入一个参数，指示该<code>class</code>是否为<code>most_derived</code>，如果是，则构造，否则，就跳过。
   * 继承体系下对象的构造过程：令每一个<code>base class constructor</code>设定其对象的<code>vptr</code>，使它指向相关的<code>virtual table</code>，构造中的对象就可以严格而正确地变成"构造过程中所幻化出来的每一个<code>class</code>"的对象。也即是说，一个<code>PVertex</code>对象会先形成一个<code>Point</code>对象，一个<code>Point3d</code>对象，一个<code>Vertex</code>对象，一个<code>Vertex3d</code>对象，然后才成为一个<code>PVertex</code>对象。
   * 在一个<code>class</code>的<code>constructor</code>的<code>member initilization list</code>中调用该<code>class</code>的一个虚函数，用其返回值作为<code>member</code>初始化的参数：在原则是安全的，因为<code>vptr</code>保证能够在<code>member initilization list</code>被扩展之前，由编译器正确设定好；在语意上是不安全的，因为该虚函数本身可能依赖于尚未被设定初值的<code>members</code>，这种做法并不推荐。
   * 在一个<code>class</code>的<code>constructor</code>的<code>member initilization list</code>中调用<code>class</code>的一个虚函数，用其返回值作为<code>base class constructor</code>的参数：这种做法是不安全的，因为此时<code>vptr</code>若不是未被设定好，就是指向错误的<code>class</code>，这种情况绝对不允许。    

>**对象复制语义学**<br/>
   
   * <code>Copy operator</code>的工作：一个<code>copy operator</code>会在需要的情况下被编译器合成出来，然而当该合成的函数不能满足需要时，我们需要自己定义它。一般地，一个<code>copy operator</code>需要负责复制自身的成员，并调用<code>base class</code>的<code>copy operator</code>来<code>copy base subobject</code>。
   * 虚拟继承下的<code>copy operator</code>：这种情况下，由于不能抑制<code>Base class</code>中对<code>shared virtual base subobject</code>的<code>copy</code>动作，因此上会发生<code>shared virtual base subobject</code>的多重拷贝过程。建议做法是尽可能不要允许一个<code>virtual base class</code>的拷贝操作，甚至不要再任何<code>virtual base class</code>中声明数据。

>**析构语义学**<br/>
   
&ensp;&ensp;&ensp;&ensp;一个由程序员定义的<code>destructor</code>被扩展的方式类似<code>constructor</code>被扩展的方式，但是顺序相反：
   
   * 如果有，重设该<code>object</code>的<code>vptr</code>指针，指向相关的<code>virtual table</code>。 
   * 如果有，<code>destructor</code>的函数本体被执行，即用户定义的相关操作。
   * 如果有，按照成员在<code>class</code>中被声明的顺序的相反顺序，调用<code>member class objects</code>的<code>destructor</code>。
   * 如果有，按照<code>base class</code>声明顺序的相反顺序，调用任何直接的<code>nonvirtual base classes</code>的<code>destructor</code>。
   * 如果有，假如讨论的是类是<code>most-derived</code>的，按照<code>virtual base classes</code>被声明的顺序的相反顺序，调用其<code>destructor</code>。

   
   
   
   
   

<p style="font-weight:700;font-size:20px;color:Magenta;text-align:center;padding:20px 0">第6章 执行期语意学</p>

>**对象的构造和析构**<br/>

   * 全局对象：
      * <code>Global object</code>在程序编译时期可以被放置于<code>data segment</code>中并且内容为0，但<code>object</code>的<code>constructor</code>的调用一直到程序启动时才会被执行。因此上，一个含有<code>constructor</code>和<code>destructor</code>的<code>global object</code>需要静态初始化操作和内存释放操作。
      * 静态初始化操作通常会被统一集中起来放在<code>main</code>函数首部执行，而内存释放操作则会被统一集中起来放在<code>main</code>函数尾部执行。一个良好的建议就是不要用那些需要静态初始化的<code>global objects</code>。
   * 局部静态对象：
      * 局部静态对象也是存放在<code>data segment</code>当中，在所属函数首次被调用时进行初始化，在<code>main</code>函数尾部与全局对象一起进行内存释放。
   * 对象数组：
      * 如果<code>class</code>不含有<code>constructor</code>和<code>destructor</code>，则所需要做的工作和一个内建类型数组一样多；否则，需要在定义时调用一个类似<code>vec_new</code>的函数，将<code>constructor</code>施行于各个元素身上，在释放时需要调用一个类似<code>vec_delete</code>的函数，将<code>destructor</code>施行于各个元素身上。
      * 如果<code>class</code>含有一个以上的形式参数，且每个参数都含有默认值，那么它也可以作为数组的元素类型。编译器可能会构建一个不含参的<code>stub constructor</code>，在函数内调用<code>class</code>的<code>constructor</code>，并将默认参数显式地传递过去。

>**new和delete运算符**<br/>
      
   * 运算符<code>new</code>的操作事实上是通过两个步骤完成的：先通过适当的<code>new</code>运算符函数实例，配置所需的内存；再为配置得来的对象调用<code>constructor</code>设定初值。运算符<code>delete</code>的操作也是类似：先调用对象的<code>destructor</code>析构对象；再释放掉对象所占用的内存。(注：前提是<code>object</code>有<code>constructor</code>和<code>destructor</code>，否则不用调用)
   * 针对数组的<code>new</code>跟<code>delete</code>：如果<code>class</code>含有<code>constructor</code>和<code>destructor</code>，需要在定义时调用一个类似<code>vec_new</code>的函数，先为对象配置内存，再将<code>constructor</code>施行于各个元素之上；在释放时需要调用一个类似<code>vec_delete</code>的函数，先将<code>destructor</code>施行于各个元素之上，再释放对象所占用的内存。
   * <code>Placement operator new</code>的语意：其语意是在指定的内存位置上，调用<code>constructor</code>构造一个对应<code>class</code>的对象。而这个内存位置应该是预先已经开辟出来的：或者是该内存地址上的对象被析构而内存没有被释放；或者是一块刚开辟出来的未作任何处理的内存块。

>**临时性对象**<br/>
  
   * 临时性对象的摧毁时机：临时性对象的被摧毁，应该是对完整表达式求值过程中的最后一个步骤，该完整表达式造成临时对象的产生。
   * 临时性对象的生命规则有两个例外：第一个例外发生在表达式被用来初始化一个<code>object</code>时，临时对象应该存留到<code>object</code>的初始化操作完成为止，如用一个问号表达式的结果初始化一个<code>string</code>对象；第二个例外是当一个临时性对象被一个<code>reference</code>绑定时，临时对象将残留到<code>reference</code>的生命结束或者临时对象的生命范畴结束，如将一个<code>string</code>对象绑定到一个字符串上。

   
   
   
   
   
   
   
<p style="font-weight:700;font-size:20px;color:Magenta;text-align:center;padding:20px 0">第7章 站在对象模型的尖端</p>

>**Template**<br/>
 
   * 实例化：一个<code>template</code>会在定义了该<code>template</code>一个实例对象时，进行相应的实例化，以便产生该实例对象的真正布局形式。然而该实例的<code>member functions</code>只有在被使用的时候才要求它们被实例化。(其主要原因是：空间和时间效率的考虑；尚未实现的机能)
   * 名称决议法：一个编译器必须保持两个<code>scope contexts</code>："scope of the template declaration"用以专注于一般的<code>template class</code>；"scope of the template instantiation"用以专注于特定的实例。
   * <code>Member Function</code>的实例化行为：
       * 编译器如何找出函数的定义？包含<code>template program text file</code>，就好像它是一个头文件一样；要求一个文件命名规则，如<code>Point.h</code>的声明，其定义必被放在<code>Point.C/Point.cpp</code>中。
       * 编译器如何只实例化程序中用到的<code>member functions</code>？忽略这项要求，把一个已经实例化的<code>class</code>的所有<code>member functions</code>都产生出来；模拟链接操作，检测哪一个函数真正需要，只为它们产生实例。
       * 编译器怎么组织<code>member definitions</code>在多个<code>.o</code>文件中都被实例化？产生多个实例，然后从链接器中提供支持，只留下其中一个实例，其余都忽略；另一个方法就是由使用者来引导"模拟链接阶段"的实例化策略，决定哪些实例才是需求的。

>**异常处理**<br/>

   * 当一个<code>exception</code>发生时，编译系统必须完成以下事情：
       * 检验发生<code>throw</code>操作的函数。
       * 决定<code>throw</code>操作是否发生才<code>try</code>区段中。如果是，跳到3，否则，跳到4。
       * 把<code>exception type</code>拿来和每一个<code>catch</code>子句进行比较。如果比较吻合，就将控制流程交到<code>catch</code>子句手上；否则跳到4。
       * 首先摧毁所有的<code>active local objects</code>；然后从堆栈中将目前的函数"<code>unwind</code>"掉；最后进行到程序堆栈的下一个函数中去，重复操作2~4。
   * 当一个<code>catch</code>子句捕获到一个异常时：
       * 如果<code>catch</code>是以<code>object</code>方式捕获的，就会发生<code>copy</code>动作，在<code>catch</code>子句结束时，这个用以捕获异常的临时对象会被销毁掉。此时如果发生<code>throw</code>操作，则是参考真正的<code>exception object</code>。
       * 如果<code>catch</code>是以<code>reference</code>方式捕获的，任何对其做的改变，都会随着再次的<code>throw</code>操作被繁殖到下一个<code>catch</code>子句中。

>**执行期类型识别**<br/>

   * 欲支持<code>type-safe downcast</code>的额外负担：
       * 需要额外的空间以存储类型信息，通常是一个指针，指向某个类型信息结点。
       * 需要额外的时间以决定执行期的类型，因为这需要在执行期才能决定。
   * <code>Type-safe dynamic cast</code>：
       * C++的<code>dynamic_cast</code>运算符可以在执行期决定真正的类型，如果<code>downcast</code>是安全的，这个运算符会传回适当的转换过的指针；如果是不安全的，这个运算符会传回0。
       * 这种动态转换的真正成本是：一个<code>type_info</code>会被编译器产生出来，其地址被放在<code>virtual table</code>的第一个<code>slot</code>内。而在执行期需要转换时，需要由<code>object</code>的<code>vptr</code>指针简介取得相应的<code>type_info object</code>，才能保证安全转换。
       * 当<code>dynamic_cast</code>运算符用于<code>reference</code>时：如果<code>reference</code>真正参考到适当的<code>derived class</code>，<code>downcast</code>会被执行而程序可以继续运行；否则，由于不能传回0，因此抛出一个<code>bad_cast exception</code>。
   * <code>Typeid</code>运算符：
       * C++的<code>typeid</code>运算符传回一个类型为<code>type_info</code>的<code>const reference</code>，该<code>class</code>定义了判断相等与否的<code>equality</code>运算符。
       * 事实上，<code>type_info</code>除过适用于多态类之外，也适用于内建类型以及非多态的使用者自定类型。区别在于，后者的<code>type_info object</code>是静态取得，而非执行期取得。
       * 使用<code>typeid</code>运算符，就可以配合<code>static_cast</code>产生跟<code>dynamic_cast</code>一样的效果。
