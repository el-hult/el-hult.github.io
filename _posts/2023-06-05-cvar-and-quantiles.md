---
title:  "Quantile minimization should give good machine learning, but is hard. Does TERM solve that?"
tags: [machine-learning,quantiles,statistics,research]
---



When optimizing a machine learning model for an optimal parameter $$\hat\theta$$, we often rely on the empirical risk minimization framework, 

$$\hat\theta_{ERM} = \operatorname{argmin}_\theta \frac{1}{N}\sum_{i=1}^{N} \ell(\theta{},z_i) = \operatorname{argmin}_\theta \hat{R}_p^n(\theta)$$

selecting the model that achieves the minimal average loss $$\ell$$ over the data points $$z_i \overset{iid}{\sim} p$$, often called the empirical risk $$\hat{R}_p^n(\theta)$$. This is motivated by the law of large numbers - under certain assumptions, this will consistently minimize the population risk

$$ R_{p}(\theta) =  \mathbb{E}_{z\sim p} [\ell(\theta{},z) ] $$

Some problem can arise, making this optimization target inappropriate. Among other

 1. The distribution of $$z$$ has rare events making the convergence of $$\hat{R}_p$$ to $$R$$ very slow - sampling outliers increase the variance of the estimation 
 2. There is noise in the data - some samples that you don't want to train a model for. Since these samples typically produce large losses they influence the estimate - corruption outliers increase bias and/or variance in estimation
 3. The target distribution is unknown - we want to minimize $$R_{q}(\theta)$$, and expect $$p$$ and $$q$$ to be similar but don't know how - our estimation is biased already and we want to minimize the impact of that

## Quantile minimization

All the problems 1-3 might be possible to address with quantile minimization. It goes like this (to simplify things, assume that the losses are always absolutely continuous).
Define $$F^{-1}_\theta$$ to be the quantile function of the random variable $$ L_\theta = \ell(\theta{},z) $$ under $$z\sim p$$.
Lets minimize the target 

$$ Q_{p}(\theta) = F^{-1}_\theta(1-\alpha) $$

which means that we only care about an upper bound on the best (smallest) $$1-\alpha$$ fraction of losses.
Minimizing $$ Q_{p}(\theta) $$ is the same as maximizing the negative value-at-risk of $$L_\theta$$. See older post: ([link]({% post_url 2022-02-14-var-cvar-etc %})).

A different variant of the same idea would be to only train produce a model for fraction $$1-\alpha$$ of samples. This is called selective classification [^selective]
In the rest of cases, the model may say "I don't work for this sample" or similar. A natural idea then is to train a model that is good on average for the $$1-\alpha$$  fraction of samples with smallest loss values. Or rather, 

$$ \tilde{Q}_{p}(\theta) = \mathbb{E}[ L_\theta | L_\theta \leq F^{-1}_\theta(1-\alpha) ] $$

which is the negative conditional value at risk of $$L_\theta$$. See older post: ([link]({% post_url 2022-02-14-var-cvar-etc %})).

Because these minus signs come from the finance literature, where we minimize a financial loss, one sometimes incorporate that minus sign in definitions, and the definitions you read might differ slightly from above. In mixed distributions (continuous + discrete) the definitions also become nastier.

## Minimizing the quantile in practice

Quantile minimization does not work so well, however. To compute the quantile, we typically set up the pinball loss minimization problem. 

$$ Q_{p}(\theta)  = \min_q  \mathbb{E}_{z\sim p} [\rho(\ell(\theta{},z)) ] $$

$$\rho_\alpha(z,q)=\begin{cases} \alpha\lvert z-q \rvert &\text{if} z\leq q \\ (1-\alpha)\lvert z-q\rvert & \text{if} z\geq q\end{cases}$$

The function $$\rho_\alpha(z,q)$$ often being called the pinball loss[^quantile]. Unfortunately 

$$\hat\theta_{quant} = \operatorname{argmin}_\theta Q_{p}(\theta) = \operatorname{argmin}_\theta \min_q  \mathbb{E}_{z\sim p} [\rho(\ell(\theta{},z)) ] $$ 

will behave badly. To start with, the objective depends locally very sparsely on the data[^sparse], so solving the problem with gradient descent is wasteful. There are versions of the quantile objective, constructible from continuous relaxations (see e.g. [^softmedian], making a softmedian which compares to the median like softmax compares to the argmax function), which perform much better with respect to gradient descent.

Using a soft-quantile still does not solve the even harder problem; $$Q_{p}(\theta)$$ is not continuous in $$\theta$$. So good luck solving this two-stage optimization...

Can we approach the problem from some different angle?

## The TERM

A new paper[^new] introduces the idea of exponential tilts to the Machine Learning field. Specifically, they claim we should pick a $$t\in\mathbb{R}$$ and solve 

$$\hat\theta_{TERM} = \operatorname{argmin}_\theta \frac{1}{t}\log{}\left(\frac{1}{N}\sum_{i=1}^{N} e^{t\ell(\theta{},z_i)} \right)$$ 

This idea has a long history, but is new to the ML field. Among the points made in the paper are:

1. A small $t$ will produce an ERM-like solution that weights down outliers, effectively seeking a quantile estimate
2. They introduces a tilted VaR measure, TiVaR, and show that it is a good approximation for VaR, and by minimizing TiVaR, one more formally does Quantile Minimization.
3. They state (appealing to previous work) that DRO of a certain kind are exactly CVaR minimization problems.
4. They propose algorithms that are reasonably efficient in computing the solutions.
4. They show in numerical examples that the algorithm delivers what is promised.


## Other connections to the litterature

The article also ties in with previous work, very well -- it is 80 pages! But there are connections to papers I've read before, that *I* want to state.

Lets say future samples are sampled from $$q$$, but you don't know $$q$$. You do know that it is quite similar to $$p$$, and you do have samples from $$p$$. 
Train a model to be good on *all* distributions similar to $$p$$! This is a Distribution Robust Optimization idea. That is about addressing problem 3. above!

One idea is that penalizing the outlier losses (like via a quantile) might be connected to penalizing the variance of the losses.
This has been explored before[^maurer]. Doing variance penalization has been shown to address problem 1. above - sampling uncertainty.

Work by Gotoh et al[^gotoh] showw that DRO in a certain formulation, and in the limit of weak strong penalization is equivalent to variance penalization.
So in a sense, addressing problems 1. and 2. above is the same thing!
Another thing in that paper is showing that this DRO framework can also be applied to solve robust CVaR optimization. So there is a connection between CVaR and variance penalties...

Work by Hu et al[^hu] show that certain DRO formulation are worthless. More specifically; some classifiers are trained with a surrogate loss and while the model is robust in the surrogate, the actual classifier might not benefit from that. They show that if the DRO problem is recasted into a variance regularized ERM, we can get some benefits.





[^selective]: [Geifman, El-Yaniv](https://arxiv.org/abs/1705.08500)
[^new]: [Tian et al](http://jmlr.org/papers/v24/21-1095.html)
[^maurer]: [Maurer, Pontil](https://www.cs.mcgill.ca/~colt2009/papers/012.pdf)
[^gotoh]: [Gotoh, Kim, Lim](https://linkinghub.elsevier.com/retrieve/pii/S016763771730514X).
[^quantile]: section 1.3 from [doi:10.1017/CBO9780511754098](https://dx.doi.org/10.1017/CBO9780511754098) or [this one](https://doi.org/10.1016/j.ijforecast.2009.12.015)
[^softmedian]: https://piccolboni.info/2019/05/the-softmedian.html
[^sparse]: Consider the optimal points, i.e. when $$q=Q_{p}(\theta)$$. At this point, the quantile only depends on the data points above and below it - all other data points cancel out exactly and give zero contribution.
[^hu]: https://proceedings.mlr.press/v80/hu18a.html