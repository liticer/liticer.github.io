---
layout: post
title:  "The Journey &mdash; Book one complete"
date:   2014-05-28
tags: ruby rails rubyonrails gem rubygems rails-4 timetrap the-depot-application Pragmatic-Bookshelf
comments: true
archive: true
---

Today, I can say I have completed the book ["Agile Web Development with Rails, Edition 4"](http://pragprog.com/book/rails4/agile-web-development-with-rails-4). I'm excited, especially after such an expected surprize in hosting challenges on [Heroku](https://www.heroku.com/home). I'm talking about issues with:

| Problem | Solution |
| ------------- |:-------------:|
|Converting my Sqlite3 database to |  [yaml_db](https://rubygems.org/gems/yaml_db) |
|Heroku rails assets not found | [rails_12factor](https://github.com/heroku/rails_12factor)|
<br />

But in the end I triumphed! I think I spent about an hour and half for this last task (The Task K: Deployment and Production). That brings the total time for reading and completing the _Agile Web Development with Rails_ book to an estimated __12 hours__.

The demo application accompanied with this book, is web-based shopping cart application called Depot (Pragmatic Bookshelf). This application implements an online store, with a catalog, cart, and orders. You are invited to take a look at the source [here](https://github.com/nadjetey/Depot) or view the live app online [here](http://depot-app-4696.herokuapp.com/).

_PS: To log into the app as an administrator use these log in credentials:_

```
username: admin
password: admin
```

### Time log
For a more comprehensive log of my time spent, refer to the following file (by kind courtesy [timetrap](http://rubygems.org/gems/timetrap))

```text
Timesheet: Task A - Creating the application
    Day                Duration   Notes
    Mon May 12, 2014   0:10:27    A1:Creating the Products -
                                    maintenance application
                       0:13:30    A2:Making prettier listings
                       0:23:57
    ------------------------------------------------------------------------
    Total              0:23:57

Timesheet: Task B - Validating and Unit testing
    Day                Duration   Notes
    Mon May 12, 2014   0:12:21    B1:Validating!
                       0:02:32    B2: Unit testing
                       0:14:31    B2: Unit testing
                       0:29:24
    ------------------------------------------------------------------------
    Total              0:29:24

Timesheet: Task C - Catalog Display
    Day                Duration   Notes
    Mon May 12, 2014   0:09:33    C1:Creating the catalog listing
                       0:12:17    C2:Adding a page layout
                       0:02:49    C3:Use a Helper to format the price
                       0:03:49    C4:Functional testing
                       0:06:58    C5:Caching
                       0:35:26
    ------------------------------------------------------------------------
    Total              0:35:26

Timesheet: Task D - Cart Creation
    Day                Duration   Notes
    Mon May 12, 2014   0:04:17    D1:Finding a cart
                       0:07:21    D2:Connecting Products to Carts
                       0:10:15    D3:Add a button
                       0:06:42    D3:Add a button
                       0:28:35
    ------------------------------------------------------------------------
    Total              0:28:35

Timesheet: Task E - A Smarter Cart
    Day                Duration   Notes
    Mon May 12, 2014   0:32:46    E1:Creating a smarter cart
                       0:14:09    E2:Handling Errors
                       0:26:02    E3:Finishing the Cart
                       1:10:38    E3:Finishing the Cart
                       2:23:35
    ------------------------------------------------------------------------
    Total              2:23:35

Timesheet: Task F - Add a dash of Ajax
    Day                Duration   Notes
    Tue May 13, 2014   0:03:12    F1:Moving the cart
                       0:08:22    F1:Moving the cart
                       0:52:06    F1:Moving the cart
                       0:06:15    F2:Creating an AJAX-based cart
                       0:14:58    F3:Highlighting changes
                       0:21:52    F4:Hiding an empty cart
                       0:00:22    F5:Making images clickable
                       0:04:19    F5:Making images clickable
                       0:22:39    F6:Testing AJAX changes
                       2:14:05
    ------------------------------------------------------------------------
    Total              2:14:05

Timesheet: Task G - Check out!
    Day                Duration   Notes
    Tue May 13, 2014   0:17:59    G1:Capturing an order
                       0:38:46    G1:Capturing an order
                       0:56:45
    Wed May 14, 2014   0:12:44    G2:Atom feeds
                       0:12:44
    Mon May 19, 2014   0:12:14    G3:Downloading an eBook
                       0:12:14
    ------------------------------------------------------------------------
    Total              1:21:43

Timesheet: Task H - Senging Mail
    Day                Duration   Notes
    Tue May 20, 2014   0:39:57    H1:Email notification
                       0:10:01    H2:Integration tests
                       0:49:58
    ------------------------------------------------------------------------
    Total              0:49:58

Timesheet: Task I - Logging In
    Day                Duration   Notes
    Tue May 20, 2014   0:43:39    I1:Adding users
                       0:20:33    I2:Authenticating users
                       0:29:13    I3:Limiting access
                       0:20:53    I4:Add a sidebar
                       1:54:18
    ------------------------------------------------------------------------
    Total              1:54:18

Timesheet: Task J - Internationalization
    Day                Duration   Notes
    Tue May 20, 2014   0:03:49    J1:Selecting a locale
                       0:18:21    J1:Selecting a locale
                       0:14:21    J2:Translating the store
                       0:13:39    J3:Translating checkout
                       0:05:58    J4:Locale switcher
                       0:56:08
    ------------------------------------------------------------------------
    Total              0:56:08

----------------------------------------------------------------------------
Grand Total            11:37:09
----------------------------------------------------------------------------
```

More Vimm!