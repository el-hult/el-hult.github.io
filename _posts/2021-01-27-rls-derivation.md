---
layout: post
title:  "Update equations for Recursive Least Squares"
---
The Recursive Least Squares (RLS) method is commonly used, but I did not find any derivation of it that suited me. 
Since I did the derivation for my own sake, I thought I would share it.
I'll do the derivation first, and then comment om some details.


This section therefore is simply a derivation of the RLS update equations for weighted least squares with forgetting and regularizing initialization.
I rely on the presentation in [this tutorial by Arvind Yedla](http://pfister.ee.duke.edu/courses/ece586/ex_proj_2008.pdf), but do some with minor tweaks and changes in notation.
You are given a scalar series \\((y_t)_{t=1}^{t_{max}}\\) and a vector valued time series \\((z_t)_{t=1}^{t_{max}}\\). The task is to compute
\[
\label{eq:rls:optim} \theta_t := \text{arg min}_\theta \frac{1}{2} \sum_{s=1}^{t} \lambda^{t-s} |y_{s} - \theta^T z_{s} |^2 + \frac{\lambda^t\delta}{2} |\theta|^2 \tag{1} \]
repeatedly for increasing $t$. The two tuning parameters are $\lambda$ and \\(\delta\\).
The objective function is first cast into vector notation by means of a weight matrix \\(\Lambda_t = \text{diag}(\lambda^0,\lambda^1,...\lambda^t)\\).
Define \\(\vec y_t\\) to be the vector of \\((y_s)_{s=1}^{t}\\) up to time \\(t\\). Let $\vec z_t$ be a matrix with \\((z_s^T)_{s=1}^{t}\\) as the rows. This recasts the problem as
\[ \theta_t := \text{argmin}_\theta \frac{1}{2} (\vec y_t -  \vec z_t \theta)^T \Lambda_t (\vec y_t - \vec z_t \theta) + \frac{\lambda^t\delta}{2} \theta^T \theta \]
We let $I$ denote an appropriately sized identity matrix. 

Diffrentiating and setting zero yields the equation
\begin{equation} \theta_t = \left(\vec z_t^T \Lambda_t\vec z_t + \lambda^t\delta I \right)^{-1} \vec z_t\Lambda_t \vec y_t  \tag{2} \end{equation}

This can be recursively be computed via the use of
\[ \vec p_t :=\vec z_t\Lambda_t \vec y_t = \lambda \vec p_{t-1 }+ z_ty_t\]
\[ R_t := \left(\vec z_t^T \Lambda_t\vec z_t + \lambda^t \delta I \right)  = \lambda R_{t-1} + z_tz_t^T \]
and with the [Sherman–Morrison formula](https://en.wikipedia.org/wiki/Sherman%E2%80%93Morrison_formula), we can compute
\[P_t:=R_t^{-1} = \lambda^{-1} \left( R_{t-1} +\lambda^{-1} z_tz_t^T   \right)^{-1} = \lambda^{-1}P_{t-1} - \lambda^{-1}\frac{P_{t-1} z_t z_t^T P_{t-1} }{\lambda+ z_t^T P_{t-1}z_t } \]
very efficiently. We may also introduce the _Kalman gain_ \\(\vec k_t := \frac{P_{t-1} z_t}{\lambda+ z_t^T P_{t-1}z_t }\\) so that \\(P_t = (I- \vec k_t z_t^T)\lambda^{-1}P_{t-1}\\).  That allows some simplifications of equation (2).



\begin{align}
	\theta_t
	 & = \left(\vec z_t^T \Lambda_t\vec z_t + \lambda^t\delta I \right)^{-1} \vec z_t\Lambda_t \vec y_t                                                      \\\\
	 & = P_t \vec p_t                                                                                                                                            \\\\
	 & = ( I- \vec k_t z_t^T)\lambda^{-1}P_{t-1}\left[ \lambda \vec p_{t-1} + z_ty_t \right]                                                                \\\\
	 & = ( I- \vec k_t z_t^T)\left[ \theta_{t-1} + \lambda^{-1}P_{t-1}z_ty_t \right]                                                                        \\\\
	 & =   \theta_{t-1} + \lambda^{-1}P_{t-1}z_ty_t - \vec k_t z_t^T\left[ \lambda \theta_{t-1} + \lambda^{-1}P_{t-1}z_ty_t \right]                             \\\\
	 & =   \theta_{t-1} + \lambda^{-1}P_{t-1}z_ty_t - \vec k_t \left[\hat y_t + \lambda^{-1} z_t^T P_{t-1}z_ty_t \right]                                        \\\\
	 & =   \theta_{t-1} + \lambda^{-1} \vec k_t y_t\left[\lambda+ z_t^T P_{t-1}z_t \right] - \vec k_t \left[\hat y_t + \lambda^{-1}z_t^T P_{t-1}z_ty_t \right] \\\\
	 & =   \theta_{t-1} + \vec k_t \left[y_t - \hat y_t \right]
\end{align}

We finally introduce the _prediction error_ or _innovation_ \\(e_t := y_t - \hat y_t\\) and arrive at our final update equation
\[ \theta_t = \theta_{t-1}+\vec k_t e_t\]

We initialize with \\(P_0 = I \frac{1}{\delta}\\) and \\(\theta_0 = \vec 0\\).

## Remark
In equation (1) we have a simple least squares objective plus a regularizing term. If not the regularizing term was vanishing with increasing \\(t), it would be a ridge regression problem.

By not having a vanishing regularization like this, we cannot make the simple recursive formulation with rank one updates by the Sherman-Morrison formula. We are thus forced to have this vanishin regularization if we want fast simple updates.

Online ridge regression is a technique that has been studied, but is in the field of online convex optimization, and not typically studied in control or statistics.

If the forgetting factor \\(\lambda=1\\), then the regularizing term will never vanish and we do get a online ridge problem.

