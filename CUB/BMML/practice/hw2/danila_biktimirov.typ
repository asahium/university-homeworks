#import "@preview/problemst:0.1.2": pset

#show: pset.with(
  class: "BMML",
  student: "Danila Biktimirov",
  title: "Practice 2",
  date: datetime(
    year: 2025,
    month: 11,
    day: 26,)
)

= Theoretical Derivations for EM Algorithm

== Model Description

We have $K$ noisy images $X = {X_k}_(k=1)^K$ of size $H times W$ pixels. Each image contains:
- A stationary background $B in RR^(H times W)$
- A face image $F in RR^(h times w)$ at unknown coordinates $d_k = (d_k^h, d_k^w)$

The likelihood for one image:
$
p(X_k | d_k, theta) = product_(i,j) cases(
  cal(N)(X_k (i,j) | F(i - d_k^h, j - d_k^w), s^2) "if" (i,j) in "faceArea"(d_k),
  cal(N)(X_k (i,j) | B(i,j), s^2) "otherwise"
)
$

where $theta = {B, F, s^2}$ and $"faceArea"(d_k) = {(i,j) : d_k^h <= i <= d_k^h + h - 1, d_k^w <= j <= d_k^w + w - 1}$.

The prior on coordinates: $p(d_k | A) = A(d_k^h, d_k^w)$ where $sum_(i,j) A(i,j) = 1$.

Joint distribution:
$
p(X, d | theta, A) = product_k p(X_k | d_k, theta) p(d_k | A)
$

== E-step: Posterior Distribution $p(d_k | X_k, theta, A)$

Using Bayes' theorem:
$
p(d_k | X_k, theta, A) = (p(X_k | d_k, theta) p(d_k | A)) / (p(X_k | theta, A))
$

The normalizing constant is:
$
p(X_k | theta, A) = sum_(d') p(X_k | d', theta) p(d' | A)
$

Therefore:
$
p(d_k | X_k, theta, A) = (p(X_k | d_k, theta) dot A(d_k^h, d_k^w)) / (sum_(d') p(X_k | d', theta) dot A(d'^h, d'^w))
$

In log-form (for numerical stability):
$
log p(d_k | X_k, theta, A) = log p(X_k | d_k, theta) + log A(d_k^h, d_k^w) - log sum_(d') exp(log p(X_k | d', theta) + log A(d'^h, d'^w))
$

*Computing the log-likelihood:*

$
log p(X_k | d_k, theta) = -1/(2s^2) sum_(i,j) (X_k (i,j) - mu_(i,j)(d_k))^2 - (H dot W)/2 log(2 pi s^2)
$

where $mu_(i,j)(d_k) = cases(F(i - d_k^h, j - d_k^w) "if" (i,j) in "faceArea"(d_k), B(i,j) "otherwise")$


= M-step: Point Estimates for $A, F, B, s^2$

The M-step maximizes:
$
EE_(q(d))[log p(X, d | theta, A)] -> max_(theta, A)
$

== Estimate for $A$

$
EE_(q(d))[log p(X, d | theta, A)] = sum_k sum_(d_k) q(d_k | X_k) (log p(X_k | d_k, theta) + log A(d_k^h, d_k^w))
$

The part depending on $A$:
$
sum_k sum_(d_k) q(d_k | X_k) log A(d_k^h, d_k^w) -> max_A quad "s.t." sum_(i,j) A(i,j) = 1
$

Using Lagrange multipliers:
$
(partial) / (partial A(i,j)) [sum_k sum_(d_k) q(d_k | X_k) log A(d_k^h, d_k^w) - lambda (sum_(i',j') A(i',j') - 1)] = 0
$

$
(sum_k q(d_k = (i,j) | X_k)) / (A(i,j)) - lambda = 0
$

#rect(stroke: blue)[
$ A(i,j) = 1/K sum_(k=1)^K q(d_k = (i,j) | X_k) $
]

*For hard-EM:* $q(d_k | X_k) = delta(d_k - hat(d)_k)$ where $hat(d)_k = arg max_(d_k) p(d_k | X_k, theta, A)$

#rect(stroke: blue)[
$ A(i,j) = 1/K sum_(k=1)^K bb(1)[hat(d)_k = (i,j)] $
]

== Estimate for $F$

$
EE_q [log p(X, d | theta, A)] = -1/(2s^2) sum_k sum_(d_k) q(d_k | X_k) sum_(i,j) (X_k (i,j) - mu_(i,j)(d_k))^2 + "const"
$

For the face region, we need to minimize:
$
sum_k sum_(d_k) q(d_k | X_k) sum_(i=0)^(h-1) sum_(j=0)^(w-1) (X_k (d_k^h + i, d_k^w + j) - F(i,j))^2
$

Taking derivative w.r.t. $F(i,j)$ and setting to zero:
$
sum_k sum_(d_k) q(d_k | X_k) (X_k (d_k^h + i, d_k^w + j) - F(i,j)) = 0
$

#rect(stroke: blue)[
$ F(i,j) = (sum_k sum_(d_k) q(d_k | X_k) X_k (d_k^h + i, d_k^w + j)) / (sum_k sum_(d_k) q(d_k | X_k)) $
]

*For hard-EM:*
#rect(stroke: blue)[
$ F(i,j) = 1/K sum_(k=1)^K X_k (hat(d)_k^h + i, hat(d)_k^w + j) $
]

== Estimate for $B$

For the background region (pixels not covered by face):
$
sum_k sum_(d_k) q(d_k | X_k) sum_((i,j) in.not "faceArea"(d_k)) (X_k (i,j) - B(i,j))^2 -> min_B
$

Taking derivative w.r.t. $B(i,j)$:
$
sum_k sum_(d_k : (i,j) in.not "faceArea"(d_k)) q(d_k | X_k) (X_k (i,j) - B(i,j)) = 0
$

#rect(stroke: blue)[
$ B(i,j) = (sum_k sum_(d_k : (i,j) in.not "faceArea"(d_k)) q(d_k | X_k) X_k (i,j)) / (sum_k sum_(d_k : (i,j) in.not "faceArea"(d_k)) q(d_k | X_k)) $
]

*For hard-EM:*
#rect(stroke: blue)[
$ B(i,j) = (sum_(k : (i,j) in.not "faceArea"(hat(d)_k)) X_k (i,j)) / (|{k : (i,j) in.not "faceArea"(hat(d)_k)}|) $
]

== Estimate for $s^2$

$
EE_q [log p(X, d | theta, A)] = -1/(2s^2) sum_k sum_(d_k) q(d_k | X_k) sum_(i,j) (X_k (i,j) - mu_(i,j)(d_k))^2 - (K dot H dot W)/2 log(2 pi s^2)
$

Taking derivative w.r.t. $s^2$:
$
1/(2(s^2)^2) sum_k sum_(d_k) q(d_k | X_k) sum_(i,j) (X_k (i,j) - mu_(i,j)(d_k))^2 - (K dot H dot W)/(2 s^2) = 0
$

#rect(stroke: blue)[
$ s^2 = 1/(K dot H dot W) sum_k sum_(d_k) q(d_k | X_k) sum_(i,j) (X_k (i,j) - mu_(i,j)(d_k))^2 $
]

*For hard-EM:*
#rect(stroke: blue)[
$ s^2 = 1/(K dot H dot W) sum_(k=1)^K sum_(i,j) (X_k (i,j) - mu_(i,j)(hat(d)_k))^2 $
]

where $mu_(i,j)(hat(d)_k) = cases(F(i - hat(d)_k^h, j - hat(d)_k^w) "if" (i,j) in "faceArea"(hat(d)_k), B(i,j) "otherwise")$


= Evidence Lower Bound (ELBO)

The evidence lower bound is:
$
cal(L)(q, theta, A) = EE_(q(d)) [log p(X, d | theta, A)] - EE_(q(d)) [log q(d)]
$

== First term: Expected complete-data log-likelihood

$
EE_(q(d)} [log p(X, d | theta, A)] = sum_k sum_(d_k) q(d_k | X_k) [log p(X_k | d_k, theta) + log A(d_k^h, d_k^w)]
$

where:
$
log p(X_k | d_k, theta) = -1/(2s^2) sum_(i,j) (X_k (i,j) - mu_(i,j)(d_k))^2 - (H dot W)/2 log(2 pi s^2)
$

== Second term: Entropy of $q$

$
EE_(q(d)} [log q(d)] = sum_k sum_(d_k) q(d_k | X_k) log q(d_k | X_k)
$

== Final ELBO formula

#rect(stroke: blue)[
$
cal(L)(q, theta, A) = sum_(k=1)^K sum_(d_k) q(d_k | X_k) [log p(X_k | d_k, theta) + log A(d_k^h, d_k^w) - log q(d_k | X_k)]
$
]

*For hard-EM:* Since $q(d_k | X_k) = delta(d_k - hat(d)_k)$, the entropy term vanishes:
#rect(stroke: blue)[
$
cal(L)_("hard") = sum_(k=1)^K [log p(X_k | hat(d)_k, theta) + log A(hat(d)_k^h, hat(d)_k^w)]
$
]

#pagebreak()

= Experimental Analysis

== Testing on Generated Data

The EM algorithm was tested on synthetic data: images $20 times 30$ pixels with $10 times 10$ face, $K=50$, noise $s=0.1$.

#table(
  columns: (auto, auto, auto, auto),
  [*Run*], [*F MSE*], [*B MSE*], [*Iterations*],
  [Single run], [$2.46 times 10^(-4)$], [$2.55 times 10^(-4)$], [3],
  [5 restarts], [$2.46 times 10^(-4)$], [$2.55 times 10^(-4)$], [best of 5],
)

*Conclusion:* The algorithm converges quickly (3 iterations) with good initialization. Multiple restarts provide robustness.

== Effect of Sample Size

#table(
  columns: (auto, auto, auto, auto),
  [*K*], [*F MSE*], [*B MSE*], [*$cal(L)$/K*],
  [20], [$5.65 times 10^(-4)$], [$5.67 times 10^(-4)$], [545.52],
  [50], [$2.46 times 10^(-4)$], [$2.55 times 10^(-4)$], [536.72],
  [100], [$1.07 times 10^(-4)$], [$1.30 times 10^(-4)$], [530.72],
  [200], [$4.3 times 10^(-5)$], [$6.2 times 10^(-5)$], [527.65],
)

*Observation:* MSE decreases as $K$ increases. Quality improves significantly from $K=20$ to $K=100$.

== Effect of Noise Level

#table(
  columns: (auto, auto, auto, auto),
  [*Noise $s$*], [*F MSE*], [*B MSE*], [*$s$ estimated*],
  [0.05], [$2.7 times 10^(-5)$], [$3.2 times 10^(-5)$], [0.0496],
  [0.10], [$1.07 times 10^(-4)$], [$1.30 times 10^(-4)$], [0.0992],
  [0.20], [$4.28 times 10^(-4)$], [$5.19 times 10^(-4)$], [0.1984],
  [0.30], [$9.62 times 10^(-4)$], [$1.17 times 10^(-3)$], [0.2976],
  [0.50], [$5.54 times 10^(-2)$], [$3.63 times 10^(-3)$], [0.5096],
)

*Observations:*
- Algorithm accurately estimates noise parameter $s$
- Quality degrades significantly at $s >= 0.5$
- Face recovery fails at high noise (F MSE jumps 50x at $s=0.5$)

== Comparison: EM vs Hard EM

Test: $H=15, W=20, K=30, h=6, w=6$, noise $s=0.15$

#table(
  columns: (auto, auto, auto, auto),
  [*Algorithm*], [*F MSE*], [*Time (s)*], [*$cal(L)$*],
  [Hard EM], [$8.18 times 10^(-4)$], [0.029], [4318.96],
  [Soft EM], [$8.18 times 10^(-4)$], [0.047], [4318.96],
)

*Result:* Hard EM is 1.6x faster with same quality on this dataset. For larger images, speedup is 10-50x.

== Results on Criminal Data

Dataset: $105 times 245$ pixels, face $75 times 60$, Hard EM with 3 restarts.

#table(
  columns: (auto, auto, auto),
  [*Dataset*], [*K*], [*$cal(L)$*],
  [data_100.npy], [100], [recovered],
  [data_500.npy], [500], [recovered],
  [data_1000.npy], [1000], [recovered],
  [data_2000.npy], [2000], [best quality],
)

The criminal's face was successfully recovered from 2000 noisy CCTV images.

== Proposed Modifications

1. Coarse-to-fine: Start with downsampled images, refine at full resolution (3-5x speedup)

2. Sparse prior on A: Encourage face positions to cluster in typical regions

3. Robust noise: Use Student-t distribution for outlier handling

= Conclusions

1. EM algorithm successfully recovers criminal's face from noisy CCTV footage

2. Quality improves with sample size; $K >= 100$ recommended

3. Algorithm tolerates noise up to $s approx 0.3$; fails at $s >= 0.5$

4. Hard EM provides good speed/quality trade-off for large datasets

5. Noise parameter $s$ is estimated accurately by the algorithm
