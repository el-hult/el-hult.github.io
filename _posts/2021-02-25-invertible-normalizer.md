---
layout: post
title:  "An invertible BatchNormalizer1D"
tags: [machine learning, normalizing flow, pyyorch]
---

In Normalizing Flows, you might want to normalize the data at some point. 
Either in the input layer, because you want your model to learn the data normalization instead of manually normalizing, or becuase batch normalization really is something nice in you middle layers. 
I ran across this while reading the R-NVP paper [^1]. 

Normalization is implemented in PyTorch via the classes `torch.nn.BatchNorm1d` and the like. However - these do not implement the `inverse` function, nor compute the (log) jacobian determinant needed for implementation in Normalizing Flows. Therefore, I wrote a simple version of `torch.nn.BatchNorm1d` that do work well with noralizing flows, and put it in a Gist.

<script src="https://gist.github.com/el-hult/06d838b2efb3920a30917afcf9327bb4.js"></script>

It is very simple and quite self explanatory. Please read chapter 3.7 and appendix E in [^1] for the motivation. The API is supposed to be similar to `torch.nn.BatchNorm1d`. Enjoy!


[^1]: Dinh, Laurent, Jascha Sohl-Dickstein, and Samy Bengio. "Density estimation using real nvp." [https://arxiv.org/abs/1605.08803](https://arxiv.org/abs/1605.08803), Accepted at ICLR 2017 