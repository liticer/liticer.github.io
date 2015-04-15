---
layout: post
title:  "KMP算法详解"
date:  2015-04-15
comments: true
tags: KMP 算法详解 字符串匹配
archive: false
---


KMP算法是一种改进的字符串匹配算法，由D.E.Knuth、V.R.Pratt和J.H.Morris三人提出。KMP算法的关键是利用匹配失败后的信息，尽量减少模式串与主串的匹配次数以达到快速匹配的目的。以下将分三个部分对KMP算法进行阐述。

<strong> 一. 暴力字符串匹配算法</strong>

假设现在我们面临这样一个问题：有一个文本串S，一个模式串P，现在要在SS中查找P出现的位置，该怎么查找呢？

我们会很自然第想到一种暴力破解的方法，算法具体如下：
假设有两个索引i=0和j=0，分别指到文本串S的第i个字符和模式串P的第j个字符，则有：

* 如果当前字符匹配成功(即S[i]==P[j])，则i++，j++，继续匹配下一个字符；
* 如果当前字符匹配失败(即S[i]!=P[j])，令i=i-j+1，j=0。相当于每次匹配失败时，i回溯，j被置为0。

算法比较简单，用C++实现如下：

```c++
int ViolentCharMatch(string s, string p) {
	
	int sLen = s.size();
	int pLen = p.size();

	int i = 0;
	int j = 0;

	while (i < sLen && j < pLen) {
		if (s[i] == p[j]) {
			i++;
			j++;
		} else {
			i = i - j + 1;
			j = 0;
		}
	}

	if (j == pLen) {
		return i - j;
	} else {
		return -1;
	}

}
```

算法流程比较清晰：对于文本串S的每个字符开始的子串依次与P进行匹配，如果匹配成功则结束；否则，跳到下一个字符开始的子串继续进行匹配。在匹配过程中，S的索引i会发生回溯，P的索引j会发生重置。KMP算法主要思想就是利用了P的索引回溯的过程，使得S的索引i不再发生回溯，从而减少了字符串匹配的复杂度。

<strong> 二. KMP字符串匹配算法</strong> 

KMP算法的核心思想是当字符串S与模式串P进行匹配时，适当地移动j以保持i一直向前移动。要做到这样，首先必须定义一个长度与P的长度相等的next向量，next[j]表示S[i]!=P[j]时，P的索引j应该回溯的位置。首先贴出KMP算法的C++实现代码，然后对照代码对算法进行分析。

1.KMP算法的C++实现如下：

```C++
#主调函数KMPCharSearch
int KMPCharSearch(string s, string p) {
	
	const int sLen = s.size();
	const int pLen = p.size();
	int next[pLen];
	getNext(p, next);

	int i = 0;
	int j = 0;

	while (i < sLen && j < pLen) {
		if (j == -1 || s[i] == p[j]) {
			i++;
			j++;
		} else {
			j = next[j];
		}
	}
	
	if (j == pLen) {
		return i - j;
	} else {
		return -1;
	}		
}
```

```C++
#KMP算法的next向量计算getNext
int getNext(string p, int next[]) {
	
	int pLen = p.size();
	
	next[0] = -1;
	int k = -1;
	int j = 0;

	while (j < pLen) {
		if (k == -1 || p[k] == p[j]) {
			k++;
			j++;
			next[j] = k;
		} else {
			k = next[k];
		}
	}

}

```

2.
