---
layout: post
title:  "Google grid gallery"
date:   2014-05-14
tags: google-grid-gallery image-gallery gallery google jekyll jekyll-theme
comments: true
archive: true
---
_This post has been updated!_

A responsive image grid gallery based on the [Google Chromebook getting started](https://gweb-gettingstartedguide.appspot.com/) guide gallery ported to Jekyll.

This is an [experiment](http://tympanus.net/Blueprints/GridGallery/) by [@crnacura](https://twitter.com/crnacura) ported to Jekyll.

### How to use (local deployment)
+ [Download](https://github.com/nadjetey/GridGallery/archive/master.zip) & extract package
+ Use the normal process of serving a jekyll site. [More details](http://jekyllrb.com/)
+ Put image in ``/img/large`` and a thumnail version with the same file name in ``/img/thumb``
+ Follow this sample front-matter

```yaml
---
layout: default
date:   2014-04-06 23:26:12
photo: 1.png
caption_header: Sample header
caption: sample caption
---
```
+ Run jekyll commands to serve site

### Screenshot
![screenshot]({{ site.url }}/assets/images/g_grid_gal.png)

### Contact
You are welcome to [fork](https://github.com/nadjetey/GridGallery/fork) this repository. Do contact [me](https://twitter.com/_nadjetey) in case of any issues or questions.

More Vimm!