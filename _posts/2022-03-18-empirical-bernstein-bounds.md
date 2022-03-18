---
title:  "Empirical Bernstein Bounds"
tags: [probability, measure spaces, lebesgue]
---

In machine learning, you often rely on the central limit theorem (CLT) in some form.
For example, you hope that a model selected by empirical risk minimization will be good on future data points, since the empirical risk tends to the true risk. 
Empirical averages do tend to the true mean!

$$ \mathbb{E}_n[\ell_\theta(z)] \to \mathbb{E}[\ell_\theta(z)] $$

But how good is this convergence? For a finite sample size $$n$$, this might be very bad! But how bad? The CLT may be used, but the result is only asymptotic.
A common rule of thumb is to have $$n\geq 30$$ before you apply CLT. So what alternatives can we use?

We will turn to a simpler notation, having a series of random variables $$X_n$$ for $$n=1..$$, all being iid distributed, and $$\mathbb{E}[X_i]=\mu$$. The empirical mean over $$N$$ data points is $$\overline{X}_N=\frac{1}{N}\sum_{i=1}^{N}X_i$$. Let the empirical variance be $$V_N =\frac{1}{N}\sum_{i=1}^{N} (X_i - \bar{X}_N)^2)$$, and the true variance $$\mathbb{E}[(X_i-\mu)^2]=\sigma^2$$

# Variants

## CLT

The CLT gives an asymptotically valid confidence interval for the mean, which can be written as

$$
 \lim_{N\to\infty} \Pr\left[ \left|\overline{X}_N - \mu \right| \leq \Phi^{-1}(1-\delta/2) \sqrt{\frac{V_N}{N}}  \right] = 1- \delta
$$

using $$\Phi^{-1}$$ for the quantile function of a standard normal random variable. When $$N$$ is larger than ca $$30$$, this is often a good approximation. For small $$N$$, this is is often a bad approximation. To deal with finite $$N$$ we use alternative bounds. 

## Hoeffding

The Hoeffding inequality says that if $$\text{range} X \subseteq [l,u]$$, we always know that

$$
 \Pr\left[ \left|\overline{X}_N - \mu \right| \leq (u-l)\sqrt{\frac{\ln ( 2/\delta)}{2N}}  \right] \geq 1- \delta
$$

This is a funny bound, and can be impressibvely good, but if the interval $$[l,u]$$ is loose, the bound may be bad!


## Bennets Inequality

In the two-sided form, an inequality known as Bennets, also incorporates the variance of the data. [^maurer] 

$$
 \Pr\left[ \left|\overline{X}_N - \mu \right| \leq \sqrt{\frac{2\sigma^2 \ln ( 2/\delta)}{N}} +\frac{ (u-l) \ln ( 2/\delta) }{3N}  \right] \geq 1-\delta
$$

But the variance $$\sigma^2$$ of the data is not known, so it must be estimated. Since Bennets and Hoeffding are in a class of inequalities known as Bernsteins, these estimated variants are sometimes called Empirical Bernstein bounds. Two are presented below.

## Audibert, Munos, Szepesvári

Form Theorem 1 of [^audibert], we learn that 

$$
 \Pr\left[ \left|\overline{X}_N - \mu \right| \leq \sqrt{\frac{2V_{N}\ln ( 3/\delta)}{N}} +\frac{ (u-l) \ln ( 3/\delta) }{N}  \right] \geq 1- \delta
$$

## Maurir, Pontil

In theorem 4, [^maurer] presentes a single sided bound, and its 2-sided variant is 

$$
 \Pr\left[ \left|\overline{X}_N - \mu \right| \leq \sqrt{\frac{2V_{N} \ln ( 4/\delta)}{N}} +\frac{ 7(u-l) \ln ( 4/\delta) }{3(N-1)}  \right] \geq 1-\delta
$$

I bring it up because of the existance of a 1-sided version, only dealing with the risk of under-estimation. But otherwise, it is wokse than the form of Audibert, Munos and Szepesvári.

# Comparison

Generate random data, with $$[l,u]=[0,1]$$. By Popovicius inequality, $$\sigma^2 \leq 0.25$$. Compute the interval widths for $$N=10, 25, 50, 100, 200$$, $$V_N=0.01, 0.1, 0.25$$ and $$\delta = 0.01, 0.05, 0.1$$. The results are in the plot below. I include CLT, Hoeffding and Audiberts intervals. The code is available in a [GitHub Gist](https://gist.github.com/el-hult/7bd7395c0a23480e82f811dd3bcf96cc)

{%include image name="compare.svg" caption="Results from the numerical experiment. The plots is a bit too small, so please enlarge it to watch it. E.g. open in new tab and zoom a bit." %}

The conclusion (if you managed to enlarge it a bit) is that Audiberts bound only beat Hoeffding for the most favorable case: $$N=200$$, $$V_N=0.01$$ and $$\delta=0.1$$.

The CLT bound is generally much smaller.

To get the finite sample guarantee version of Bennets inequality, incorporating the estimated variance, we pay a price in the form of worsened constants compared to Bennet. These bad constants imply that in practise, they perform worse than Hoeffding.

For $$N \leq 30$$, the the $$O(1/N)$$-term is still often dominating, so by the time this term is negligable, CLT would give a good estimate anyways.

So in conclusion, the empirical bernstein bounds are interesting, but not always that useful. For small sampels, Hoeffding will do good. For large sampels, CLT is good.



# References

[^audibert]:
    J.-Y. Audibert, R. Munos, and C. Szepesvári, 'Exploration-exploitation tradeoff using variance estimates in multi-armed bandits', Theoretical Computer Science, vol. 410, no. 19, pp. 1876-1902, Apr. 2009, doi: [10.1016/j.tcs.2009.01.016](https://dx.doi.org/10.1016/j.tcs.2009.01.016).

[^maurer]:
    A. Maurer and M. Pontil, 'Empirical Bernstein Bounds and Sample-Variance Penalization', presented at the Conference on Learning Theory 2009, Montreal, Quebec, Canada, 2009. Accessed: Dec. 20, 2024. [Online]. Available: [https://www.cs.mcgill.ca/~colt2009/papers/012.pdf](https://www.cs.mcgill.ca/~colt2009/papers/012.pdf)