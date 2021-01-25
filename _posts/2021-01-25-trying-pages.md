---
layout: post
title:  "GitHub Pages with MathJax"
---

So I thought I'd write a line about how it is to have a first experience in using GitHub Pages and enabling MathJax. I had not used Jekyll at all before, so this took me a little bit of reading. So here it is.

## Background

GitHub Pages uses Jekyll to create static web pages. Jekyll parses markdown files, and those files may contain maths. 
By default, Jekyll uses the markdown parser kramdown, and [it identifies call math and make sure that it is tagged for MathJax to process](https://kramdown.gettalong.org/math_engine/mathjax.html). However, the actual rendering of the MathJax engine is not active by default. 
The easiest way to activate MathJax is by writing a `<script>` tag that tells the web browser to feth MathJax and process the whole page. This is well described on their [getting started page](https://www.mathjax.org/#gettingstarted). That script tag should be in the `<head>` section of the page, which in Jekyll is specified in the layout definitions, which in turn is part of the theme. So we must configure the theme to make it ave the correct MathJax include-links.
