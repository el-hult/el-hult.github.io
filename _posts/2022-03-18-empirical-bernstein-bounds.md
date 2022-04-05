---
title:  "Empirical Bernstein Bounds"
tags: [probability, measure spaces, lebesgue]
---

In machine learning, we often rely on the possibility to estimate an expectation by a sample mean. 
One example is the hope that a model selected by empirical risk minimization will be good on future data points, since the empirical risk tends to the true risk. 
Empirical averages do tend to the true mean!

$$ \lim_{n\to\infty} \mathbb{E}_n[\ell_\theta(z)] \to \mathbb{E}[\ell_\theta(z)] $$

But how good is this convergence?
For a finite sample size $$n$$, we might still have a bad approximation! But how bad?
The central limit theorem (CLT) a standard approximation to estimate the uncertainty in the approximation, and I'll review its result below, but that result is only asymptotic.
A common rule of thumb is to have $$n\geq 30$$ before you apply CLT. So what alternatives can we use when we have smaller sample sizes?

We will turn to a simple notation, having a series of random variables $$X_n$$ for $$n=1..$$, all being iid distributed. The  mean $$\mathbb{E}[X_i]=\mu$$ and variance variance $$\mathbb{E}[(X_i-\mu)^2]=\sigma^2$$ are fixed unknown. The empirical mean -- or sample mean -- $$\overline{X}_N=\frac{1}{N}\sum_{i=1}^{N}X_i$$ and variance $$V_N =\frac{1}{N}\sum_{i=1}^{N} (X_i - \bar{X}_N)^2)$$ over $N$ data points are random variables, since they are functions of $$N$$ random variables.

# Measures of uncertainty in mean estimation

Below, I'll state a few different bounds on the estimation error between empirical mean and the true mean. In the end I will compare them.

## Central limit theorem

The CLT gives an asymptotically valid confidence interval for the mean, which can be written as

$$
 \lim_{N\to\infty} \Pr\left[ \left|\overline{X}_N - \mu \right| \leq \Phi^{-1}(1-\delta/2) \sqrt{\frac{V_N}{N}}  \right] = 1- \delta
$$

using $$\Phi^{-1}$$ for the quantile function of a standard normal random variable. When $$N$$ is larger than ca $$30$$, this is often a good approximation. For small $$N$$, may be a bad approximation. The bound is proportional to $$1/\sqrt{N}$$, which is good to note in comparison to the later bounds.

## Hoeffding

The Hoeffding inequality says that if $$\text{range} X \subseteq [l,u]$$, we always know that

$$
 \Pr\left[ \left|\overline{X}_N - \mu \right| \leq (u-l)\sqrt{\frac{\ln ( 2/\delta)}{2N}}  \right] \geq 1- \delta
$$

This is a interesting bound as it disregards the variance of data altogether. It can be impressively, good assuming $$(u-l)$$ is not to large in comparison with the variance. By [Popoviciu's inequality on variances](https://en.wikipedia.org/wiki/Popoviciu%27s_inequality_on_variances) we have that $$(u-l) \geq 2 \sigma$$, which is a sometimes useful tool for assessing the looseness of the range $$[l,u]$$.


## Bennets Inequality

To incorporate information about the variance into the bound, we can turn to Bennets inequality. [^maurer] The two-sided formulation looks like

$$
 \Pr\left[ \left|\overline{X}_N - \mu \right| \leq \sqrt{\frac{2\sigma^2 \ln ( 2/\delta)}{N}} +\frac{ (u-l) \ln ( 2/\delta) }{3N}  \right] \geq 1-\delta
$$

And it asserts that the $$1/\sqrt{N}$$ term depends on the variance, but we must also respect the range of $$X$$ via a $$1/N$$-proportional term. This is the price we pay for having a finite sample valid inequality compared to the CLT, and using the actual variance, compared to Hoeffding.

The variance $$\sigma^2$$ is not known, so it must be estimated. Since Bennets and Hoeffding are in a class of inequalities known as Bernstein's, variants that use empirical estimates are sometimes called Empirical Bernstein bounds.

## Audibert, Munos, Szepesvári

The first Empirical Bernstein bound is presented as Theorem 1 of in a paper by Audibert et al[^audibert]. We learn that 

$$
 \Pr\left[ \left|\overline{X}_N - \mu \right| \leq \sqrt{\frac{2V_{N}\ln ( 3/\delta)}{N}} +\frac{ (u-l) \ln ( 3/\delta) }{N}  \right] \geq 1- \delta
$$

which is a Bennet-like inequality. The variance has been traded for an empirical variance, and it costs us a worse constant coefficient in both the $$1/N$$ and the $$1/\sqrt{N}$$ terms.

I will also mention theorem 4, of Maurer and Pontil [^maurer]. They present a single-sided bound which is tighter than the bound of Audibert et al. But the two-sided formulation of it is worse, so I'll not analyze it further here.

# Comparison

Below is a simple comparison of the methods for various settings. We can always scale the data so it is supported on $$[l,u]=[0,1]$$. By Popoviciu's inequality, $$\sigma^2 \leq 0.25$$, which informs us to try $$V_N=0.01, 0.1, 0.25$$. We try sample sizes $$N=10, ..., 200$$,  and $$\delta = 0.01, 0.05, 0.1$$. The results are in the plot below. I include CLT, Hoeffding and Audibert intervals. The code is available in a [GitHub Gist](https://gist.github.com/el-hult/7bd7395c0a23480e82f811dd3bcf96cc)

{%include image name="compare.svg" caption="Results from the numerical experiment. Consider enlarging the plots it to watch it, e.g. open in new tab." %}

The conclusion is that Audibert bound only beat Hoeffding for the most favorable case: very large $$N$$, very small $$V_N$$ and large $$\delta$$.
So if finite sample guarantee is needed, Hoeffding will often be a better bound.

If you have a large sample size $$N$$, the CLT approximation is good, and the plots should that the CLT approximate bound is always better than the Audibert and Hoeffding bounds. It is also valid for random variables not supported on a finite interval, which gives it more generality.

In conclusion: the empirical bernstein bounds are interesting, but not always that useful. For small samples, Hoeffding will do good. For large samples, CLT is good.



# References

[^audibert]:
    J.-Y. Audibert, R. Munos, and C. Szepesvári, 'Exploration-exploitation tradeoff using variance estimates in multi-armed bandits', Theoretical Computer Science, vol. 410, no. 19, pp. 1876-1902, Apr. 2009, doi: [10.1016/j.tcs.2009.01.016](https://dx.doi.org/10.1016/j.tcs.2009.01.016).

[^maurer]:
    A. Maurer and M. Pontil, 'Empirical Bernstein Bounds and Sample-Variance Penalization', presented at the Conference on Learning Theory 2009, Montreal, Quebec, Canada, 2009. Accessed: Dec. 20, 2024. [Online]. Available: [https://www.cs.mcgill.ca/~colt2009/papers/012.pdf](https://www.cs.mcgill.ca/~colt2009/papers/012.pdf)