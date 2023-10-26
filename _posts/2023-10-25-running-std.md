---
title: "Running means and covariances"
tags: [online-learning, statistics]
---

## Welfords algorithm

The mean of a string of numbers is 

$$ \mu_n = (x_1+x_2 + \dots x_n)/n $$

and this gives a simple update equation for a running mean, when updating online. 

$$\mu_0 = 0$$
and 
$$\mu_{n} = \mu_{n-1}\frac{n-1}{n} + x_n\frac{1}{n}$$

The similar formlua for variance is by accumulating the sum of squares
$$ S_n = \sum_{i=1}^{n}x_ix_i^T = S_{n-1} + x_nx_n^T $$, $$S_0=0$$ and then compute 

$$ \Sigma_n = \frac{1}{n}\sum_{i=1}^n (x_i - \mu_n)(x_i - \mu_n)^T = \frac{1}{n}\left(\sum_{i=1}^{n}x_ix_i^T\right) - \mu_n^2 = \frac{S_n}{n} - \mu_n^2$$

The algorithm is not great, since we compute the answer as a difference between two large quantities, and may lose numeric precision.

We want to find an accumulator that is "closer" to the answer, not requireing a subtraction at the end. Examine the difference of sum of central squares, $$M_n = n\Sigma_n$$. We obtain 

$$
\begin{aligned}
\Sigma_n &= M_n/n \\
M_0 &= 0 \\
M_n &= M_{n-1} + \frac{n-1}{n}(x_n - \mu_{n-1})(x_n - \mu_{n-1})^T
\end{aligned}
$$

The proof of this formula is quite simple.  Some steps use the recursion $$\mu_{n} = \mu_{n-1} + \frac{x_n - \mu_{n-1}}{n}$$. Others use $$\sum_{i=1}^{n-1} x_i = (n-1)\mu_{n-1}$$. The rest uses straightforward algebra.
the computation below is for scalar data, but the generalization to vector valued data is straightforward since I won't use commutativity. Just replace multiplication with outer products.

$$
\begin{aligned}
    & M_n-M_{n-1} \\
    & = \sum_{i=1}^{n}(x_{i}-\mu_{n})^2 -  \sum_{i=1}^{n-1}(x_{i}-\mu_{n-1})^2 \\
    &= (x_{n}-\mu_{n})^2 + \sum_{i=1}^{n-1} \left[ (x_{i}-\mu_{n})^2 - (x_{i}-\mu_{n-1})^2   \right]\\
    &= (x_{n}-\mu_{n})^2 + \sum_{i=1}^{n-1} \left[(\mu_{n} -x_{i} ) \mu_{n}+( \mu_{n-1} -\mu_{n} ) x_{i} + (x_{i} - \mu_{n-1})\mu_{n-1} \right] \\
    &= (x_{n}-\mu_{n})^2 + (n-1) (\mu_{n} -\mu_{n-1} )^2 \\
    &= \frac{(n-1)^2}{n^2} (x_n - \mu_{n-1})^2  + \frac{n-1}{n^2} (x_n - \mu_{n-1})^2 \\
    &= \frac{n-1}{n} (x_n - \mu_{n-1})^2\\
    &= (x_n - \mu_{n-1})^2 - (x_n - \mu_{n-1})^2/n
\end{aligned}
$$

The paper *Comparison of Several Algorithms for Computing Sample Means and Variances* by Robert F. Ling (1974) [doi](https://doi.org/10.2307/2286154
) attributes the final equation to Welford (1962), but also posits some alternative algorithms and compare them. While writing this article, I found that others have written this or very similar blog post before me, e.g. [Joni Salonen](https://jonisalonen.com/2013/deriving-welfords-method-for-computing-variance/), [Jakob Ludewig](https://natural-blogarithm.com/post/variance-welford-vs-numpy/) and [John D Cook](https://www.johndcook.com/blog/standard_deviation/). The formulas reported in their posts may differ slightly from mine, and might be better. Do your own work if you want to be sure which one is the best for your data.
You can also read about this kind of algorithms on [Wikipedia](https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance).