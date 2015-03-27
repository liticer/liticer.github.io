---
layout: post
title:  "Current traffic analysis failures"
date:   2014-02-28
tags: traffic-analysis GitHub bitdeli
comments: true
archive: true
---

"Service disruption: GitHub has recently changed the way images are served in readmes. This has seriously limited our traffic analytics features for repositories. Read more"

This was the welcome notice I received while trying to view the traffic to my GitHub repositories using [bitdeli](http://blog.bitdeli.com/post/77717727361/on-githubs-image-proxy). The most bitdeli could do was post this on their site:
> There doesn’t seem to be an easy way to fix the problem on our side.
> Fortunately GitHub released their own traffic analytics just before
> blocking image-based tracking, so now you can get the basic metrics
> directly from GitHub.
> We apologize for any inconvenience this transition may cause.

On the bright side, Github is actually giving you by default all the traffic analysis features - get this - for free! It was part of a system wide upgrade, so all you have to do is

+ click on the `contributor` link right under the description of your repo
+ then finally click on the `traffic` tab

on your own GitHub account for traffic monitoring and analysis.

[GitHub traffic tutorial](https://github.com/blog/1672-introducing-github-traffic-analytics)