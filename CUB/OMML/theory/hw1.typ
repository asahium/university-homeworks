#set document(
  title: "Homework 1",
  author: "Danila Biktimirov",
  date: auto
)
#set text(font: "Linux Libertine", lang: "en")
#set heading(numbering: "1.")
// #set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 20pt, weight: "bold")[Optimization Methods in Machine Learning, CUB, Spring 2026]
  #v(0.01em)
  #text(size: 16pt)[Theory 1. Convergence speed and second differential.]
  #v(0.01em)
  #text(size: 12pt)[
    Danila Biktimirov
  ]
  #v(0.01em)
  February 17, 2026
]

= Problem 1

*For each of the following sequences ${r_k}$ find out its convergence speed (linear, sublinear, superlinear). In case of superlinear rate find out additionally whether the sequence has quadratic convergence rate.*

== (a) $r_k = (0.99)^(k^2)$

$ frac(r_(k+1), r_k) = frac((0.99)^((k+1)^2), (0.99)^(k^2)) = (0.99)^(2k+1). $

Since $lim_(k -> infinity) (0.99)^(2k+1) = 0$, the convergence is superlinear.

$ frac(r_(k+1), r_k^2) = (0.99)^((k+1)^2 - 2k^2) = (0.99)^(-k^2 + 2k + 1) -> infinity, $

since the exponent $-k^2 + 2k + 1 -> -infinity$ and the base $0.99 < 1$.

Superlinear convergence (not quadratic).

== (b) $r_k = (0.99)^(2^k)$
$ frac(r_(k+1), r_k) = frac((0.99)^(2^(k+1)), (0.99)^(2^k)) = (0.99)^(2^k) -> 0. $

The convergence is superlinear. Check quadratic:

$ frac(r_(k+1), r_k^2) = frac((0.99)^(2^(k+1)), ((0.99)^(2^k))^2) = frac((0.99)^(2^(k+1)), (0.99)^(2^(k+1))) = 1. $

The limit is exactly $1$ (a positive constant).

Quadratic convergence.

== (c) $r_k = 1 / k!$

$ frac(r_(k+1), r_k) = frac(k!, (k+1)!) = frac(1, k+1) -> 0. $

Superlinear. Check quadratic:

$ frac(r_(k+1), r_k^2) = frac((k!)^2, (k+1)!) = frac(k!, k+1) -> infinity. $

Superlinear convergence (not quadratic).

== (d) $r_k = 1 / k^k = k^(-k)$

$ frac(r_(k+1), r_k) = frac(k^k, (k+1)^(k+1)) = frac(1, k+1) dot frac(1, (1 + 1\/k)^k) -> 0 dot frac(1, e) = 0. $

Superlinear. Check quadratic:

$ ln frac(r_(k+1), r_k^2) = 2k ln k - (k+1) ln(k+1) approx k ln k -> infinity. $

Superlinear convergence (not quadratic).

== (e) $ r_k = cases(
  (0.99)^(2^k) &"if" k "is even",
  r_(k-1) \/ k &"if" k "is odd".
) $

-$k$ even:
$ frac(r_(k+1), r_k) = frac(r_k \/ (k+1), r_k) = frac(1, k+1) -> 0. $

-$k$ odd, so $k+1$ even:
$ frac(r_(k+1), r_k) = frac((0.99)^(2^(k+1)), (0.99)^(2^(k-1)) \/ k) = k dot (0.99)^(2^(k+1) - 2^(k-1)) -> 0. $

So the convergence is superlinear. Check quadratic at $k$ even:

$ frac(r_(k+1), r_k^2) = frac(r_k \/ (k+1), r_k^2) = frac(1, (k+1) r_k) = frac(1, (k+1)(0.99)^(2^k)) -> infinity. $

Superlinear convergence (not quadratic). The even subsequence is quadratic, but the odd steps break the quadratic rate for the full sequence.

= Problem 2

*Suppose that ${r_k}$ is a sequence of non-negative values given by $r_(k+1) = M r_k^2$, where $M > 0$, $r_0 >= 0$. Find necessary and sufficient condition for $M$ and $r_0$, when the sequence converges to zero. What would be the convergence rate in this case?*

Take logarithms: let $y_k = ln r_k$:

$ y_(k+1) = 2 y_k + ln M. $

The general solution is $y_k = c dot 2^k - ln M$ with $c = ln(M r_0)$. Exponentiating:

$ r_k = frac(1, M) (M r_0)^(2^k). $

$r_k -> 0$ if and only if $abs(M r_0) < 1$, i.e.:

$ r_0 < 1 / M. $

$ frac(r_(k+1), r_k^2) = frac(M r_k^2, r_k^2) = M = "const" > 0. $

Quadratic convergence when $r_0 < 1\/M$.

= Problem 3

*For each of the following functions find out the second differential $d^2 f(x)[d x, d x]$ and show that this differential has constant sign. Find out also whether this sign is strict for all $d x != 0$ or not.*

== (a) $f(x) = ln(-1/2 x^top A x - b^top x - c)$, where $A$ is non-negatively definite and the function is considered only for those values of $x$ where the expression under logarithm is strictly positive.

Let $u(x) = -1\/2 x^top A x - b^top x - c > 0$.

$ d f = frac(d u, u) = frac(-(x^top A + b^top) d x, u). $

$ d^2 f = frac(u dot (-d x^top A d x) - (-(A x + b)^top d x)^2, u^2). $

$ d^2 f[d x, d x] = -frac(1, u^2) [u (d x^top A d x) + ((A x + b)^top d x)^2]. $

Since $A succ.eq 0$ we have $d x^top A d x >= 0$, and $u > 0$, and the squared term $>= 0$. The overall factor is $-1\/u^2 < 0$.

$ d^2 f[d x, d x] <= 0 quad ==> quad "concave". $

The sign is not necessarily strict: if $d x in ker A$ and $(A x + b)^top d x = 0$, then $d^2 f = 0$ for $d x != 0$.

== (b) $f(x) = (sum_(i=1)^n x_i^p)^(1\/p)$, where $p < 1$, $p != 0$, $x_i > 0$ for all $i$.

Let $S = sum x_i^p$, so $f = S^(1\/p)$.

$ d f = S^(1\/p - 1) sum x_i^(p-1) d x_i. $

$ d^2 f = (1-p) S^(1\/p - 2) [(sum x_i^(p-1) d x_i)^2 - S sum x_i^(p-2) (d x_i)^2]. $

By Cauchy--Schwarz with $u_i = x_i^(p\/2)$, $v_i = x_i^(p\/2 - 1) d x_i$:

$ (sum u_i v_i)^2 <= (sum u_i^2)(sum v_i^2) quad ==> quad (sum x_i^(p-1) d x_i)^2 <= S dot sum x_i^(p-2) (d x_i)^2. $

The bracket is $<= 0$, the prefactor $(1-p) S^(1\/p - 2) > 0$ (since $p < 1$).

$ d^2 f[d x, d x] <= 0 quad ==> quad "concave". $

The sign is strict for $d x != 0$ unless $d x_i prop x_i$ (Cauchy--Schwarz equality condition).

== (c) $f(X) = op("tr")(X^(-1) A)$, where $X$ is positive definite and $A$ is non-negative definite.

Using $d(X^(-1)) = -X^(-1) (d X) X^(-1)$:
$ d f = -op("tr")(X^(-1) A X^(-1) d X). $

$ d^2 f = 2 op("tr")(X^(-1) d X X^(-1) A X^(-1) d X). $

Let $Y = X^(-1\/2) d X X^(-1\/2)$ and $B = X^(-1\/2) A X^(-1\/2) succ.eq 0$. Then:

$ d^2 f = 2 op("tr")(B Y^2) >= 0, $

since $B succ.eq 0$ and $Y^2 succ.eq 0$, and the trace of two PSD matrices is non-negative.

$ d^2 f[d X, d X] >= 0 quad ==> quad "convex". $

If $A succ 0$ then $B succ 0$, and $op("tr")(B Y^2) = 0$ only when $Y = 0$ (i.e. $d X = 0$), so the sign is strict. If $A$ is only $succ.eq 0$ (singular), the sign is not necessarily strict.

== (d) $f(X) = (det X)^(1\/n)$, where $X$ is positive definite.

Using $d(det X) = (det X) op("tr")(X^(-1) d X)$:
$ d f = frac(1, n) f(X) op("tr")(X^(-1) d X). $

$ d^2 f = frac(f(X), n) [frac(1, n) (op("tr")(X^(-1) d X))^2 - op("tr")((X^(-1) d X)^2)]. $

Let $M = X^(-1\/2) d X X^(-1\/2)$ with eigenvalues $lambda_1, ..., lambda_n$. Then $op("tr")(M) = sum lambda_i$ and $op("tr")(M^2) = sum lambda_i^2$. By Cauchy--Schwarz:

$ frac(1, n) (sum lambda_i)^2 <= sum lambda_i^2. $

So the bracket is $<= 0$, and $f(X)\/n > 0$.

$ d^2 f[d X, d X] <= 0 quad ==> quad "concave". $

The sign is strict for $d X != 0$ unless all $lambda_i$ are equal, i.e. $d X prop X$.

= Problem 4

*Let $f(x) = (x^top A x) / (norm(x)^2)$, where $A$ is a symmetric matrix and $x != 0$. Show that all stationary points of this function are determined by eigenvectors of the matrix $A$. Find the Hessian $nabla^2 f(x)$ for eigenvectors $x$. Determine the type of stationarity (local minima, local maxima, saddle point).*

$ nabla f(x) = frac(2, x^top x) (A x - f(x) x). $

Setting $nabla f = 0$ gives $A x = lambda x, quad lambda = f(x)$. The stationary points are the eigenvectors of $A$, and the values are the corresponding eigenvalues.

At a stationary point $v$ with $A v = lambda v$, $nabla f(v) = 0$:

$ nabla^2 f(v) = frac(2, v^top v) (A - lambda I). $

Let $lambda_1 <= lambda_2 <= ... <= lambda_n$ be the eigenvalues of $A$.

-$lambda = lambda_1$ (minimum eigenvalue): $A - lambda_1 I$ has eigenvalues $lambda_j - lambda_1 >= 0$. Hessian is PSD $==>$ local (and global) minimum.

-$lambda = lambda_n$ (maximum eigenvalue): $A - lambda_n I$ has eigenvalues $lambda_j - lambda_n <= 0$. Hessian is NSD $==>$ local (and global) maximum.

-$lambda = lambda_k$, $1 < k < n$: $A - lambda_k I$ has both positive and negative eigenvalues $==>$ saddle point.
