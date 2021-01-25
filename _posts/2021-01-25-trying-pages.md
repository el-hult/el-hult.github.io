---
layout: post
title:  "GitHub Pages with MathJax"
---

So I thought I'd write a line about how it is to have a first experience in using GitHub Pages and enabling MathJax. I had not used Jekyll at all before, so this took me a little bit of reading. So here it is.

## Background

GitHub Pages uses Jekyll to create static web pages. Jekyll parses markdown files, and those files may contain maths. 
By default, Jekyll uses the markdown parser kramdown, and [it identifies call math and make sure that it is tagged for MathJax to process](https://kramdown.gettalong.org/math_engine/mathjax.html). However, the actual rendering of the MathJax engine is not active by default. 
The easiest way to activate MathJax is by writing a `<script>` tag that tells the web browser to feth MathJax and process the whole page. This is well described on their [getting started page](https://www.mathjax.org/#gettingstarted). That script tag should be in the `<head>` section of the page, which in Jekyll is specified in the layout definitions, which in turn is part of the theme. So we must configure the theme to make it ave the correct MathJax include-links.

## How to

1. Create a github pages repository. Follow instructions [here](https://pages.github.com/). Initialize it as empty.
1. Select a theme. I chose minimal, also called `jekyll-theme-minimal`. Documentation can be found [here](https://github.com/pages-themes/minimal). Think of it like this: when GitHub Pages processes your repo (using Jekyll) to create the static pages, it will look into directories such as `_layouts` and `_includes` to compile the page. If the file is not available in your repo Jekyll will fall back to the files in the Theme (i.e. that linked repo with the documentation). Thus, all config is made by overriding files from the base repo.
1. Copy the `_layout/default.html` file from the source repo and into your own repo. Inside the `<head>` tag, write the code {% raw %}`{% include mathjax.html %}`{% endraw %}. This will utilize the jekyll [include](https://jekyllrb.com/docs/includes/) mechanism to insert the content of that `mathjax.html` file in the page head of all your pages. 
1. Create the file `_includes/mathjax.html` with the `<script src=...>` as described in [the MathJax documentation](https://www.mathjax.org/#gettingstarted). Now all your pages are MathJax powered!
1. Create `index.md` and write some math. Commit it. Then read your page at `username.github.io` or whatever page name you have.

Now it is done! So here is an equation: \\(h=3\\).
