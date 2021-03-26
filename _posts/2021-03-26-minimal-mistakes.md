---
title:  "Jekyll Minial Mistakes"
tags: [jekyll, ruby, github-pages]
---

Today I migrated to [Minimal-Mistakes](https://mmistakes.github.io/minimal-mistakes/), quite possiblu the most common Jekyll theme for personal blogs in the ML-AI clique.
I realized it was worth it to migrate since it gives so much more out-of-the-box than the [Minimal theme](https://github.com/orderedlist/minimal) I used before.
It was probably a good idea to start with Minimal, and then step up. This was good for learning jekyll and kramdown and so on. I would recommend anyone else to do the same and start with some really tiny jekyll theme at first.

Making this change was a bit interesting, and another important step in getting it to work was installing more ruby packages locally to be able to efficiently troubleshooting and testing the theme.
Having ruby installed on WSL seemed to have been an issue. I had mismatching versions of kramdown, which was horrible. I had to uninstall Ruby alltogether, and apt-get uninstall jekyll, and then after a fresh installation of ruby and jekyll (via bundler) it worked out well.

Doing this overhaul, I also added favicons and social media buttons. It is simple to see why the minimal-mistakes template is so much used!