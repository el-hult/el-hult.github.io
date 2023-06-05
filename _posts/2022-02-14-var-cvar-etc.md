---
title:  "CVaR, VaR and quantiles"
tags: [probability, finance]
---

There are funny concept in mathematical finance, that have strange abbreviations and funny names. 
It seems part of the problem is that one tries to capture financial risk via mathematical statistical models, and these models are imperfect.
So within the field of finance, one downplays the mathematical definitions, in order to not overemphasize idealized models.
This is all good and well, but it saddens me that the wikipedia pages on [Expected Shortfall](https://en.wikipedia.org/wiki/Expected_shortfall), [Value at Risk](https://en.wikipedia.org/wiki/Value_at_risk) and wikipedia [Quantiles](https://en.wikipedia.org/wiki/Quantile) are partly incompatible, and together quite unintelligeble.

This post is an attempt to state proper definitions and provide some sources. 

Let $$(\Omega,\mathcal F , p)$$ be a probability triplet. Let $$X$$ be a random variable (i.e. a measurable random variable $$\Omega \to \mathbb R$$). Let $$F$$ be its distribution (i.e. $$F_{X}(x) = P(X\leq x)$$). Ths is as in standard text books, such as [^gut].

## The Quantile function
Assume a random variable $X$ with cumulative distributeion function $$F$$. It is thus right-continous and has left-limits. It is not necessarily inective nor surjective. But it might be nice to have its inverse anyways. How do you defined it canonically still?

The *quantile funtion* is the unique function $$F^{-1}$$ fulfilling the Galois connection

$$ \alpha  \leq F_{X}(x) \text{ if and only if } F^{-1}_{X}(\alpha) \leq x $$

In all cases, we may compute $$F^{-1}_{X}$$ by

$$F^{-1}_{X} = \inf \{ \alpha : F_{X}(x) \leq \alpha \}$$

This definition is canonical, and you can read it on wikipedia [^1].

If $$F$$ is continous and strictly monotomic, $$F^{-1}_{X}$$ is indeed an inverse.

## Quantiles

If we forget about the Galois criterion for a second, we could imagine a whole family of quantiles. Any value $$q(c)$$ so that $$F_{X}(q(c))=c$$ is thinkable.

One such alternative definition is given in [^2]. In this article, they first stipulate that $$\Omega$$ is finite. I guess this is to make sure that limits always exists and so on.... But anyway. Definition 3.2 in that article, after replacing some symbols, states that

> Given $$c \in (0,1)$$, the number $$q$$ is a $$c$$-quantile of the random variable $$X$$ under distribution $$P$$ is any of the following three conditions are satisfied
>
> i. $$P(X\leq q)\geq c$$ and  $$c \geq P(X< q)$$
>
> ii. $$P(X\leq q)\geq c$$ and  $$ P(X\geq q)  \geq 1-c$$
> 
> iii. $$F_{X}(q)\geq c$$ and $$c \geq F_{X}(q_-)$$ where $$F_{X}(q_-) = \lim_{x\to q,r<q}F_{X}(x)$$
>
> Remark: The set of such $$c$$-quantiles is a closed interval. Since $$\Omega$$ is finite, there is
a finite left (respectively, right) end point $$q^{-}_{c}$$ (respectively, $$q^{+}_{c}$$) that satisfies $$q^{-}_{c} = \inf \{ x  : F_{X}(x) \geq a \}$$ [equivalenty $$\sup \{x:F_{X}(x)<c\}$$] (resp. $$q^{+}_{c} = \inf \{ x  : F_{X}(x) > c \}$$. With the exception of at most countably many $$c$$, the equality $$q^{-}_{c}=q^{+}_{c}$$ holds. [...]

We introduce the names *left quantile* and *right quantile* for $$q^{-}_{c}$$ and $$q^{+}_{c}$$. We illustrate the concepts in the image below. I will use the notation $$q_{c}(X), q^{-}_{c}(X), q^{+}_{c}(X)$$ to denote these are the quantile, left- and right-quantiles for the random variable $$X$$.

{% include image name="quantiles.svg" caption="Quantiles, right and left" %}

## Value at Risk

For a given financial asset and time horizon, the return on the investment can be positive (a profit) or negative (a loss).
Fix a probability $$\alpha$$. The value at risk ($$\operatorname{VaR}_{\alpha}(X)$$), at that probability, is an amount of money, so that losses in the worst $$\alpha$$ percent of time is at least that large. In maths:

Let $$X$$ be a random variable representing the profit/loss. Fix $$\alpha \in (0,1)$$. Then

$$ \operatorname{VaR}_{\alpha}(X) = -q_{\alpha}^{+}(X) = q_{\alpha}^{-}(-X) = F^{-1}_{-X}(\alpha) $$

Notice the minus sign so that a loss is still reported as a positive amount of money.

This definition is chosen so that if we keep $$\operatorname{VaR}_{\alpha}(X)$$ amount of money at hand, we can cover the losses in $$1-\alpha$$ amount of cases. In the last $$\alpha$$ amount of cases, the losses are worse than that, and this risk measure does not care about that.

The definition here stated is taken from Definition 3.3 in [^2] as well, with a small adjustments. In that definition, the net profit of some investment is called $$X/r$$, as the value of one financial instrument $$X$$ is measured against some other instrument $$r$$. By the replacement $$X \mapsto X/r$$, the definitions are equivalent

## Conditional Value at Risk / Expected Shortfall

Since $$\operatorname{VaR}_{\alpha}(X)$$ does not care for the risk at unprobable events in the left tail of $$X$$, we might want to calculate the expected loss, for such events. That is called the Expected Shortfall ($$\operatorname{ES}$$), or the Conditional Value at Risk ($$\operatorname{CVaR}$$). Formally,

$$ \operatorname{CVaR}_{\alpha}(X) = - \mathbb{E}[ X | X \leq -\operatorname{VaR}_{\alpha}(X)] $$

Notice that onece again, we need to juggle the minus sign to make sure the losses are reported as positive numbers.

It is sometimes clearer to state the $$\operatorname{CVaR}_{\alpha}(X)$$ for $$X$$ in terms of the loss $$L=-X$$ so that the juggling is more consistent.

$$ \operatorname{CVaR}_{\alpha}(X) = \mathbb{E}[ L | L \geq F^{-1}_{L}(\alpha)]$$

but this formula seems not to be the standard one in financial litterature.


## Closing comments

The definitions are a bit finicky and the trouble with them are mostly the use of inequalities. For all "kind" distributions, that are purely categorical or absolutely continous, this is not an issue. But in mixed distributions, where some intervals of outcomes are unthinkable, or there are point masses, this might be worse.

All this matters, as one of the primary critiques against $$\operatorname{VaR}_{\alpha}(X)$$ and $$\operatorname{CVaR}_{\alpha}(X)$$ is that they rest on specific mathematical assumptions difficult to verify in practise. And the least we can do then, is to know these definitions very well and understand their quirks and implications.

My only open issue is to understand if $$q^{-}$$ and $$q^{+}$$ exists always when $$\Omega$$ is not finite, but countable, or uncountable. We always have $$q^{-}$$ well defined, but the existance of $$q^{+}$$ and the relation $$q^{-}(X) = -q^{+}(-X)$$ seems less obvious. I honestly haven't thought too much about it.


[^1]: [Wikipedia on quantiles and the quantile function](https://en.wikipedia.org/wiki/Quantile)
[^2]: Artzner, P., Delbaen, F., Eber, J.-M. & Heath, D. "Coherent Measures of Risk". *Mathematical Finance* 9, 203–228 (1999)  preprint:[https://people.math.ethz.ch/~delbaen/ftp/preprints/CoherentMF.pdf](https://people.math.ethz.ch/~delbaen/ftp/preprints/CoherentMF.pdf), DOI: [10.1111/1467-9965.00068](https://onlinelibrary.wiley.com/doi/abs/10.1111/1467-9965.00068)
[^gut]: A. Gut, Probability: a graduate course, Second edition. New York: Springer, 2013.

