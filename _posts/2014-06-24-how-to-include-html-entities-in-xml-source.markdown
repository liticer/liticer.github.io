---
layout: post
title:  "How to include HTML entities in XML source"
date:   2014-06-24
tags: xml atom jekyll
comments: true
archive: true
---
In my attemp to build an RSS feed for this blog, I run a problem. Some html entities (without some help) could not be parsed in XML. This was the error generated

```
 error on line # at column #: Entity 'mdash' not defined
```

I guess it must have been complaining about lines in my posts such as

```
"The Journey &mdash; Book one complete"
```

which under normal circumstances should render as

```
The Journey — Book one complete
```

Thanks to this [Stackoverflow](http://stackoverflow.com/questions/2729478/leave-entity-intact-in-xml-xslt) answer I overcame this problem by adding only this line to my XML

```
<!DOCTYPE xsl:stylesheet [<!ENTITY mdash "&#x2014;">]>
```
Have a look at my template
<script src="https://gist.github.com/nadjetey/95d9596405316f9885b4.js"></script>

More Vimm!
