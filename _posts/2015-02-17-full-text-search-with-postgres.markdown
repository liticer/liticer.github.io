---
layout: post
title:  "Full text search w/ RoR and Postgres"
date:  2015-02-17
comments: true
tags: postgres full-text-search
archive: false
---
Full text searching provides the capability to identify documents/models that satify a query, and even sort by relevance to the query (optional). [Full documentation](http://www.postgresql.org/docs/9.1/static/textsearch-intro.html)

1 Build your search form

```erb
<%= form_tag users_path, :method => "get" do %>
  <p>
    <%= text_field_tag :query, params[:query], :placeholder => "Search..." %>
    <%= submit_tag "SEARCH", :name => nil %>
  </p>
<% end %>
```

2 Alter Controller action

```ruby
# GET /users filtered by custom search method
def index
  @search = User.custom_search(params[:query])
end
```

3 Alter the model and define custom search function

```ruby
def self.custom_search(query)
  if query.present?
    where("name @@ :q", q: query)
  else
    all
  end
end
```

Done!