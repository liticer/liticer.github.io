---
layout: post
title: 深度探索C++对象模型学习笔记
description: 阅读侯捷老师翻译的Lippman大作《Inside the C++ Object Mode》过程中，在自己理解和体会的基础上做了一些笔记。
categories: CPP
tags: Object Model

---

<p style="font-size:25px;color:blue;text-align:center;padding:20px 0">第1章 关于对象</p>

1.&ensp;C++对象的布局成本<br/>

   * C++中单纯地使用封装和继承，并不会增加存取时间和存储空间上的成本。
   * C++真正需要的额外成本是由Virtual引起的(包括Virtual function和Virtual base class)。

2.&ensp;C++对象模型<br/>

  * 数据成员：
    * Nonstatic data members被配置于每一个class object之内；Static data members被存放在个别的class object之外。
  * 非虚函数成员：
    * Nostatic/Static function members均被置于个别的class object 之外，同一般的非成员函数处理机制类似。
  * 虚函数成员：
    * 每一个class产生出一堆指向virtual functions的指针，存放在一个叫做virtual table(vtbl)的表格之中。通常一个class所关联的type_info object被存放在该表格的第一个slot中。
    * 每一个class object被安插一个叫做virtual pointer(vptr)的指针，指向相关的virtual table。通常vptr会被每一个class的constructor，destructor和copy assignment等函数自动地进行设定和重置。


<p style="font-size:25px;color:blue;text-align:center;padding:20px 0">第2章 构造函数语意学</p>

1.&ensp;Default Constructor的构造操作<br/>

&ensp;&ensp;&ensp;&ensp;对于一个类，如果没有任何user-declared constructor，那么在编译器有需要的时候，会为它合成一个nontrival default constructor。通常，有如下4种情况需要合成copy constructor：

  * 该class有"带Default Constructor"的Data member
    * 需要在构造函数中调用该Data member的默认构造函数初始化该成员。
  * 该class有"带Default Constructor"的Base class
    * 需要在构造函数中调用Base class的默认构造函数初始化Base class subobject。
  * 该class有"Virtual Function"
    * 需要在构造函数中生成或维护vtbl，并设置或修改vptr。
  * 该class有"Virtual base class"
    * 需要在构造函数中维护vtbl和vptr，保证virtual base class在每一个derived class object中的位置在执行期准备妥当。

&ensp;&ensp;&ensp;&ensp;至于没有存在上述4种情况且没有声明任何constructor的class，我们说它拥有的是implicit trivial default constructor，它们实际上不会被合成出来。

&ensp;&ensp;&ensp;&ensp;C++新手一般有两个常见的误解：
(1)任何class，如果没有定义default constructor，就会被合成出来一个。
(2)编译器默认合成出来的default constructor会显式地设定“class内每一个data member的默认值”。


2.&ensp;Copy Constructor的构造操作<br/>

&ensp;&ensp;&ensp;&ensp;调用Copy constructor三种情况分别是：初始化，传参和返回值。和default construtor一样，copy constructor也分为trivial和nontrivial两种，只有nontrivial的class才会合成它。倘若一个class展现出所谓的"bitwise copy semantics"，那么它的copy constructor就是trivival的。一个class不展现出"bitwise copy semantics"的4种情况如下：<br/>

  * 当class内含有一个member object，而后者的class声明有一个copy constructor时(不论是被class设计者显式声明，还是被编译器合成都算)，该class的copy constructor需要调用该member object的copy constructor完成该成员的拷贝构造。
  * 当class继承自一个base class，而后者存在一个显式声明的copy constructor时，该class的copy constructor需要调用base class的copy constructor完成base class subobject的拷贝构造。
  * 当class声明了一个或多个virtual functions时，该class的copy constructor需要维护vptr指针，保证其指向对应的class的vtbl。
  * 当class派生于一个继承串链，其中有一个或多个virtual base classes时，该class的copy constructor需要拷贝构造virtual base subobject，同时维护vptr指针确保其指向对应的class的vtbl。


3.&ensp;程序转化语意学<br/>

  * 参数初始化：在非引用参数传入之前，可能会先创建一个临时变量存储参数。然后在调用函数时以引用方式传入这个临时变量，当然函数的声明也会做相应的修改。
  * 返回值初始化：如果函数的返回值不是引用变量，会在函数调用前创建一个临时变量存储返回值。然后在调用函数时以引用方式传入这个临时变量，当然函数的声明也会作相应的修改。
  * 使用者层面的优化：如果函数的返回值不是引用变量，则在函数return时创建临时变量比在函数开始处创建临时变量要好，有可能会减少一次copy constructor的调用。如果不懂，可以联系上一条结论理解。
  * 编译器层面的优化：如果函数中所有return指令传回相同的变量，编译器有可能会以返回值result参数取代named return value， 这个过程也被叫做NRV优化。
  * Copy constructor的取舍：当class的default copy constructor被时为trivial的时候，一般情况下不需要为其提供emplicit的copy constructor。然而如果class需要大量的memberwise的初始化操作，那么就可以给它提供一个copy constructor；一方面结合编译器作NRV优化，另一方面可以用memcpy函数提高拷贝效率。


4.&ensp;成员初始化<br/>

  * Member initialization list必需的情况：初始化一个reference member；初始化一个const member；初始化member object时需要调用含参构造函数；初始化base class时需要调用含参构造函数。
  * Member initialization list的初始化顺序：一个object的构造总是先构造其base subobject部分，而member的初始化总是要按顺序被安插在任何explicit user code之前。在每一个constrctor中的member初始化时，需要先调用base class的constructor，然后在按成员在class中的顺序逐一初始化各个成员，最后执行explicit user code
。
  * 初始化的一些特殊情况：以member function的结果初始化member；以member function的结果作为base class constructor的参数。Member function的调用是合法的，因为在object相关的this指针在构建时已经准备妥当，但还是要尽量避免上述情况。具体原因时，构造函数调用前，object的data member有可能还未被全部初始化；而在调用构造base class subobject时，通过this指针调用虚函数时将有可能发生异常的动态绑定过程。

<p style="font-size:25px;color:blue;text-align:center;padding:20px 0">第3章 Data语意学</p>

1.&ensp;Data member的绑定<br/>
&ensp;&ensp;&ensp;&ensp;编译器对于一个inline member function的本体的分析，会在整个class的声明都出现了才开始；然而对于member function的argument list，则是在它们第一次出现时被适当地进行决议完成的。因此上，在现代C++程序设计中，需要将"nested type声明"放在class的起始处，这是一种安全的防御性程序设计风格。

2.&ensp;Data member的布局<br/>
&ensp;&ensp;&ensp;&ensp;C++ Standard要求，在同一个access session中，较晚出现的members在class object中有较高的地址。同时，编译器还可能会合成一些内部使用的data member(如vptr),传统上它们通常被放在所有显式声明的members之前或者之后。

3.&ensp;Data member的存取<br/>

   * Static data members对每个class来说只有一个实例，存放在从class之外的data segment中，并被视为一个global变量；不论通过实例访问，还是通过类名访问，都会在内部被转化成类名的访问形式。

   * Nonstatic data members直接存放在每一个object当中。每一个nonstatic data member的偏移位置在编译时期即可获知，因此存取一个nonstatic data member的效率和存取一个C struct member的效率是一样的。唯一的例外是，当使用指针或引用访问member时，该指针或引用指向的class的继承结构中有一个virtual base class，且该member是从该virtual base class继承而来的。这种情况下，因为不知道该指针或引用指向哪一种class type，因此存取操作必须延迟至执行期，经由一个额外的间接引导才能解决。

4.&ensp;继承与data member<br/>
   
   * 单一继承不含virtual functions：
      * 一个object由两部分构成，base class subobject和本身的data members。这种情况下并不会增加空间或者时间上的额外负担。
   * 单一继承且含virtual functions：
      * 为每一个class导入一个virtual table，用来存放它所声明的每一个virtual function的地址。
      * 在每一个class object种导入一个vptr，提供执行期的链接，使每一个object都能找到相应的virtual table。对base class来说，vptr在object中的位置通常在所有data members之后；而derived class object会继承base class的vptr，不用单独再留存储空间。
      * 加强constructor，使它能够为vptr设定初值，让它指向class所对应的virtual table。这可能意味者在derived class和每一个base class的constructor中，会重新设定vptr的值。
      * 加强destructor，使它能够矫正vptr，让它指向class所对应的virtual table。因为，vptr很可能已经在derived class destructor中被设定为derived class的virtual table的地址了。
   * 多重继承：
      * 对于多重继承来说，一个derived class object由几部分组成：base class1 subobject， base class2 subobject， ..., data members。在这种情况下，把一个derived object转换为其base类型，就需要编译器的介入，用以调整地址。
      * 多重继承的情况下，如果一个derived class object有vptr，那么其vptr就存放在其继承列表中第一个含有vptr的subobject的vptr处，否则在data members之后新增一个vptr域。
   * 虚拟继承：
      * 对于虚拟继承来说，它跟多重继承的情况类似。只是它需要指出shared base subobject的偏移位置，而这个偏移量通常会被放置在virtual table最前面的slot中。在将derived object赋值给base object时，需要通过virtual table查找这个偏移量，并进行复制构造。
      * 当通过object来存取一个从virtual base class的member，可以被优化成一个直接存取操作；然而通过指针或引用来访问上述member时，就需要在执行期通过查找virtual table中的offset，经过两次间接引导才能访问到。因此上，virtual base class最有效的一种运用形式就是：一个抽象的virtual base class，没有任何的data member。

5.&ensp;指向data members的指针<br/>

   * 对class的nonstatic member取地址得到的是一个偏移值，表示该member在class中的偏移位置，可以将该值赋给一个指向该class的data member的指针；而对object的nonstatic member取地址得到的是一个地址值，表示该object中的data member的地址，可以将该值赋给一个指向该member类型的指针。
   * 对class或者object中的static member取地址得到的是一个地址值，表示该class中static member的在内存中的位置，可以将该值赋给一个指向该member类型的指针。
   * 为了区分一个"没有指向任何data member的指针"和"一个指向第一个data member的指针",每一个真正的member offset值都会被加上1，而在使用该offset取值之前，需要减掉1。


<p style="font-size:25px;color:blue;text-align:center;padding:20px 0">第4章 Function语意学</p>

1.&ensp;Member function的各种调用方式<br/>
   
   * Nonstatic member functions：
      * C++的设计准则之一就是：nonstatic member function至少必须和一般的nonmember function有相同的效率。
      * 在编译器内部，会将member function实例转换为对等的nonmember function实例。通常member function的函数名称会被"mangling"为程序中独一无二的名称，其函数原型会被安插一个额外的this指针参数，其"对nonstatic data member的存取操作"会被改写成通过this指针的存取操作。
   
   * Virtual member functions：
      * 如果通过指针或引用去访问一个virtual member function，将在编译器内部被转换为通过查询virtual table进行访问的形式。
      * 如果通过object取访问一个virtual member function，其在编译器内部的转换方式跟nonstatic member function相同。
   
   * Static member functions：
      * 无论通过何种形式访问一个static member function，总是会被转化一个对对等的nonmember function的访问形式。通常static member function的函数名称会被"mangling"为程序中独一无二的名字。
      * Static member functions的主要特性就是它没有this指针。因此上，它不可以访问class中的nonstatic members，也不能够被声明为const，volatile或virtual。

2.&ensp;Virtual member functions<br/>
   
   * 单一继承下的virtual functions：
      * 含有virtual functions的单一继承下，一个class只会有一个virtual table，每一个table中含有该从class的类型信息和对应class object中所有active virtual functions函数实例的地址。其中的active virtual functions包括继承自base class的virtual functions，重写的base class的virtual functions，自己定义的virtual functions。
      * 含有virtual functions的单一继承下，一个class object中会被安插一个指向该class virtual table的指针。为了找到函数地址，编译器会为每一个virtual function指派一个表格索引值。
  
   * 多重继承下的virtual functions：
      * 含有virtual functions的多重继承下，一个derived class内含有n个virtual tables，n表示其上一层的base class的个数。其中包含1个主要实例(由derived class于base1 class共享),n-1个次要实例(除base1 class之外的每个base class各享一个).针对每一个virtual table，derived对象中都有一个对应的vptr，需要在构造，复制，析构时进行适当的维护。为了调节执行期链接器的效率，编译器或许会将多个virtual tables连锁为一个，指向次要表格的指针，可以主要表格名称加上一个offset获得。
      * 在多重继承中支持virtual functions，其复杂度围绕在第二个及后继的base  class身上，以及必须在执行期调整this指针这一点上。具体地有三种情况，第二或后继的base class会影响对virtual function的支持:(1) 通过一个指向"第二个base class或后继"的指针，调用derived class virtual function;(2) 通过一个指向"derived class"的指针，调用第二个base class或后继中继承而来的virtual function;(3)允许一个virtual function的返回值类型有所变化，可能时base type，也可能时derived type。

   * 虚拟继承下的virtual functions：
      * 含有virtual functions的虚拟继承下，编译器会在生成virtual table的时，在table的首部加入一个额外的slot(索引为-1),指出virtual base的偏移量。
      * 强烈建议，不要在一个virtual base class中声明nonstatic data members，只将它作为一个接口使用即可。


3.&ensp;指向member function的指针<br/>
  
   * Nonvirtual member function指针：对一个nonstatic member function取地址得到的是一个带有相同参数+额外参数(this指针)的普通函数指针；而对一个static member function取地址得到的是一个相同参数的普通函数指针。
   * Virtual member function指针：
      * 对一个单一继承下的virtual member function取地址得到的它在virtual table中的索引值；对一个多重继承下的virtual member function取地址得到的是一个结构体，除了反应virtual table索引值之外，还要反应this指针的offset值。

4.&ensp;Inline functions<br/>
  
   * 定义在类内的函数，隐式为内联的；在类外声明的内联函数，须加inline声明。并非所有的inline声明都会变成inline函数，代码过多的话，编译器可能会拒绝，转而将它作为普通函数。
   * 内联函数的形参：传入参数，直接替换为参数名；传入常量，直接替换为常量值；传入函数运行结果，则需要导入临时变量。
   * 内联函数的局部变量：局部变量会被"mangling",以便inline函数被替换后局部变量名字唯一。也就是说，一次性调用N次，就会出现N个临时变量，程序体积会暴增。总之，inline的使用要小心处理。

<p style="font-size:25px;color:blue;text-align:center;padding:20px 0">第5章 构造，析构，拷贝语意学</p>
  
1.&ensp;关于纯虚函数<br/>
   
&ensp;&ensp;&ensp;&ensp; 原则上允许定义和调用一个pure virtual function。不过它只能被静态调用(即通过类名调用),不能经由虚拟机制调用(即通过指针或引用调用).不过pure virtual destructor必须被定义，因为每一个derived class destructor都会被编译器加以扩张，以静态方式调用其"每一个virtual base class"和"上一层base class"的destructor。所以一个比较好的替代方案是，不要把virtual destructor声明为pure。

2.&ensp;无继承情况下的对象构造<br/>
  
   * Plain OI Data声明形式：在这种情况下，该类的constructor和destructor被视为trival的，不是没被定义就是没被调用。此时的copy assignment operator会直接进行像C那样的纯粹位搬移操作。
   * Abstract Data Type声明形式：在这种情况下，该类的表现与上一种情况类似。简单的封装并没有给C++带来任何额外的负担。
   * 含有virtual function的情况：在这种情况下，destructor仍然是trival的，而constrcutor和copy operator不再是trival的了。因为virtual functions的出现，使得每一个object含有一个vptr，所以constructor，copy constructor和copy operator都需要被编译器安插代码初始化object的vptr指针。

3.&ensp;继承体系下的对象构造<br/>
   
&ensp;&ensp;&ensp;&ensp;继承体系下constructor的扩充步骤： 

   * 如果有，调用所有的virtual base class constructors，从左到右，从深到浅。
       * 如果class被列于member initialization list中，那么任何显式指定的参数都应该被传递过去；否则，调用class的default constructor，如果没有，就报错。
       * 此外，class中的每一个virtual base class subobject的偏移位置必须在执行期可被存取，以便在进行上述操作时移动this指针。
       * 如果class object时最底层的class，其constructors可能被调用。用以支持这一行为的机制必须被放进来。
   * 如果有，调用上一层的base class constructors，以base class的声明顺序为顺序。
       * 如果class被列于member initialization list中，那么任何显式指定的参数都应该被传递过去；否则，调用class的default constructor，如果没有，就报错。
       * 如果base class是多重继承下的第二或后继的base class，必须根据情况调整this指针以指向正确的位置。
   * 如果有，指定vptr的初值，以便指向正确的virtual table。
   * 如果有，如果类中有member出现在member initialization list或者含有一个default constructor，按照它们在类中被声明的顺序依次进行初始化。
   * 如果有，执行用户显式指定的代码部分，即构造函数的显式函数体。

&ensp;&ensp;&ensp;&ensp;继承体系下构造过程中需要注意的地方： 

   * 虚拟继承下的virtual base class构造：这种情况下，virtual base subobject的构造总是由继承链中最底层的class来否则。因此需要在构造函数中额外加入一个参数，指示该class是否为most_derived，如果是，则构造，否则，就跳过。
   * 继承体系下对象的构造过程：令每一个base class constructor设定其对象的vptr，使它指向相关的virtual table，构造中的对象就可以严格而正确地变成"构造过程中所幻化出来的每一个class"的对象。也即是说，一个PVertex对象会先形成一个Point对象，一个Point3d对象，一个Vertex对象，一个Vertex3d对象，然后才成为一个PVertex对象。
   * 在一个class的constructor的member initilization list中调用该class的一个虚函数，用其返回值作为member初始化的参数：在原则是安全的，因为vptr保证能够在member initilization list被扩展之前，由编译器正确设定好；在语意上是不安全的，因为该虚函数本身可能依赖于尚未被设定初值的members，这种做法并不推荐。
   * 在一个class的constructor的member initilization list中调用class的一个虚函数，用其返回值作为base class constructor的参数：这种做法是不安全的，因为此时vptr若不是未被设定好，就是指向错误的class，这种情况绝对不允许。    

4.&ensp;对象复制语义学<br/>
   
   * Copy operator的工作：一个copy operator会在需要的情况下被编译器合成出来，然而当该合成的函数不能满足需要时，我们需要自己定义它。一般地，一个copy operator需要负责复制自身的成员，并调用base class的copy operator来copy base subobject。
   * 虚拟继承下的copy operator：这种情况下，由于不能抑制Base class中对shared virtual base subobject的copy动作，因此上会发生shared virtual base subobject的多重拷贝过程。建议做法是尽可能不要允许一个virtual base class的拷贝操作，甚至不要再任何virtual base class中声明数据。

5.&ensp;析构语义学<br/>
   
&ensp;&ensp;&ensp;&ensp;一个由程序员定义的destructor被扩展的方式类似constructor被扩展的方式，但是顺序相反：
   
   * 如果有，重设该object的vptr指针，指向相关的virtual table。 
   * 如果有，destructor的函数本体被执行，即用户定义的相关操作。
   * 如果有，按照成员在class中被声明的顺序的相反顺序，调用member class objects的destructor。
   * 如果有，按照base class声明顺序的相反顺序，调用任何直接的nonvirtual base classes的destructor。
   * 如果有，假如讨论的是类是most-derived的，按照virtual base classes被声明的顺序的相反顺序，调用其destructor。


<p style="font-size:25px;color:blue;text-align:center;padding:20px 0">第6章 执行期语意学</p>

1.&ensp;对象的构造和析构<br/>

   * 全局对象：
      * Global object在程序编译时期可以被放置于data segment中并且内容为0，但object的constructor的调用一直到程序启动时才会被执行。因此上，一个含有constructor和destructor的global object需要静态初始化操作和内存释放操作。
      * 静态初始化操作通常会被统一集中起来放在main函数首部执行，而内存释放操作则会被统一集中起来放在main函数尾部执行。一个良好的建议就是不要用那些需要静态初始化的global objects。
   * 局部静态对象：
      * 局部静态对象也是存放在data segment当中，在所属函数首次被调用时进行初始化，在main函数尾部与全局对象一起进行内存释放。
   * 对象数组：
      * 如果class不含有constructor和destructor，则所需要做的工作和一个内建类型数组一样多；否则，需要在定义时调用一个类似vec_new的函数，将constructor施行于各个元素身上，在释放时需要调用一个类似vec_delete的函数，将destructor施行于各个元素身上。
      * 如果class含有一个以上的形式参数，且每个参数都含有默认值，那么它也可以作为数组的元素类型。编译器可能会构建一个不含参的stub constructor，在函数内调用class的constructor，并将默认参数显式地传递过去。

2.&ensp;new和delete运算符<br/>
      
   * 运算符new的操作事实上是通过两个步骤完成的：先通过适当的new运算符函数实例，配置所需的内存；再为配置得来的对象调用constructor设定初值。运算符delete的操作也是类似：先调用对象的destructor析构对象；再释放掉对象所占用的内存。(注：前提是object有constructor和destructor，否则不用调用)
   * 针对数组的new跟delete：如果class含有constructor和destructor，需要在定义时调用一个类似vec_new的函数，先为对象配置内存，再将constructor施行于各个元素之上；在释放时需要调用一个类似vec_delete的函数，先将destructor施行于各个元素之上，再释放对象所占用的内存。
   * Placement operator new的语意：其语意是在指定的内存位置上，调用constructor构造一个对应class的对象。而这个内存位置应该是预先已经开辟出来的：或者是该内存地址上的对象被析构而内存没有被释放；或者是一块刚开辟出来的未作任何处理的内存块。

3.&ensp;临时性对象<br/>
  
   * 临时性对象的摧毁时机：临时性对象的被摧毁，应该是对完整表达式求值过程中的最后一个步骤，该完整表达式造成临时对象的产生。
   * 临时性对象的生命规则有两个例外：第一个例外发生在表达式被用来初始化一个object时，临时对象应该存留到object的初始化操作完成为止，如用一个问号表达式的结果初始化一个string对象；第二个例外是当一个临时性对象被一个reference绑定时，临时对象将残留到reference的生命结束或者临时对象的生命范畴结束，如将一个string对象绑定到一个字符串上。

<p style="font-size:25px;color:blue;text-align:center;padding:20px 0">第7章 站在对象模型的尖端</p>

1.&ensp;Template<br/>
 
   * 实例化：一个template会在定义了该template一个实例对象时，进行相应的实例化，以便产生该实例对象的真正布局形式。然而该实例的member functions只有在被使用的时候才要求它们被实例化。(其主要原因是：空间和时间效率的考虑；尚未实现的机能)
   * 名称决议法：一个编译器必须保持两个scope contexts："scope of the template declaration"用以专注于一般的template class；"scope of the template instantiation"用以专注于特定的实例。
   * Member Function的实例化行为：
       * 编译器如何找出函数的定义？包含template program text file，就好像它是一个头文件一样；要求一个文件命名规则，如Point.h的声明，其定义必被放在Point.C/Point.cpp中。
       * 编译器如何只实例化程序中用到的member functions？忽略这项要求，把一个已经实例化的class的所有member functions都产生出来；模拟链接操作，检测哪一个函数真正需要，只为它们产生实例。
       * 编译器怎么组织member definitions在多个.o文件中都被实例化？产生多个实例，然后从链接器中提供支持，只留下其中一个实例，其余都忽略；另一个方法就是由使用者来引导"模拟链接阶段"的实例化策略，决定哪些实例才是需求的。

2.&ensp;异常处理<br/>

   * 当一个exception发生时，编译系统必须完成以下事情：
       * 检验发生throw操作的函数。
       * 决定throw操作是否发生才try区段中。如果是，跳到3，否则，跳到4。
       * 把exception type拿来和每一个catch子句进行比较。如果比较吻合，就将控制流程交到catch子句手上；否则跳到4。
       * 首先摧毁所有的active local objects；然后从堆栈中将目前的函数"unwind"掉；最后进行到程序堆栈的下一个函数中去，重复操作2~4。
   * 当一个catch子句捕获到一个异常时：
       * 如果catch是以object方式捕获的，就会发生copy动作，在catch子句结束时，这个用以捕获异常的临时对象会被销毁掉。此时如果发生throw操作，则是参考真正的exception object。
       * 如果catch是以reference方式捕获的，任何对其做的改变，都会随着再次的throw操作被繁殖到下一个catch子句中。

3.&ensp;执行期类型识别<br/>

   * 欲支持type-safe downcast的额外负担：
       * 需要额外的空间以存储类型信息，通常是一个指针，指向某个类型信息结点。
       * 需要额外的时间以决定执行期的类型，因为这需要在执行期才能决定。
   * Type-safe dynamic cast：
       * C++的dynamic_cast运算符可以在执行期决定真正的类型，如果downcast是安全的，这个运算符会传回适当的转换过的指针；如果是不安全的，这个运算符会传回0。
       * 这种动态转换的真正成本是：一个type_info会被编译器产生出来，其地址被放在virtual table的第一个slot内。而在执行期需要转换时，需要由object的vptr指针简介取得相应的type_info object，才能保证安全转换。
       * 当dynamic_cast运算符用于reference时：如果reference真正参考到适当的derived class，downcast会被执行而程序可以继续运行；否则，由于不能传回0，因此抛出一个bad_cast exception。
   * Typeid运算符：
       * C++的typeid运算符传回一个类型为type_info的const reference，该class定义了判断相等与否的equality运算符。
       * 事实上，type_info除过适用于多态类之外，也适用于内建类型以及非多态的使用者自定类型。区别在于，后者的type_info object是静态取得，而非执行期取得。
       * 使用typeid运算符，就可以配合static_cast产生跟dynamic_cast一样的效果。
