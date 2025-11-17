#import "@preview/problemst:0.1.2": pset
#import math

#show: pset.with(
  class: "BMML",
  student: "Danila Biktimirov",
  title: "Theory 2",
  date: datetime(
    year: 2025,
    month: 09,
    day: 30,)
)


=

==

*Maximum likelihood estimation $theta_{M L}$*

The likelihood function $p(x | theta)$ for $N$ i.i.d. samples $x_1, dots, x_N$ from $(R)[0, theta]$ is:
$ p(x; theta) = product_{i=1}^{N} p(x_i | theta) = $
$ cases(
  (1/theta)^N \, "if" theta >= max(x_1, dots, x_N) "and" min(x_1, dots, x_N) >= 0,
  0 \, "otherwise"
) $
We want to maximize $p(x | theta)$. The function $p(x | theta) = (1/theta)^N$ is a decreasing function of $theta$. To maximize it, we must choose the smallest possible value for $theta$ that satisfies the constraint $theta >= max(x_1, dots, x_N)$.
Let $x_{max} = max(x_1, dots, x_N)$.
The maximum likelihood estimate is $theta_{M L} = x_{max}$.

*Conjugate prior and posterior distribution*

We are looking for a prior $p(theta)$ such that the posterior $p(theta|x)$ has the same functional form.
$ p(theta | x) prop p(x | theta) p(theta) $
$ p(theta | x) prop (1 / theta)^N dot I[theta >= x_{max}] dot p(theta) $
Let's use the Pareto distribution as the prior (as hinted):
$ p(theta) = "Pareto"(theta | x_m, alpha) = cases(
  (alpha x_m^alpha) / theta^(alpha+1), "if" theta >= x_m
  0 \, "if" theta < x_m
) $
Now, let's find the posterior:
$ p(theta | x) prop p(x | theta) p(theta) $
$ prop (1 / theta)^N dot I[theta >= x_{max}] dot (alpha x_m^alpha) / theta^{alpha+1} dot I[theta >= x_m] $
$ prop (1 / theta^{N + alpha + 1}) dot I[theta >= max(x_{max}, x_m)] $
This has the same functional form as the Pareto distribution.
So, the posterior distribution is:
$ p(theta | x) ~ "Pareto"(theta | max(x_{max}, x_m), N + alpha) $

==

*Statistics of Posterior Distribution*

Let the parameters of the posterior be $alpha' = N + alpha$ and $x_m' = max(x_{max}, x_m)$.
$ p(theta | x) = (alpha' (x_m')^{alpha'}) / theta^{alpha'+1}, quad theta >= x_m' $

*Expectation*

First, let's find the expectation for a general $"Pareto"(theta | x_m, alpha)$ distribution (assuming $alpha > 1$):
$ E[theta] = integral_{-inf}^{inf} theta p(theta) d theta = integral_{x_m}^{inf} theta dot (alpha x_m^alpha) / theta^{alpha+1} d theta $
$ = alpha x_m^alpha integral_{x_m}^{inf} 1 / theta^alpha d theta = alpha x_m^alpha [ theta^{-alpha+1} / (1-alpha) ]_{x_m}^{inf} $
$ = alpha x_m^alpha ( lim_{theta -> inf} theta^{1-alpha} / (1-alpha) - x_m^{1-alpha} / (1-alpha) ) $
$ = alpha x_m^alpha ( 0 - x_m^{1-alpha} / (1-alpha) ) = - (alpha x_m^{alpha + 1 - alpha}) / (1-alpha) $
$ = - (alpha x_m) / (1-alpha) = (alpha / (alpha-1)) x_m = (1 + 1/(alpha-1)) x_m $
Now, we reuse this result for our posterior parameters:
$ E[theta | x] = (alpha' / (alpha' - 1)) x_m' = ((N + alpha) / (N + alpha - 1)) max(x_{max}, x_m) $

*Median*

We need to find $m$ such that $P(theta <= m | x) = 0.5$.
This is $1 - P(theta > m | x) = 0.5$, or $P(theta > m | x) = 0.5$.
$ P(theta > m | x) = integral_m^{inf} (alpha' (x_m')^{alpha'}) / theta^{alpha'+1} d theta $
$ = alpha' (x_m')^{alpha'} [ theta^{-alpha'} / (-alpha') ]_m^infinity $
$ = alpha' (x_m')^{alpha'} ( 0 - m^{-alpha'} / (-alpha') ) $
$ = (x_m')^{alpha'} m^{-alpha'} = (x_m' / m)^{alpha'} $
Set this to $0.5$:
$ (x_m' / m)^{alpha'} = 1/2 $
$ x_m' / m = (1/2)^{1/alpha'} = 2^{-1/alpha'} $
$ m = x_m' / 2^{-1/alpha'} = x_m' dot 2^{1/alpha'} $
So, the median is:
$ "Median" = max(x_{max}, x_m) dot 2^{1 / (N + alpha)} $

*Mode*

We want to find $arg max_{theta} p(theta | x)$:
$ "mode" = arg max_{theta >= x_m'} ( (alpha' (x_m')^{alpha'}) / theta^{alpha'+1} ) $
The function $f(theta) = 1 / theta^{alpha'+1}$ is a strictly decreasing function for $theta > 0$.
The maximum value of this function on the domain $theta >= x_m'$ will be at the smallest available point, which is $theta = x_m'$.
$ "Mode" = x_m' = max(x_{max}, x_m) $

= Binomial Distribution

We have the binomial PMF:
$ "Bin"(k | n, p) = C_n^k p^k (1-p)^{n-k} $
We want to show it belongs to the exponential family, which has the form:
$ p(y | eta) = h(y) exp(eta^T u(y) - A(eta)) $
(Note: the form $g(y) exp(eta^T u(y)) / h(eta)$ is also common).

Let's rewrite the PMF:
$ "Bin"(k | n, p) = C_n^k exp( k ln p + (n-k) ln(1-p) ) $
$ = C_n^k exp( k ln p + n ln(1-p) - k ln(1-p) ) $
$ = C_n^k exp( k ln(p / (1-p)) + n ln(1-p) ) $
$ = binom(n, k) (1-p)^n exp( k dot ln(p / (1-p)) ) $

This matches the exponential family form:
* $h(k) = binom(n, k)$ (the base measure)
* $u(k) = k$ (the sufficient statistic)
* $eta = ln(p / (1-p))$ (the natural parameter)
* The term $(1-p)^n$ must be related to $A(eta)$.
    $p(k | eta) = h(k) exp(eta u(k) - A(eta))$
    $p(k | eta) = binom(n, k) exp( k eta - A(eta) )$
    Comparing, we must have $exp(-A(eta)) = (1-p)^n$.
    $A(eta) = - ln((1-p)^n) = -n ln(1-p)$

Let's express $A(eta)$ in terms of $eta$:
$ eta = ln(p / (1-p)) => e^eta = p / (1-p) $
$ e^eta (1-p) = p => e^eta - e^eta p = p $
$ e^eta = p (1 + e^eta) => p = e^eta / (1 + e^eta) $
$ 1 - p = 1 - e^eta / (1 + e^eta) = (1 + e^eta - e^eta) / (1 + e^eta) = 1 / (1 + e^eta) $
Now substitute this into $A(eta)$:
$ A(eta) = -n ln(1 / (1 + e^eta)) = n ln(1 + e^eta) $
So, the distribution is:
$ "Bin"(k | eta) = binom(n, k) exp( k eta - n ln(1 + e^eta) ) $
This is in the exponential family.

*Find $E k$ and $D k$ by differentiation*

For the exponential family, we have:
1.  
$
E[u(k)] = E[k] = A'(eta)
$
2.  
$
D[u(k)] = D[k] = A''(eta)
$

Let's differentiate $A(eta) = n ln(1 + e^eta)$:
1.  
$ E[k] = d/d eta ( n ln(1 + e^eta) ) = n dot (1 / (1 + e^eta)) dot e^eta $
    
$ E[k] = n (e^eta / (1 + e^eta)) $
    
Since $p = e^eta / (1 + e^eta)$, we have:
    $ E[k] = n p $

2.  
$ D[k] = d/d eta ( n e^eta / (1 + e^eta) ) $
    $ D[k] = n dot [ (e^eta (1 + e^eta) - e^eta (e^eta)) / (1 + e^eta)^2 ] $
    $ = n dot [ (e^eta + e^{2eta} - e^{2eta}) / (1 + e^eta)^2 ] $
    $ = n dot e^eta / (1 + e^eta)^2 $
    We can rewrite this:
    $ = n dot (e^eta / (1 + e^eta)) dot (1 / (1 + e^eta)) $
    Since $p = e^eta / (1 + e^eta)$ and $1-p = 1 / (1 + e^eta)$:
    $ D[k] = n dot p dot (1-p) $

// =

// The probabilistic model is:
// $ p(X, T, Z | w, mu, Sigma, nu) = product_{n=1}^N product_{k=1}^K [ w_k (N)(x_n | mu_k, Sigma_k / z_n) (G)(z_n | nu/2, nu/2) ]^{[t_n=k]} $
// The approximate posterior is $q(T, Z) = q_T(T) q_Z(Z) = ( product_{n=1}^N q_T(t_n) ) ( product_{n=1}^N q_Z(z_n) )$.

// The complete data log-likelihood is:
// $ log p(X, T, Z | theta) = sum_{n=1}^N sum_{k=1}^K [t_n=k] ( log w_k + log (N)(x_n | mu_k, Sigma_k / z_n) + log (G)(z_n | nu/2, nu/2) ) $
// Let's expand the terms:
// $ log (N)(x_n | mu_k, Sigma_k / z_n) = -D/2 log(2pi) - 1/2 log|Sigma_k / z_n| - 1/2 (x_n - mu_k)^T (Sigma_k / z_n)^{-1} (x_n - mu_k) $
// $ = C_1 - 1/2 log|Sigma_k| + D/2 log z_n - z_n/2 (x_n - mu_k)^T Sigma_k^{-1} (x_n - mu_k) $
// $ log (G)(z_n | nu/2, nu/2) = nu/2 log(nu/2) - log Gamma(nu/2) + (nu/2 - 1) log z_n - nu/2 z_n = C_2 + (nu/2 - 1) log z_n - nu/2 z_n $

// *E-step: Re-estimation of $q_T(T)$ and $q_Z(Z)$
// *
// We use the coordinate ascent (CAVI) update rules.

// *Update for $q_Z(Z)$*
// $ log q_Z(Z) = sum_{n=1}^N log q_Z(z_n) $
// $ log q_Z(z_n) prop E_{q_T(T)} [ log p(x_n, t_n, z_n | theta) ] $
// $ prop E_{q_T(t_n)} [ sum_{k=1}^K [t_n=k] ( log (N)(x_n | mu_k, Sigma_k / z_n) + log (G)(z_n | nu/2, nu/2) ) ] $
// $ prop E_{q_T(t_n)} [ sum_{k=1}^K [t_n=k] ( D/2 log z_n - z_n/2 Delta_{n k}^2 ) ] + (nu/2 - 1) log z_n - nu/2 z_n $
// where $Delta_{n k}^2 = (x_n - mu_k)^T Sigma_k^{-1} (x_n - mu_k)$.
// Let $r_{n k} = E_{q_T(t_n)}[[t_n=k]] = q_T(t_n=k)$.
// $ prop sum_{k=1}^K r_{n k} ( D/2 log z_n - z_n/2 Delta_{n k}^2 ) + (nu/2 - 1) log z_n - nu/2 z_n $
// $ prop ( sum_{k=1}^K r_{n k} D/2 + nu/2 - 1 ) log z_n - ( sum_{k=1}^K r_{n k} Delta_{n k}^2/2 + nu/2 ) z_n $
// Since $sum_k r_{n k} = 1$:
// $ prop ( (D + nu)/2 - 1 ) log z_n - ( nu/2 + 1/2 sum_{k=1}^K r_{n k} Delta_{n k}^2 ) z_n $
// This is the log of a Gamma distribution, $q_Z(z_n) = (G)(z_n | alpha_n, beta_n)$, with:
// $ alpha_n = (D + nu)/2 $
// $ beta_n = nu/2 + 1/2 sum_{k=1}^K r_{n k} (x_n - mu_k)^T Sigma_k^{-1} (x_n - mu_k) $

// *Update for $q_T(T)$*
// $ log q_T(T) = sum_{n=1}^N log q_T(t_n) $
// $ log q_T(t_n) prop E_{q_Z(Z)} [ log p(x_n, t_n, z_n | theta) ] $
// $ prop E_{q_Z(z_n)} [ sum_{k=1}^K [t_n=k] ( log w_k + log (N)(x_n | mu_k, Sigma_k / z_n) ) ] $
// This defines a categorical distribution $q_T(t_n=k) = r_{n k}$.
// $ log r_{n k} prop E_{q_Z(z_n)} [ log w_k + log (N)(x_n | mu_k, Sigma_k / z_n) ] $
// $ prop log w_k + E_{q_Z(z_n)} [ C_1 - 1/2 log|Sigma_k| + D/2 log z_n - z_n/2 Delta_{n k}^2 ] $
// $ prop log w_k - 1/2 log|Sigma_k| + D/2 angle.l log z_n angle.r - 1/2 angle.l z_n angle.r Delta_{n k}^2 $
// Let $log rho_{n k} = log w_k - 1/2 log|Sigma_k| + D/2 E[log z_n] - 1/2 E[z_n] (x_n - mu_k)^T Sigma_k^{-1} (x_n - mu_k)$.
// Then the update is:
// $ r_{n k} = q_T(t_n=k) = rho_{n k} / sum_{j=1}^K rho_{n j} $

// === b) M-step: Re-estimation of $w_k, mu_k, Sigma_k$

// We maximize the expected complete-data log-likelihood $(L)(q, theta) = E_q[log p(X, T, Z | theta)]$.
// $ (L)(q, theta) = sum_{n,k} r_{n k} ( log w_k + E_{q_Z(z_n)}[log (N)(dots)] + E_{q_Z(z_n)}[log (G)(dots)] ) $
// We only need the terms that depend on $w, mu, Sigma$.
// $ (L)(w, mu, Sigma) = sum_{n=1}^N sum_{k=1}^K r_{n k} ( log w_k - 1/2 log|Sigma_k| - 1/2 angle.l z_n angle.r (x_n - mu_k)^T Sigma_k^{-1} (x_n - mu_k) ) + C $

// *Update for $w_k$*
// We maximize $sum_{n,k} r_{n k} log w_k$ subject to $sum_k w_k = 1$.
// This is a standard result for mixtures. Let $N_k = sum_{n=1}^N r_{n k}$.
// $ w_k = N_k / sum_{j=1}^K N_j = (sum_{n=1}^N r_{n k}) / N $

// *Update for $mu_k$*
// We maximize $L(mu_k) = sum_{n=1}^N r_{n k} ( - 1/2 angle.l z_n angle.r (x_n - mu_k)^T Sigma_k^{-1} (x_n - mu_k) )$.
// Set the derivative $d/d mu_k L(mu_k)$ to zero:
// $ d/d mu_k L(mu_k) = sum_{n=1}^N r_{n k} ( - 1/2 angle.l z_n angle.r dot (-2) Sigma_k^{-1} (x_n - mu_k) ) = 0 $
// $ sum_{n=1}^N r_{n k} angle.l z_n angle.r Sigma_k^{-1} (x_n - mu_k) = 0 $
// $ sum_{n=1}^N r_{n k} angle.l z_n angle.r (x_n - mu_k) = 0 $
// $ sum_{n=1}^N r_{n k} angle.l z_n angle.r x_n = sum_{n=1}^N r_{n k} angle.l z_n angle.r mu_k $
// $ mu_k = ( sum_{n=1}^N r_{n k} angle.l z_n angle.r x_n ) / ( sum_{n=1}^N r_{n k} angle.l z_n angle.r ) $

// *Update for $Sigma_k$*
// We maximize $L(Sigma_k) = sum_{n=1}^N r_{n k} ( - 1/2 log|Sigma_k| - 1/2 angle.l z_n angle.r (x_n - mu_k)^T Sigma_k^{-1} (x_n - mu_k) )$.
// Set the derivative $d/d Sigma_k L(Sigma_k)$ to zero (using matrix derivatives):
// $ d/d Sigma_k L(Sigma_k) = sum_{n=1}^N r_{n k} ( - 1/2 Sigma_k^{-1} - 1/2 angle.l z_n angle.r (-Sigma_k^{-1} (x_n - mu_k)(x_n - mu_k)^T Sigma_k^{-1}) ) = 0 $
// $ sum_{n=1}^N r_{n k} Sigma_k^{-1} = sum_{n=1}^N r_{n k} angle.l z_n angle.r Sigma_k^{-1} (x_n - mu_k)(x_n - mu_k)^T Sigma_k^{-1} $
// Multiply by $Sigma_k$ from left and right:
// $ (sum_{n=1}^N r_{n k}) Sigma_k = sum_{n=1}^N r_{n k} angle.l z_n angle.r (x_n - mu_k)(x_n - mu_k)^T $
// $ Sigma_k = ( sum_{n=1}^N r_{n k} angle.l z_n angle.r (x_n - mu_k)(x_n - mu_k)^T ) / ( sum_{n=1}^N r_{n k} ) $
// $ Sigma_k = ( sum_{n=1}^N r_{n k} E[z_n] (x_n - mu_k)(x_n - mu_k)^T ) / N_k $

// *Check for K=1*
// If $K=1$, then $r_{n 1} = 1$ for all $n$, and $w_1 = 1$. $N_1 = N$.
// $ mu_1 = ( sum_n angle.l z_n angle.r x_n ) / ( sum_n angle.l z_n angle.r ) $
// $ Sigma_1 = ( sum_n angle.l z_n angle.r (x_n - mu_1)(x_n - mu_1)^T ) / N $
// These are the update rules for fitting a single Student-t distribution, which transform to the formulas for a Gaussian mixture model if we set $E[z_n] = 1$. The formulas from the seminar would be for a GMM, where these reduce to the standard weighted $M L$ estimates for $mu_k$ and $Sigma_k$ if $angle.l z_n angle.r$ is replaced by 1.

// === c) Evidence Lower Bound (ELBO) and Necessary Statistics

// The ELBO is $(L)(q, theta) = E_q[log p(X, T, Z | theta)] - E_q[log q(T, Z)]$.
// $ (L)(q, theta) = E_q[log p(X, T, Z | theta)] - E_q[log q_T(T)] - E_q[log q_Z(Z)] $

// $ E_q[log p(X, T, Z | theta)] = sum_{n,k} r_{n k} ( log w_k + E_{q_Z(z_n)}[log (N)(dots)] + E_{q_Z(z_n)}[log (G)(dots)] ) $
// $ = sum_{n,k} r_{n k} ( log w_k - 1/2 log|Sigma_k| + D/2 angle.l log z_n angle.r - 1/2 angle.l z_n angle.r Delta_{n k}^2 ) $
// $ + sum_n ( nu/2 log(nu/2) - log Gamma(nu/2) + (nu/2 - 1) angle.l log z_n angle.r - nu/2 angle.l z_n angle.r ) + C $

// $ E_q[log q_T(T)] = sum_n E_{q_T(t_n)}[log q_T(t_n)] = sum_{n,k} r_{n k} log r_{n k} $
// $ E_q[log q_Z(Z)] = sum_n E_{q_Z(z_n)}[log q_Z(z_n)] $
// $ E[log q_Z(z_n)] = E[log (G)(z_n | alpha_n, beta_n)] = alpha_n log beta_n - log Gamma(alpha_n) + (alpha_n - 1) angle.l log z_n angle.r - beta_n angle.l z_n angle.r $

// Combining all terms gives the ELBO.

// *Necessary Statistics*

// The formulas in (a) and (b) depend on statistics of the $q$ distributions.
// 1.  **From $q_T(T)$:**
//     The necessary statistic is $E[[t_n=k]]$.
//     $ E_{q_T(t_n)}[[t_n=k]] = q_T(t_n=k) = r_{n k} $
// 2.  **From $q_Z(Z)$:**
//     $q_Z(z_n) = (G)(z_n | alpha_n, beta_n)$ with $alpha_n = (D+nu)/2$ and $beta_n = nu/2 + 1/2 sum_k r_{n k} Delta_{n k}^2$.
//     The necessary statistics are $E[z_n]$ and $E[log z_n]$.
//     For a Gamma$(alpha, beta)$ distribution:
//     $ E[z_n] = alpha_n / beta_n = ((D+nu)/2) / ( nu/2 + 1/2 sum_k r_{n k} (x_n - mu_k)^T Sigma_k^{-1} (x_n - mu_k) ) $
//     $ E[log z_n] = psi(alpha_n) - log(beta_n) = psi((D+nu)/2) - log( nu/2 + 1/2 sum_k r_{n k} (x_n - mu_k)^T Sigma_k^{-1} (x_n - mu_k) ) $
//     where $psi(dot)$ is the digamma function.