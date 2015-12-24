---
layout: post
title: Excel使用笔记
description: Excel软件使用的一些笔记，以备查用。
categories: Excel
tags: Tutorial

---

<p style="font-size:25px;color:blue;text-align:center;padding:20px 0">第1篇  快捷键</p>

1.<font color="red">Esc键:</font>

&ensp;&ensp;&ensp;&ensp;修改单元格时如果不小心更改公式的构成，可以用Esc键退出，避免破坏了公式

2.<font color="red">鼠标快速移动：</font> 

   * Home移动到该单元格所在行行首
   * Ctrl+Home移动到工作表的第一行第一列
   * Ctrl+End移动到工作表的最后一行最后一列
   * Ctrl+上键移动到该单元格所在列列首，Ctrl+下键移动到该单元格所在列列尾
   * Ctrl+左键移动到该单元格所在行行首，Ctrl+右键移动到该单元格所在行行尾
   
3.<font color="red">Alt+分号键：</font>

   * 快速删除不连续的多行数据：
      * 筛选得到要删除的行---->全部选中这些行---->按Alt+分号键---->按Ctrl+减号键删除行
   * 快速复制不连续的多行数据：
      * 筛选得到要复制的行---->全部选中这些行---->按Alt+分号键---->按Ctrl+C键复制数据
   * 快速将公式应用到不连续的多行数据：
      * 筛选得到要应用公式的行---->在首行编辑公式---->按Ctrl+V键复制首行---->选中除首行外要应用公式的所有行---->按Alt+分号键---->按Ctrl+V键粘贴公式
   


<p style="font-size:25px;color:blue;text-align:center;padding:20px 0">第2篇  函数</p>
	   
1.<font color="red">条件求和：</font> 
  
&ensp;&ensp;&ensp;&ensp;=SUMIF(B2:B56, "男", K2:K56)
	   
2.<font color="red">查找重复内容公式：</font> 
 
&ensp;&ensp;&ensp;&ensp;=IF(COUNTIF($A$2:$A$56, A2)>1, "重复", " ")
	   
3.<font color="red">用出生年月来计算年龄公式：</font> 
 
&ensp;&ensp;&ensp;&ensp;=TRUNC((DAYS360(A2, "2015/8/30", FALSE))/360)

4.<font color="red">计算日期差：</font> 

&ensp;&ensp;&ensp;&ensp;DATEDIF(start_date,end_date,unit)

5.<font color="red">计算单元格地址：</font> 

&ensp;&ensp;&ensp;&ensp;=ADDRESSS(row_num,column_num,abs_num,a1,sheet_text)

6.<font color="red">间接引用：</font> 

&ensp;&ensp;&ensp;&ensp;=INDRECT(ref_txt), 有两种使用方式：

* =INDIRECT("A1")——加引号，文本引用——即引用A1单元格所在的文本(B2)。
* =INDIRECT(A1)——不加引号，地址引用——因为A1的值为B2，B2=11，所以返回11。




<p style="font-size:25px;color:blue;text-align:center;padding:20px 0">第3篇  技巧</p>


1.<font color="red">快速选中一行或一列：</font> 
 
* 先将鼠标移动到行首或列首：可以使用“Ctrl+方向键”快速移动
* 再使用“Ctrl+Shift+下键”选中一行或者使用“Ctrl+Shift+右键”选中一列
	   
2.<font color="red">快速插入一行或一列：</font> 
 
* 先用鼠标选中要插入的行的下一行或者要插入的列的右一列：可以使用技巧篇中1的快捷键选中
* 再用“Ctrl+Shift+加键”插入一行或一列
	   
3.<font color="red">删除一行或一列：</font> 
 
* 先用鼠标选中要删除的行或列：可以使用技巧篇中1的快捷键选中         
* 再用“Ctrl+减键”删除一行或一列
	   
4.<font color="red">快速选中一个区域：</font> 
 
* 先选中该区域中左上角的单元格或者右下角的单元格
* 按住“Shift键”，再选中该区域中右下角的单元格或者左上角的单元格
	   
5.<font color="red">删除一张工作表中重复的行：</font> 
 
* 先选中包含重复值的行：可以用技巧篇中4的快捷键选中
* 依次点击“数据---->删除重复项---->选择作为键值的列名---->确定”
	   
6.<font color="red">如何将公式快速应用到一列：</font> 
 
* 在该列最开始一格编辑好公式并应用
* 选中该单元格并双击填充柄将公式应用到一整列 
	   
7.<font color="red">找出一张工作表中重复的行：</font> 
 
* 公式：=IF(COUNTIF($A$2:$A$456,A2)>1, "重复", 0)       
* 在第三列去进行筛选，选择值为重复的列
	   
8.<font color="red">找出两张工作表中不一样的行：</font> 
 
* 有两张表查找表1和查找表2:
                                      
&ensp;&ensp;&ensp;&ensp;&ensp;![pseudo](/assets/image/10-1.png "查找表1")&ensp;&ensp;&ensp;&ensp;![pseudo](/assets/image/10-2.png "查找表2")

* 用两张表中所有的人员工号连接表1：

&ensp;&ensp;&ensp;&ensp;&ensp;![pseudo](/assets/image/10-3.png)
         
* 用两张表中所有的人员工号连接表2：

&ensp;&ensp;&ensp;&ensp;&ensp;![pseudo](/assets/image/10-4.png)         
         
* 连接结果相减，N/A的表示该工号对应的数据在其中一张表中不存在，不为0的数据表示该工号对应的数据在两张表中都存在但是数值不一样：

&ensp;&ensp;&ensp;&ensp;&ensp;![pseudo](/assets/image/10-5.png)   

9.<font color="red">使用文本为公式的地址参数：</font> 

* 先使用ADDRESS函数得到单元格地址，形如A1/$A$1/A$1/$A$1
* 再将上述地址文本作为参数，传递给INDRECT函数
* 就可以将INDRECT函数返回值作为参数，来传递给其它需要地址参数的公式

&ensp;&ensp;&ensp;&ensp;举例如下，要为每个人计算月均工资：

&ensp;&ensp;&ensp;&ensp;&ensp;![pseudo](/assets/image/10-6.png)  

10.<font color="red">双向查找：</font> 

&ensp;&ensp;&ensp;&ensp;查找某个人某个月份的工资：

&ensp;&ensp;&ensp;&ensp;&ensp;![pseudo](/assets/image/10-7.png) 
         

