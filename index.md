---
layout: single
title: Home
author_profile: true
related: false
---

Personal publication for Ludvig Hult. Notes about maths, latex, programming, machine learning and other hobbies.

See list of posts below.

<ul  style="list-style-type: none;">
  {% for post in site.posts %}
    <li style="margin-bottom: 0em">
      {{post.date | date: "%Y-%m-%d" }} <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>