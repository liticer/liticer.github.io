---
layout: post
title:  "Installing Rails on GNU Linux"
date:   2014-02-20
tags: linux rails gnu ruby
comments: true
archive: true
---

It is no news that sometimes, the most diffult part of developing software is - setting up the development environment. This tutorial is going to walk you through 9 simple steps to installing [Ruby on Rails (RoR)](http://rubyonrails.org/). This method uses [RVM](https://rvm.io/). Type the following commands into your ``terminal``

    sudo apt-get install git-core build-essential

    curl -L get.rvm.io | bash -s stable

    rvm requirements

    source ~/.rvm/scripts/rvm
Restart terminal &

    type rvm | head -n 1
The previous command shoud output

    rvm is a function

    rvm install 2.1.0

    rvm use 2.1.0 --default

    gem install rails

Thats it!