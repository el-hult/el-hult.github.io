---
layout: post
title:  "Trying GitHub Pages"
---
So I thought I'd write a line about how it is to have a first experience in using GitHub Pages.

MAking a minimal start is simple. But getting Latex rendering to work is more difficult. Especially since I have not used Jekyll before.
So this post is simply me trying to understand how posts work. 

Enjoy!


Oh! And here is an image ![Some curves in  achart](/assets/betas.png)


$$x=3-e^{4\ell}$$

The formula above is not the same as $h=3$.


## MAthJax
So GitHub Pages uses Jekyll. And I use the default markdown parser kramdown.
It identifies can identify all math and make sure that it is tagged for MathJax to process. See here: (https://kramdown.gettalong.org/math_engine/mathjax.html).

However, Jekyll does not ship with mathjax. So I need to tell Jekyll to inculde the import-link for math-jax.
That can be done in several ways. 

According to the [MathJax documentation](https://www.mathjax.org/#gettingstarted), we should make sure to include 
```html
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
```
to always get the latest MathJax version. I add that to the `_includes/scripts.html` file.
