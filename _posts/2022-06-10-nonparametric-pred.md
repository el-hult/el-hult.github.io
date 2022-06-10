---
title:  "Nonparametric prediction intervals"
tags: [statistics]
---

There is a simple formula for a onesided nonparametric prediction interval under exchangeable data. One can derive it very directly under iid assumptions, and the computation is quite simple. 
It goes like this:

Let $$X_i, i=1,... n+1$$ be iid random variables, with continuous cdf $$F$$. With probability 1, all $$X_i$$ have distinct values, so we will assume that throughout.
 
Let $$U_i, i=1,... n+1$$ be iid random variables, with uniform distribution over $$[0,1]$$. Its density is $$f_U(u)$$ and its cdf is $$F_U(u)$$.

Let $$X_{n,(k)}$$ be the $$k$$'th smallest value of $$\{X_i\}_{i=1}^{n}$$. Similar for $$U_{n,(k)}$$. It is called the $$k$$'th order


$$
\begin{aligned}
&\Pr[ X_{n+1} \leq X_{n,(k)}] =\\
&\Pr[ F(X_{n+1}) \leq F(X_{n,(k)})] =\\
&\Pr[ U_{n+1} \leq U_{n,(k)}]=\\ 
& \{\text{use independence and uniformity}\} =\\
&\mathbb{E} [ U_{n,(k)} ]
\end{aligned}
$$

This is a Beta-expectation, because

$$
\begin{aligned}
f_{U_{n,(k)}}(u) \propto & f_{U}(u) F_U(u)^{k-1} (1-F_{U}(u))^{n-k} \\
\propto & u^{k-1}(1-u)^{(n-k+1)-1}
\end{aligned}
$$

shows that $$U_{n,(k)} \sim \operatorname{Beta}(k,n-k+1)$$,
and it is known that its expectation is $$ k/(n+1)$$.
You can either perform the integration, or just look it up in a table.

Conclude that $$\Pr[ X_{n+1} \leq X_{n,(k)}]=k/(n+1)$$ under iid assumptions.


### Discussion

This result is not very deep, but awfully general. I realized it while reading chapter 13 and 21 in "Asymptotic statistics" from 1998, byt A.W. Vaart, published by Cambridge University Press. It is a nice book that I can happily recommend.

The same result holds under exchangeability as well, is not much harder to prove that way, and in that form it is the basis for many permutation tests. Undoubtledly, the result is more useful under exchangeability, but I wanted to share this simple iid version.

The transformation from $$X_i$$ to $$U_i$$ is called the integral probability transform, and it is a generally useful tool.

I guess this result is also presented in different text books. I hope it is, because it is instructive and simple to present. But it I have not seen it in statistics book for engineers, so it could be worth spreading like this. I hope it can help you.