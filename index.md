# Ludvig Hult

This is a first  version 

## CV

There might be a CV here at some point. 

## Social media 
There might be a social media link.


## Typesetting
I use github pages as simple as i can.

# Posts

I really want to use this for posting blog-like articles related to my research and readings.

Here they are

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>

