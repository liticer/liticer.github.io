---
layout: post
title:  "How to deploy Jekyll 2.1.1 on Github server"
date:   2014-10-23
tags: jekyll_2.1.1 github_server hosting free
comments: true
archive: true
---
<strong>[UPDATED]</strong> GitHub Pages now runs Jekyll 2.2.0.
Check out the full list of 300+ changes and new features added to Jekyll since version 1.5.1.
[Read more](https://github.com/blog/1867-github-pages-now-runs-jekyll-2-2-0)

Problem is that SASS with Jekyll, cannnot be used GitHub Pages since the GitHub Pages server is still using Jekyll 1.5.1, as shown [here](https://pages.github.com/versions/).

Solution:

\#1 Use sass as described [here](http://jekyllrb.com/docs/assets/)

\#2 When committing changes and hosting on Github Pages, comment out the sass/scss options in the _config file

``` yaml
#/_config.yml
...
#sass:
#    sass_dir: _sass
#    style: :compressed
...
```
\#3 Copy the compressed file into \css\ after running `jekyll build` in local development. Copy the pre-compiled css from _site and place it into \css\.

\#4 Rename the main css file (e.g. main.scss) to _main.scss to avoid compilation by the static server

\#5 Go ahead and run commits and complete hosting

_If you like this hack, shout me out on [twitter](https://twitter.com/_nadjetey)_

More Vimm!
