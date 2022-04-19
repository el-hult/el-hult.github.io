---
layout: single
title: el-hult
author_profile: true
related: false
---

This is a kind of blog for Ludvig Hult, to save some thoughts for his own sake, and possibly to the benefit of others who are confused about maths, latex, programming, and my other hobbies.

See list of posts by navigating in the menu or selecting below.

<ul  style="list-style-type: none;">
  {% for post in site.posts %}
    <li style="margin-bottom: 0em">
      {{post.date | date: "%Y-%m-%d" }} <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>