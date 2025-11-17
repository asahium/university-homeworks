#import "@preview/problemst:0.1.2": pset
#import math

#show: pset.with(
  class: "BMML",
  student: "Danila Biktimirov",
  title: "Theory 1",
  date: datetime(
    year: 2025,
    month: 09,
    day: 30,)
)

= Simplify the following expressions:

== (a) // $norm(u v^T - A)_F^2 - norm(A)_F^2$

$
norm(u v^T - A)_F^2 - norm(A)_F^2 =
tr((u v^T - A)^T (u v^T - A)) - tr(A^T A) = \
= tr((u v^T)^T (u v^T)) - 2tr(A^T (u v^T)) + tr(A^T A) - tr(A^T A) \
= tr(v u^T u v^T) - 2tr(A^T u v^T) = \
= tr(v (u^T u) v^T) - 2 u^T A v = \
= norm(u)^2 norm(v)^2 - 2 u^T A v
$

== (b) // $tr((2 I_n + a a^T)^(-1) (u v^T + v u^T))$

$
tr((2 I_n + a a^T)^-1 (u v^T + v u^T)) = \
= "tr"([ (1/2 I_n - (1/4) a (1 + 1/2 a^T a)^-1 a^T) (u v^T + v u^T) ]) \
= "tr"([ (1/2 I_n - (a a^T) / (4 + 2 a^T a)) (u v^T + v u^T) ]) \
= "tr"( 1/2 u v^T + 1/2 v u^T - (a a^T u v^T)/(4 + 2 a^T a) - (a a^T v u^T)/(4 + 2 a^T a) ) \
= 1/2 "tr"(u v^T) + 1/2 "tr"(v u^T) - 1/(4 + 2 a^T a) ["tr"(a a^T u v^T) + "tr"(a a^T v u^T)] \
= 1/2 v^T u + 1/2 u^T v - 1/(4 + 2 a^T a) [ (v^T a)(a^T u) + (u^T a)(a^T v) ] \
= u^T v - (2 (a^T u)(a^T v)) / (4 + 2 a^T a) \
= u^T v - ((a^T u)(a^T v)) / (2 + a^T a)
$

== (c) // $sum_(i=1)^n < S^(-1) a_i, a_i >$ where $a_1, ..., a_n in RR^d$, $S = sum_(i=1)^n a_i a_i^T$, $det(S) != 0$.

$
sum_(i=1)^n < S^(-1) a_i, a_i > = sum_(i=1)^n a_i^T S^(-1) a_i = tr(S^(-1) sum_(i=1)^n a_i a_i^T) = tr(S^(-1) S) = d
$

#pagebreak()

= For each of the following functions, find its first derivative using the technique of differentials:

== (a) // $f(t) = det(A - t I_n)$

Let $M(t) = A - t I_n$, so that: $f(t) = det(M(t))$ and $M'(t) = -I_n$. 

And we know that: \
$
(d)/(d t) det(M(t)) = det(M(t)) dot tr(M(t)^(-1) M'(t)) => \
=> (d)/(d t) det(A - t I_n) = -det(A - t I_n) dot tr((A - t I_n)^(-1))
$

== (b) // $f(t) = norm((A + t I_n)^(-1) b)$

Let $g(t) = (A + t I_n)^(-1) b$; \
$
(d g(t))/(d t) = -(A + t I_n)^(-1) (A + t I_n)^(-1) b
$ 
$
f(t) = norm(g(t)) = (g(t)^T g(t))^(1/2)
$ 
$
(d f)/(d t) = (g(t)^T (d g(t))/(d t)) / (norm(g(t))) =\
= -(g(t)^T (A + t I_n)^(-1) (A + t I_n)^(-1) b) / (norm(g(t))) =\
= -(b^T (A + t I_n)^(-1) (A + t I_n)^(-1) b) / (norm((A + t I_n)^(-1) b))
$

#pagebreak()

= For each of the following functions, find its gradient $nabla f$;

== (a) // $f(x) = 1/2 norm(x x^T - A)_F^2$

$
"Let " A = (2 I_n + a a^T)^-1 #h(1em) " and " #h(1em) X = u v^T + v u^T.\
" We want to find " "tr"(A X).\

// First, simplify A using the Woodbury matrix identity.
A = (2I_n)^-1 - (2I_n)^-1 a (1 + a^T (2I_n)^-1 a)^-1 a^T (2I_n)^-1 \
=> A = 1/2 I_n - 1/4 a (1 + 1/2 a^T a)^-1 a^T \
=> A = 1/2 I_n - a a^T / (4 + 2 a^T a)

// Now, substitute A back into the trace.
"tr"(A X) = "tr"((1/2 I_n - (a a^T)/(4 + 2 a^T a)) (u v^T + v u^T))\

// Distribute and use linearity of trace.
=> "tr"(1/2(u v^T + v u^T)) - "tr"(((a a^T)(u v^T + v u^T))/(4 + 2 a^T a))\

// Evaluate the first term. tr(u v^T) = v^T u.
"tr"(1/2(u v^T + v u^T)) = 1/2(v^T u + u^T v) = u^T v\

// Evaluate the second term using the cyclic property of trace.
"tr"(a a^T u v^T) = "tr"(v^T a a^T u) = (v^T a)(a^T u)\
"tr"(a a^T v u^T) = "tr"(u^T a a^T v) = (u^T a)(a^T v)\

// Combine the results.
=> "tr"(A X) = u^T v - ((v^T a)(a^T u) + (u^T a)(a^T v)) / (4 + 2 a^T a)\

// Since the terms are scalar products, they commute.
=> u^T v - (2(a^T u)(a^T v)) / (4 + 2 a^T a)

// Final simplified form.
=> u^T v - ((a^T u)(a^T v)) / (2 + a^T a)
$

== (b) // $f(x) = <x, x>^(<x, x>)$

Let $f(x) = <x, x> ^ (<x, x>) = (x^T x)^(x^T x)$.

Define $u(x) = x^T x = ||x||^2$. Thus, $f(x) = u^u$.

By the chain rule, the gradient is $nabla f(x) = (d f)/(d u) nabla u$.
$
// Step 1: Differentiate f with respect to the scalar u.
(d f)/(d u) = d/(d u) (u^u) = d/(d u) e^(u ln u) = e^(u ln u) * (1 * ln u + u * 1/u) = u^u(ln u + 1).\

// Step 2: Find the gradient of u with respect to the vector x.
nabla u = nabla (x^T x) = 2x.

// Step 3: Combine the results and substitute u back.
nabla f(x) = [u^u(ln u + 1)] * (2x) \
=> nabla f(x) = [(||x||^2)^(||x||^2) (ln(||x||^2) + 1)] * 2x

// Final expression for the gradient.
nabla f(x) = 2(||x||^2)^(||x||^2) (ln(||x||^2) + 1) x.
$

== (c) // $f(x) = norm(A x - b)^p$
$
f(x) = norm(A x - b)^p = (sum_(i=1)^m abs((A x - b)_i)^2)^(p/2) \
"Let" z = A x - b => f(x) = norm(z)^p
nabla f(x) = p norm(z)^(p-2) nabla norm(z)^2 \
nabla norm(z)^2 = nabla(z^T z) = 2 z^T nabla z \
nabla z = A => nabla norm(z)^2 = 2 (A x - b)^T A \
nabla f(x) = p norm(A x - b)^(p-2) A^T (A x - b) 
$

#pagebreak()

= For each of the following functions, find all stationary points (i.e. points where the gradient is zero) and indicate conditions when they exist:

== (a) // $f(x) = <c, x> + sigma/3 norm(x)^3$

$ 
nabla(< c, x>) = c \
nabla(sigma/3 norm(x)^3) = sigma norm(x) x \
=> nabla f(x) = c + sigma norm(x) x \
c + sigma norm(x) x = 0 \
sigma norm(x) x = -c \
sigma norm(x)^2 = norm(c) \
norm(x) = sqrt(norm(c) / sigma) \
dot(x) = -c / sqrt(sigma norm(c)) ("always" exists).
$

== (b) // $f(x) = <a, x> - ln(1 - <b, x>)$

To find the stationary point, we set the gradient of $f(x)$ to zero:
$
nabla f(x) = a + b / (1 - <b, x>) = 0 ==> b/(1 - <b, x>) = -a.
$

Taking the dot product with $b$ on both sides yields:
$
<b, b/(1 - <b, x>)> = -<b, a> ==> ||b||^2/(1 - <b, x>) = -<b, a>.
$

For the logarithm in $f(x)$ to be defined, we need $1 - <b, x> > 0$. The equation above shows this is equivalent to $-(||b||^2)/(<b, a>) > 0$. Since $||b||^2 >= 0$, this condition holds if and only if $<b, a> < 0$.

Under this condition, we can solve for $<b, x>$:
$
<b, x> = 1 + (||b||^2)/(<b, a>).
$

== (c) // $f(x) = <c, x> exp(-<A x, x>)$

The function is $f(x) = <c, x> exp(-<A x, x>)$. To find stationary points, we set its gradient to zero.

Using the product rule, the gradient is:
$ nabla f(x) = exp(-<A x, x>) (c - 2<c, x>A x) $

Since $exp(-<A x, x>) > 0$, we set the other term to zero:
$ c - 2<c, x>A x = 0 ==> c = 2<c, x>A x $

Let the scalar be $lambda = 2<c, x>$. The equation becomes $c = lambda A x$. Since $A$ is in $S_{++}^n$, it's invertible, so $x = (1/lambda) A^(-1)c$. Note $lambda!=0$ because $c!=0$.

Substitute $x$ back into the definition of $lambda$:
$ lambda = 2<c, (1/lambda)A^(-1)c> = (2/lambda)<c, A^(-1)c> $
$ ==> lambda^2 = 2<c, A^(-1)c> $
$ ==> lambda = +- sqrt(2<c \, A^(-1)c>) $

This gives two stationary points:
$ x = +- (A^(-1) c)/sqrt(2<c \, A^(-1)c>) $

*Existence:* Since $A$ is positive definite and $c != 0$, we have $<c, A^(-1)c> > 0$. Therefore, the two stationary points *always exist* under the given conditions.

#pagebreak()

= Solve the following optimization problem: $min_(X in S_(++)^n) sum_(i=1)^m < X^(-1) a_i, a_i> + ln det(X)$ where $a_1, ..., a_m in RR^n$.

We find the stationary point by setting the gradient to zero:
$ nabla_X f(X) = X^(-1) - X^(-1) (sum_(i=1)^m a_i a_i^T) X^(-1) = 0 $

This simplifies to:
$ X^(-1) = X^(-1) (sum_(i=1)^m a_i a_i^T) X^(-1) $

Since $X in S_(++)^n$, it is invertible. Pre- and post-multiplying by $X$ isolates the solution:
$ X = sum_(i=1)^m a_i a_i^T $

This solution is the minimizer. It exists within the domain $S_(++)^n$ if and only if the resulting matrix $X$ is positive definite, which requires that the set of vectors ${a_1, ..., a_m}$ must span $RR^n$.

#pagebreak()

= 6. Let's consider the Principal Component Analysis (PCA) approach. Suppose we are given a training dataset ${x_i}_(i=1)^N, x_i in RR^D$ and we want to reduce it to a dataset of lower dimensionality d using projection to a linear subspace that is determined by matrix $P in RR^(D times d)$. Orthogonal projection of a vector to this space can be calculated as $P (P^T P)^(-1) P^T x$. Then to find the best matrix P we may consider the following optimization problem: $ F(P) = sum_(i=1)^N norm(x_i - P (P^T P)^(-1) P^T x_i)^2 = N tr((I - P (P^T P)^(-1) P^T)^2 S) -> min_P, $ where $S = 1/N sum_(i=1)^N x_i x_i^T$ is the sample covariance matrix for the normalized dataset.

== (a) Find gradient $nabla_P F(P)$, calculated for arbitrary matrix with orthogonal columns, i.e., P: $P^T P = I$ (Note: you should first compute differential $d F(P)$ for arbitrary matrix P and only then use orthogonality property of its columns in obtained expression.)

$
F(P) = N dot tr[(I - P(P^T P)^(-1) P^T)^2 S] = N dot tr[d[(I - P(P^T P)^(-1) P^T)^2 S]] \
d F(P) = N dot tr[2(I - P(P^T P)^(-1) P^T)(-d[P(P^T P)^(-1) P^T])S] \
d[P(P^T P)^(-1) P^T] = d P(P^T P)^(-1) P^T - P(P^T P)^(-1) d(P^T P) (P^T P)^(-1) P^T + P(P^T P)^(-1) d P^T \
d F(P) = -2N dot tr[(I - P(P^T P)^(-1) P^T)(d P(P^T P)^(-1) P^T -\
-P(P^T P)^(-1) d(P^T P) (P^T P)^(-1) P^T + P(P^T P)^(-1) d P^T)S] \
P^T P = I => (P^T P)^(-1) = I "and" d(P^T P) = 0 \
d F(P) = -2N dot tr[(I - P P^T)(d P P^T + P d P^T)S] = \
= -2N dot [tr(d P P^T S (I - P P^T)) + tr(P d P^T S (I - P P^T))] = tr(nabla_P F dot d P)\
nabla_P F(P) = -2N[S P - P P^T S P]
$

// == (b) Let's consider the eigenvalue decomposition of matrix S: $S = Q Lambda Q^T$ where Lambda is a diagonal matrix with eigenvalues on its diagonal, $Q = [q_1 | q_2 | ... | q_D] in RR^(D times D)$ is an orthogonal matrix with columns determined by eigenvectors $q_i$. Prove that the gradient $nabla_P F(P)$ equals zero for matrix P consisting of any d different eigenvectors $q_i$. Also prove that the minimum value of $F(P)$ is obtained for matrix P consisting of eigenvectors $q_i$ that correspond to the highest eigenvalues of matrix S.

// $F(P) = N dot tr[(I - P P^T)^2 S]$ \
// As eigenvectors are orthogonal, $P P^T$ is a projection matrix onto the subspace spanned by these eigenvectors: \
// $ P P^T = sum_(k=1)^d q_(i_k) q(i_k)^T. $ \
// Substituting this into the expression for the gradient $nabla_P F(P)$, we recall that the gradient is given by: \
// $ nabla_P F(P) = -2N[S P - P P^T S P]. $ \
// Using the fact that $S P = P Lambda_P$, where $Lambda_P$ is the diagonal matrix of eigenvalues corresponding to the eigenvectors in P, we get: \
// $ S P - P P^T S P = P Lambda_P - P P^T P Lambda_P = P Lambda_P - P Lambda_P = 0. $ \
// Thus, the gradient $nabla_P F(P)$ equals zero, which means that any matrix P consisting of eigenvectors of S is a critical point of the function. \
// Next, to find the minimum value of $F(P)$, we observe that the function $F(P)$ minimizes the term $(I - P P^T)^2 S$. Since $S = Q Lambda Q^T$, the matrix $Lambda$ contains the eigenvalues of S, and the projection $P P^T S P$ captures the variance corresponding to the eigenvalues of the eigenvectors chosen for P. To minimize $F(P)$ we need to maximize the variance captured by $P P^T S P$, which occurs when the eigenvectors associated with the largest eigenvalues are selected for P. Hence, the minimum value of $F(P)$ is obtained when P consists of the eigenvectors corresponding to the largest eigenvalues of S.