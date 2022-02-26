---
layout: single
title: About
author_profile: true
related: true
---

This is a kind of blog for Ludvig Hult, to save some thoughts for his own sake, and possibly to the benefit of others who are confused about maths, latex, programming, and my other hobbies.

See list of posts by navigating in the menu or selecting below.

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>