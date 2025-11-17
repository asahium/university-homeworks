#import "@preview/problemst:0.1.2": pset
#import math

#show: pset.with(
  class: "BMML",
  student: "Danila Biktimirov",
  title: "Practice 1 - Variant 1",
  date: datetime(
    year: 2025,
    month: 09,
    day: 30,)
)

=
== Model 1

$
p(a, b, c, d) &= p(d|c)p(c|a, b)p(a)p(b)
$ 

$
d|c ~ c + "Bin"(c, p_3)
$

$
c|a, b ~ "Bin"(a, p_1) + "Bin"(b, p_2)
$

$
a ~ "Unif"[a_min, a_max}]
$

$
b ~ "Unif"[b_min, b_max]
$

=== $p(a)$
$
p(a) &= cal(U)_([a_min, a_max]) =
cases(
  1 / (a_max - a_min + 1) & "if" a in [a_min, a_max],
  0 & "otherwise"
) =
cases(
  1/16 & "if" a in [75, 90],
  0 & "otherwise"
)
$

=== $p(b)$
$
p(b) &= cal(U)_([b_min, b_max]) =
cases(
  1 / (b_max - b_min + 1) & "if" b in [b_min, b_max],
  0 & "otherwise"
) =
cases(
  1/101 & "if" b in [500, 600],
  0 & "otherwise"
)
$

=== $p(c|a,b)$
We need to calculate
$
p(c|a,b) = "Bin"(a,p_1) + "Bin"(b,p_2)
$

We'll sum the probabilities of all ways two variables can add up to a specific value:

$
p(a+b=c) &= sum_(i=0)^c p(a=i) dot p(b=c-i) = \ 
&=sum_(i=0)^c binom(a, i) p_1^i (1-p_1)^(a-i) binom(b, c-i) p_2^(c-i) (1-p_2)^(b-c+i) = \
&= sum_(i=0)^c binom(a, i) 0.1^i 0.9^(a-i) binom(b, c-i) (0.01)^(c-i) (0.99)^(b-c+i)
$

=== $p(c|a)$
$
p(c|a) &= sum_(b=b_min)^(b_max) p(c|a, b) p(b) = 1/101 sum_(b=500)^600 (sum_(i=0)^c binom(a, i) 0.1^i 0.9^(a-i) binom(b, c-i) (0.01)^(c-i) (0.99)^(b-c+i))
$

=== $p(c|b)$
$
p(c|b) &= sum_(a=a_min)^(a_max) p(c|a, b) p(a) = 1/16 sum_(a=75)^90 (sum_(i=0)^c binom(a, i) 0.1^i 0.9^(a-i) binom(b, c-i) (0.01)^(c-i) (0.99)^(b-c+i))
$

=== $p(c|d)$
$
p(c|d) = \
&= frac(p(d|c) p(c), p(d)) \
&= (
  binom(c, d-c) 0.3^(d-c) 0.7^(2c-d) 1/16 sum_(a=75)^90 sum_(b=500)^600 (sum_(i=0)^c binom(a, i) 0.1^i 0.9^(a-i) binom(b, c-i) (0.01)^(c-i) (0.99)^(b-c+i))
  ) / (
  sum_(c=0)^690 [binom(c, d-c) 0.3^(d-c) 0.7^(2c-d) 1/16 sum_(a=75)^90 sum_(b=500)^600 (sum_(i=0)^c binom(a, i) 0.1^i 0.9^(a-i) binom(b, c-i) (0.01)^(c-i) (0.99)^(b-c+i))]
  )
$

=== $p(c|a,b,d)$
$
p(c|a, b, d) = \
&= frac(p(d|c) p(c|a, b), p(d|a, b)) = \
&= frac(p(d|c) p(c|a, b), sum_(c'=0)^690 p(d|c') p(c'|a, b)) = \
&= (
  binom(c, d-c) 0.3^(d-c) 0.7^(2c-d) sum_(i=0)^c binom(a, i) 0.1^i 0.9^(a-i) binom(b, c-i) (0.01)^(c-i) (0.99)^(b-c+i)
  ) / (
    sum_(c'=0)^690 binom(c', d-c') 0.3^(d-c') 0.7^(2c'-d) p(c'|a, b)
    )
$

== Model 2

$
  p(a, b, c, d) &= p(d|c) p(c|a, b) p(a) p(b), \
  d|c &~ c + "Bin"(c, p_3), \
  c|a, b &~ "Poiss"(a p_1 + b p_2), \
  a &~ cal(U)_([a_min, a_max]), \
  b &~ cal(U)_([b_min, b_max]).
)
$

=== $p(a)$
$
p(a) &= cal(U)_([a_min, a_max]) =
cases(
  1 / (a_max - a_min + 1) & "if" a in [a_min, a_max],
  0 & "otherwise"
) =
cases(
  1/16 & "if" a in [75, 90],
  0 & "otherwise"
)
$

=== $p(b)$
$
p(b) &= cal(U)_([b_min, b_max]) =
cases(
  1 / (b_max - b_min + 1) & "if" b in [b_min, b_max],
  0 & "otherwise"
) =
cases(
  1/101 & "if" b in [500, 600],
  0 & "otherwise"
)
$

=== $p(c|a,b)$
We need to calculate
$
p(c|a,b) = "Poiss"(a,p_1+b,p_2)
$

$
p(c|a, b) = ((a p_1 + b p_2)^c e^(-(a p_1 + b p_2))) / (c!) = ((0.1a + 0.01b)^c e^(-(0.1a + 0.01b))) / (c!)
$

=== $p(d|c)$
$
p(d|c) = binom(c, d-c) p_3^(d-c) (1 - p_3)^(2c-d) = binom(c, d-c) 0.3^(d-c) (0.7)^(2c-d)
$

=== $p(d)$
$
p(d) = \
&= sum_(c=0)^690 p(d|c) p(c) = \
&= sum_(c=0)^690 lr[ binom(c, d-c) 0.3^(d-c)(0.7)^(2c-d) 1/1616 sum_(a=75)^90 sum_(b=500)^600((0.1a + 0.01b)^c e^(-(0.1a+0.01b)))/(c!) ]
$

=== $p(c|a)$
$
p(c|a) &= sum_b p(c|a, b) p(b) = 1/16 sum_(b=500)^600 ((0.1a + 0.01b)^c e^(-(0.1a+0.01b))) / (c!)
$

=== $p(c|b)$
$
p(c|b) &= sum_a p(c|a, b) p(a) = 1/101 sum_(a=75)^90 ((0.1a + 0.01b)^c e^(-(0.1a+0.01b))) / (c!)
$

= 
Analytical calculations were confirmed by computer results.

*Priors for $a$ and $b$ (both models):*
- $E[a] = (75+90)/2 = 82.5$
- $"Var"(a) = ((90-75+1)^2 - 1) / 12 = 21.25$
- $E[b] = (500+600)/2 = 550$
- $"Var"(b) = ((600-500+1)^2 - 1) / 12 = 850$

== Model 1 Results
- $E[c] = E[a] p_1 + E[b] p_2 = 82.5(0.1) + 550(0.01) = 13.75$
- $"Var"(c) approx 13.17$
- $E[d] = E[c] (1+p_3) = 13.75(1.3) = 17.875$
- $"Var"(d) approx 25.14$

== Model 2 Results
- $E[c] = E[a] p_1 + E[b] p_2 = 13.75$
- $"Var"(c) approx 14.05$
- $E[d] = E[c] (1+p_3) = 17.875$
- $"Var"(d) approx 26.63$

Both models yield similar expected values, but Model 2 (Poisson) has a slightly higher variance for $p(c)$ and $p(d)$.

= 
The variance of $c$ drops from an initial value of around 13.17 (Model 1) or 14.05 (Model 2) to about 1.53-1.54 in both models when conditioned on $d$ (and $a, b$). This highlights how observing $d$ refines the forecast for $c$.

= 
To determine which variable ($a$, $b$, or $d$) best refines the forecast for $c$, the Variance of $c$ was analyzed when conditioned on each.

- Avg $"Var"[c|a]$ (over all $a$) = 12.95
- Avg $"Var"[c|b]$ (over all $b$) = 13.08
- Avg $"Var"[c|d]$ (over all $d$) = 2.46

It is clear that conditioning on $d$ makes the greatest contribution to refining the forecast for $c$. This is because $d$ is directly related to $c$, whereas $a$ and $b$ are only indirectly related.

The document also analyzed the linear separability of the sets ${ (a,b) | "Var"[c|b] < "Var"[c|a] }$ and ${ (a,b) | "Var"[c|b] >= "Var"[c|a] }$. The boundary $"Var"[c|b] = "Var"[c|a]$ simplifies to $b p_2 (1-p_2) = a p_1 (1-p_1)$, which is a linear equation. Therefore, the sets are linearly separable.

=
Theoretically, Model 2 (Poisson) should be faster than Model 1 (Binomial sum). However, the actual results were mixed, suggesting implementation details or data size may be factors.

#table(
  columns: (auto, auto, auto),
  table.header(
    [*Function*], [*Model 1 (sec)*], [*Model 2 (sec)*],
  ),
  [$p(c)$], [0.0192], [0.0539],
  [$p(c|a)$], [0.0075], [0.0051],
  [$p(c|b)$], [0.0007], [0.0006],
  [$p(c|d)$], [0.0441], [0.0721],
  [$p(c|a,b)$], [0.0001], [0.0001],
  [$p(c|a,b,d)$], [0.0241], [0.0197],
  [$p(d)$], [0.0457], [0.0788],
)

Model 1 was surprisingly faster for calculating the marginals $p(c)$ and $p(d)$. Model 2 was faster for most conditional distributions, as expected.

=
The main difference between the models is the treatment of $c$ (attendance):

- *Model 1:* Uses a sum of two Binomial distributions ($"Bin"(a, p_1) + "Bin"(b, p_2)$). This is precise but requires a complex convolution (sum) to calculate $p(c|a,b)$.
- *Model 2:* Uses a single Poisson distribution ($"Poiss"(a p_1 + b p_2)$) as an approximation. This is computationally simpler, as $p(c|a,b)$ has a direct, simple formula.

Both models have the same expected value for $c$: $E[c] = a p_1 + b p_2$. However, Model 1 has a slightly lower variance, as it precisely captures the binomial process. Model 2's simplification results in a slightly higher "Var"iance.

The difference is most pronounced when $a$ and $b$ are large and $p_1, p_2$ are small; here, Model 2's Poisson approximation is most efficient.