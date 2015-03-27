---
layout: post
title:  "Dirty tracking"
date:  2014-11-24
comments: true
tags: cs-concepts web-dev
archive: false
---
Dirty tracking is a way to check if an attribute of interest has changed or not - it is a way to verify is an attribute is dirty (or changed). Rails/ActiveModel supports dirty tracking.

+ \_attr_changed?  #=> returns a whether attr changed.
+ attr\_change  #=> returns an array [old\_value, new_value].
+ attr_was  #=> returns the old value of attr.

### Use in an example

```ruby
after_validation :geocode, :if => :address_changed?
:address_changed? #=> This is an example of dirty tracking
```