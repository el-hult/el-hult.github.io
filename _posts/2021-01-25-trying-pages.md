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
to always get the latest MathJax version. I add that to the `_includes/mathjax.html` file.

However, we now need to make sure that Jekyll always includes that file, when building the static site. We wish to use the (https://jekyllrb.com/docs/includes/) mechanism.

The theme I use have the full source from [here](https://github.com/pages-themes/minimal) and I copy files from there, and just make small changes to make sure the java script references are there. You can get the whole `default.html`, and then I just insert a single include-statment `{include mathjax.html}` and then it is done.
