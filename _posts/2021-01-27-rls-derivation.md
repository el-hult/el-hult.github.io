---
layout: single
title:  "Update equations for Recursive Least Squares"
tags: [recursive least squares, machine learning, signal processing, online learning, least squares]
---
The Recursive Least Squares (RLS) method is commonly used, but I did not find any derivation of it that suited me. 
Since I did the derivation for my own sake, I thought I would share it.
I'll do the derivation first, and then comment om some details.


## The derivation
This section is simply a derivation of the RLS update equations for weighted least squares with forgetting and regularizing initialization.
I rely on the presentation in [this tutorial by Arvind Yedla](http://pfister.ee.duke.edu/courses/ece586/ex_proj_2008.pdf), but do some with minor tweaks and changes in notation.

You are given a scalar series $$(y_t)_{t=1}^{t_{max}}$$ and a vector valued time series $$(z_t)_{t=1}^{t_{max}}$$. The task is to compute

$$
\label{eq:rls:optim} \theta_t := \text{arg min}_\theta \frac{1}{2} \sum_{s=1}^{t} \lambda^{t-s} |y_{s} - \theta^T z_{s} |^2 + \frac{\lambda^t\delta}{2} |\theta|^2 \tag{1}
$$

repeatedly for $$t$$ from $$t=1$$ to $$t_{max}$$. There are two tuning parameters: $$0\lt\lambda\leq1$$ and $$0\lt\delta$$.
The objective function is first cast into vector notation by means of a weight matrix $$\Lambda_t = \text{diag}(\lambda^0,\lambda^1,...\lambda^t)$$.
Define $$\vec y_t$$ to be the vector of $$(y_s)_{s=1}^{t}$$ up to time $$t$$.
Let $$\vec z_t$$ be a matrix with $$(z_s^T)_{s=1}^{t}$$ as the rows. This recasts the problem as
$$ \theta_t := \text{argmin}_\theta \frac{1}{2} (\vec y_t -  \vec z_t \theta)^T \Lambda_t (\vec y_t - \vec z_t \theta) + \frac{\lambda^t\delta}{2} \theta^T \theta $$
 

Diffrentiating and setting zero yields the equation
$$ \theta_t = \left(\vec z_t^T \Lambda_t\vec z_t + \lambda^t\delta I \right)^{-1} \vec z_t\Lambda_t \vec y_t  \tag{2} $$
We have introduced $$I$$ to denote an appropriately sized identity matrix.

This can be recursively be computed. Define 
$$ \vec p_t :=\vec z_t\Lambda_t \vec y_t = \lambda \vec p_{t-1 }+ z_ty_t$$
and 
$$ R_t := \left(\vec z_t^T \Lambda_t\vec z_t + \lambda^t \delta I \right)  = \lambda R_{t-1} + z_tz_t^T \tag{3}$$
and 
$$ P_t:=R_t^{-1} $$
. Since equation (3) is a rank-one update, we can apply the  [Sherman–Morrison formula](https://en.wikipedia.org/wiki/Sherman%E2%80%93Morrison_formula) and do fast updates on $$P_{t-1}$$ to obtain $$P_t$$.
The computation is
$$P_t:=R_t^{-1} = \lambda^{-1} \left( R_{t-1} +\lambda^{-1} z_tz_t^T   \right)^{-1} = \lambda^{-1}P_{t-1} - \lambda^{-1}\frac{P_{t-1} z_t z_t^T P_{t-1} }{\lambda+ z_t^T P_{t-1}z_t } $$
We may also introduce the _Kalman gain_ $$\vec k_t := \frac{P_{t-1} z_t}{\lambda+ z_t^T P_{t-1}z_t }$$ so that $$P_t = (I- \vec k_t z_t^T)\lambda^{-1}P_{t-1}$$. We now have most of the symbols needed to simplify equation (2).


$$
\begin{aligned}
	\theta_t
	 & = \left(\vec z_t^T \Lambda_t\vec z_t + \lambda^t\delta I \right)^{-1} \vec z_t\Lambda_t \vec y_t                                                               \\
	 & = P_t \vec p_t                                                                                                                                                     \\
	 & = ( I- \vec k_t z_t^T)\lambda^{-1}P_{t-1}\left[ \lambda \vec p_{t-1} + z_ty_t \right]                                                                        \\
	 & = ( I- \vec k_t z_t^T)\left[ \theta_{t-1} + \lambda^{-1}P_{t-1}z_ty_t \right]                                                                                \\
	 & =   \theta_{t-1} + \lambda^{-1}P_{t-1}z_ty_t - \vec k_t z_t^T\left[ \lambda \theta_{t-1} + \lambda^{-1}P_{t-1}z_ty_t \right]                             \\
	 & =   \theta_{t-1} + \lambda^{-1}P_{t-1}z_ty_t - \vec k_t \left[\hat y_t + \lambda^{-1} z_t^T P_{t-1}z_ty_t \right]                                        \\
	 & =   \theta_{t-1} + \lambda^{-1} \vec k_t y_t\left[\lambda+ z_t^T P_{t-1}z_t \right] - \vec k_t \left[\hat y_t + \lambda^{-1}z_t^T P_{t-1}z_ty_t \right] \\
	 & =   \theta_{t-1} + \vec k_t \left[y_t - \hat y_t \right]
\end{aligned}
$$

By the end, we introduced the prediction $$\hat y_t := z_t^T\theta_{t-1} $$. We finally introduce the _prediction error_ or _innovation_ $$e_t := y_t - \hat y_t$$ and arrive at our final update equation
$$ \theta_t = \theta_{t-1}+\vec k_t e_t$$

We initialize with $$P_0 = I \frac{1}{\delta}$$ and $$\theta_0 = \vec 0$$.

## Remark

In equation (1) we have a simple least squares objective plus a regularizing term. If not the regularizing term was vanishing with increasing $$t$$, it would be a ridge regression problem.

By not having a vanishing regularization like this, we cannot make the simple recursive formulation with rank one updates by the Sherman-Morrison formula. We are thus forced to have this vanishin regularization if we want fast simple updates.

Online ridge regression is a technique that has been studied, but is in the field of online convex optimization, and not typically studied in control or statistics.

If the forgetting factor $$\lambda=1$$, then the regularizing term will never vanish and we do get a online ridge problem.

The initialization $$P_0$$ is obvious here. The value chosen corresponds to a ridge regression with vanishing regularization coefficient. In some references (e.g. the [wikipedia article](https://en.wikipedia.org/wiki/Recursive_least_squares_filter)) they simply state that such an initialization is customary, but I think this derivation clearly shows where it comes from and how it should be interpreted.

Nothing in the derivation motivates why the one-step ahead prediction $$\hat y_t$$ is a reasonable idea. It does not show that the values converges to something reasonable. Please refer to other sources for such proofs.

## Meta-comments
I wrote this post by hand directly into the web-editor on github. It was a pain. But doing mistakes in what MathJax can/can't do, as well as falling into pitfalls from Jekyll and kramdown was a pain. I have soooo many manually type backslashes in the sourse that I soon need to find a better way to typeset this mess. I'll let you know in time.

Furthermore, it seems line breaking in MathJax `align` environments does not work as expected. 
This is apparently (a known bug in MathJax 3](https://github.com/mathjax/MathJax/issues/2312)
So a middle part in this post is a mess. 
I'll look into it eventually. But for now, I'll let it be.

_Update 2021-01-28_: Today I troubleshooted the errors in the markdown. I did so by installing [kramdown](https://kramdown.gettalong.org/) locally on my machine and then parsing this post. In that way I could see various parse errors and see the HTML output. I found the following:

1. \\left\[ had to be typed as `\\left\[`. Because otherwise the `[` is interpreted as a start of a [reference link](https://kramdown.gettalong.org/syntax.html#reference-links). 	
2. kramdown supports [mathmode](https://kramdown.gettalong.org/syntax.html#math-blocks). In that mode, normal escape rules are ignored so that one does not neet to do all the silly extra backslashes. What a mess! Using `$$math$$` will either produce `\[math\]` or `\(math\)` depending on whether it is written in line or as a separate block (blank line before and after).
