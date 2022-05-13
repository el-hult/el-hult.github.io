---
title:  "Example of limits and Lebesgue integration"
tags: [probability, integration, math]
---

Examples from Lebesgue theory and examples in integration and taking limits. Specifically, bounded convergence.

# Why?

Do you often wonder if

$$
\lim_{n\to\infty} \int f_n d\mu = \int \lim_{n\to\infty} f_n d\mu
$$

holds true? In general, it is a hard question, but there are several results from Lebesgue theory to answer this precisely. In this post, I'll take some examples from Durrett [^1] 

The post is intended at someone who might have seen the definitions, but forgot the intuition.

## Notation

Let $$\mathbb{1}_{A}$$ be the indicator function over $$A$$. I use "alomst surely" and "in probability" instead of "almost everywhere" and "in measure", even if it holds for measures in general.


# Examples

## Case 1 - bounded values, unbounded support

This is example 1.5.4 from Durrett. Consider integration over the real line with borel algebra and lebesgue measure $$(\mathbb R, \mathcal R, \lambda)$$. Define the functions 

$$ f_n = \frac{1}{n}\mathbb{1}_{[0,n]} $$.

In this case, $$f_n \to 0$$ pointwise ($$f(x) \to 0 \, \forall x$$),
almost surely ($$\lambda(\left\{ x\in \mathbb R : f_n(x) \not \to 0 \}\right)=0$$), 
and in probability ($$ \forall \epsilon>0 ,\, \lambda\left( \{ x \in \mathbb R : |f_n(x)-0|>\epsilon \}\right) \to 0 $$ ).
Still the limit of the integral does not converge as we hope.

$$\int f_n d\lambda = 1 \neq 0 = \int \lim f_n d\lambda$$

From the image below, we can understand that it is the unbounded support of the functions that makes life hard for us. Since the support grows with $$n$$, there is no possibility to make this integration.

{% include image name="durrett154.svg" caption="The function, and its integral" %}

The Bounded convergence theorem (Thm 1.5.3 in Durrett) is our first main result on when convergence holds. For a function converging in probability, the function must also be bounded and have bounded support. Otherwise, the integral may not converge.

## Case 2 - bounded support, unbounded function

This time, use Example 1.5.6.

$$ f_n = n \mathbb{1}_{[0,1/n]} $$.

This time, we have convergence pointwise, almost surely and in probability. But STILL the limit of the integral is 1, and the integral of the limit is 0. This is because the function values are unbounded.

{% include image name="durrett156.svg" caption="The function, and its integral" %}

Fatous lemma (which applies whenever $$f_n \geq 0$$ ) tells us that the liminf may overshoot, just like in this situation

$$ 1=  \liminf_{n\to \infty} \int f_n \, d\mu \geq  \int \left( \liminf_{n\to \infty}  f_n \right)\, d\mu  = 0$$

## When does it work?

The second main results to establish when it works generally are the Monotone Convergence Theorem, saying that if the convergence is monotone $$f_n \nearrow f$$ for nonnegative functions $$f_n \geq 0$$, then the integral converges.

The third result is the Dominated Convergence Theorem. For functions converging $$f_n \to f$$ almost surely, we must also demand dominance $$ \lvert f_n \rvert \leq g$$, by an integrable function $$g$$ to get the convergence.

# An application in probability

You  you want to predict $$y$$ given $$x$$, being draws from the random vector $$(Y,X)$$, and you have historical data of $$n$$ data points. You construct the prediction intercal $$C_n^{\alpha}$$ so that

$$ \Pr ( Y  \in C_n^{\alpha} \lvert X=x_\star ) \to_{p} 1-\alpha $$

as is common in classical OLS prediction intervals (see section 2.4.5 in Ruppert, for example) [^2]. Will this hold even if we marginalize over $$x_\star$$?

The Bounded Convergence Theorem  says that if $$f_n \to_{p} f$$, there is some $$E \subseteq \Omega$$ so that $$\mu(E) < \infty$$, $$f_n(\omega) = 0 $$ for all $$\omega \in E$$, $$\lvert f_n \rvert \leq M$$, then

$$  \int f \, d\mu = \lim_{n\to \infty} \int f_n \, d\mu$$

We can apply this! Define $$f_n = \Pr ( Y  \in C_n^{\alpha} \lvert x=x_\star )$$, $$f = 1-\alpha$$. We have that $$\lvert f_n \rvert \leq 1$$ and $$E=\Omega$$ since $$\mu$$ is a probability measure ensures $$\mu(E) = 1 < \infty$$. Applying the theorem yields to us 

$$  \Pr ( Y  \in C_n^{\alpha} ) \to 1-\alpha $$



[^1]: R. Durrett, Probability: theory and examples, 2nd ed. Belmont, Calif: Duxbury Press, 1996.
[^2]: D. Ruppert, M. P. Wand, and R. J. Carroll, Semiparametric Regression. Cambridge University Press, 2003. doi: 10.1017/CBO9780511755453.




