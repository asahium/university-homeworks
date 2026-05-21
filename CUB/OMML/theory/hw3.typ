#set document(
  title: "Homework 3",
  author: "Danila Biktimirov",
  date: auto,
)
#set text(font: "Linux Libertine", lang: "en")
#set heading(numbering: "1.")

#align(center)[
  #text(size: 20pt, weight: "bold")[Optimization Methods in Machine Learning, CUB, Spring 2026]
  #v(0.01em)
  #text(size: 16pt)[Theory 3. Constrained optimization and dual problems.]
  #v(0.01em)
  #text(size: 12pt)[Danila Biktimirov]
  #v(0.01em)
  April 21, 2026
]

= Task 1

Solve $min_(x ∈ RR^n) {c^T x : x^T A x <= 1}$, $c != 0$, $A ∈ S_(++)^n$.

Substitute $y = A^(1\/2) x$:
$
min_(||y|| <= 1) (A^(-1\/2) c)^T y.
$
By Cauchy--Schwarz,
$
(A^(-1\/2) c)^T y >= -||A^(-1\/2) c|| ||y|| >= -sqrt(c^T A^(-1) c),
$
with equality at $y^* = -A^(-1\/2) c \/ ||A^(-1\/2) c||$. Hence
$
x^* = -frac(A^(-1) c, sqrt(c^T A^(-1) c)), quad p^* = -sqrt(c^T A^(-1) c).
$
The Cauchy--Schwarz equality case is unique since $A^(-1\/2) c != 0$.

= Task 2

Solve $min_(X ∈ S_(++)^n) {op("tr")(X^(-1)) : ⟨A, X⟩ <= b}$, $A ∈ S_(++)^n$, $b > 0$.

If $⟨A, X⟩ < b$, then $t X$ is feasible for some $t > 1$ and $op("tr")((t X)^(-1)) = t^(-1) op("tr")(X^(-1)) < op("tr")(X^(-1))$, so the constraint is active.

Lagrangian:
$
L(X, λ) = op("tr")(X^(-1)) + λ (⟨A, X⟩ - b), quad λ >= 0.
$
Using $d op("tr")(X^(-1))[H] = -op("tr")(X^(-2) H)$, stationarity gives
$
-X^(-2) + λ A = 0 ==> X^(-2) = λ A.
$
The positive definite square root is unique, so
$
X^(-1) = sqrt(λ) A^(1\/2), quad X = λ^(-1\/2) A^(-1\/2).
$
Active constraint: $b = op("tr")(A X) = λ^(-1\/2) op("tr")(A^(1\/2))$, hence $sqrt(λ) = op("tr")(A^(1\/2)) \/ b$ and
$
X^* = frac(b, op("tr")(A^(1\/2))) A^(-1\/2), quad p^* = frac((op("tr")(A^(1\/2)))^2, b).
$

= Task 3

Let $λ_1, ..., λ_n > 0$ be the eigenvalues of $X ∈ S_(++)^n$. Since $X = X^T$,
$
sum_(i=1)^n ||X e_i||^2 = sum_(i=1)^n e_i^T X^2 e_i = op("tr")(X^2) = sum_(i=1)^n λ_i^2.
$
The constraints $||X e_i|| <= 1$ give $op("tr")(X^2) <= n$. By AM--GM,
$
det X = product λ_i = (product λ_i^2)^(1\/2) <= ( frac(1, n) sum λ_i^2)^(n\/2) <= 1.
$
$I_n$ is feasible with $det I_n = 1$, so it is optimal. Equality forces all $λ_i^2 = 1$, and $X ≻ 0$ gives $λ_i = 1$, hence $X^* = I_n$ uniquely.

*Hadamard.* For arbitrary $X ∈ S_(++)^n$, set $d_i = ||X e_i|| > 0$, $D = op("diag")(d_1, ..., d_n)$, $B = X D^(-1)$. Then $||B e_i|| = 1$. Let $H = (B^T B)^(1\/2) ∈ S_(++)^n$. For every $i$,
$
||H e_i||^2 = e_i^T B^T B e_i = ||B e_i||^2 = 1,
$
so $H$ is feasible above and $det H <= 1$. But $det H = sqrt(det(B^T B)) = |det B|$, so $|det B| <= 1$, and
$
det X = det B product d_i <= product ||X e_i||.
$

= Task 4

Solve $min_(X ∈ S_(++)^n) {⟨C^(-1), X⟩ - log det X : a^T X a <= 1}$, $C ∈ S_(++)^n$, $a != 0$.

The objective is strictly convex on $S_(++)^n$, the constraint is affine, and Slater holds (e.g. $X = ε I_n$ small). Hence KKT is necessary and sufficient, the solution is unique.

Lagrangian:
$
L(X, λ) = ⟨C^(-1), X⟩ - log det X + λ (a^T X a - 1), quad λ >= 0.
$
Stationarity:
$
C^(-1) - X^(-1) + λ a a^T = 0 ==> X = (C^(-1) + λ a a^T)^(-1).
$
Let $γ = a^T C a > 0$. By the Woodbury identity,
$
X = C - frac(λ, 1 + λ γ) C a a^T C, quad a^T X a = γ - frac(λ γ^2, 1 + λ γ) = frac(γ, 1 + λ γ).
$
Complementary slackness: $λ (γ \/ (1 + λ γ) - 1) = 0$.

- If $γ <= 1$: $λ^* = 0$, so $X^* = C$.
- If $γ > 1$: constraint active, $γ \/ (1 + λ γ) = 1$ gives $λ^* = (γ - 1)\/γ$.

Combined,
$
X^* = C - frac((γ - 1)_+, γ^2) C a a^T C, quad γ = a^T C a, quad (t)_+ = max{t, 0}.
$

= Task 5

Primal: $min_(x, s) {1/2 ||s - b||^2 + ρ/2 ||x||^2 : s = A x}$, $ρ > 0$. Introduce $ν ∈ RR^m$:
$
L(x, s, ν) = 1/2 ||s - b||^2 + ρ/2 ||x||^2 + ν^T (s - A x).
$
Minimization over $s$ and $x$:
$
s - b + ν = 0 ==> s = b - ν, quad ρ x - A^T ν = 0 ==> x = frac(1, ρ) A^T ν.
$
Substituting:
$
g(ν) = b^T ν - 1/2 ||ν||^2 - frac(1, 2 ρ) ||A^T ν||^2.
$
Dual problem (unconstrained concave quadratic):
$
max_(ν ∈ RR^m) b^T ν - 1/2 ||ν||^2 - frac(1, 2 ρ) ||A^T ν||^2,
$
or equivalently $min_ν 1/2 ν^T (I_m + (1\/ρ) A A^T) ν - b^T ν$, with maximizer
$
ν^* = (I_m + frac(1, ρ) A A^T)^(-1) b.
$

= Task 6

Let $Δ_(i k) = bb(1){k != y_i}$. The two primal constraints combine into
$
w_k^T x_i + b_k - w_(y_i)^T x_i - b_(y_i) + Δ_(i k) - ξ_i <= 0, quad ∀ i, k,
$
since the $k = y_i$ case is exactly $ξ_i >= 0$. With multipliers $β_(i k) >= 0$,
$
L = 1/2 sum_k ||w_k||^2 + C sum_i ξ_i + sum_(i, k) β_(i k) [w_k^T x_i + b_k - w_(y_i)^T x_i - b_(y_i) + Δ_(i k) - ξ_i].
$
$∂L \/ ∂ξ_i$: $C - sum_k β_(i k) = 0$.

Define
$
α_(i k) = cases(
  -β_(i k) &k != y_i,
  C - β_(i y_i) &k = y_i,
)
$
Then $sum_k α_(i k) = 0$, $α_(i k) <= 0$ for $k != y_i$, and $α_(i y_i) = sum_(k != y_i) β_(i k) <= sum_k β_(i k) = C$.

$∂L \/ ∂w_ℓ$:
$
w_ℓ + sum_i (β_(i ℓ) - bb(1){y_i = ℓ} sum_k β_(i k)) x_i = 0 ==> w_ℓ = sum_i α_(i ℓ) x_i.
$

Linear part of the dual:
$
sum_(i, k) β_(i k) Δ_(i k) = sum_i sum_(k != y_i) β_(i k) = sum_i α_(i y_i).
$
Quadratic part:
$
- 1/2 sum_ℓ ||w_ℓ||^2 = - 1/2 sum_(i, j) x_i^T x_j sum_(k=1)^K α_(i k) α_(j k).
$
Hence the dual
$
max_α sum_(i=1)^N α_(i y_i) - 1/2 sum_(i, j=1)^N x_i^T x_j sum_(k=1)^K α_(i k) α_(j k)
$
subject to
$
sum_(k=1)^K α_(i k) = 0, quad α_(i k) <= 0 quad (k != y_i), quad α_(i y_i) <= C, quad ∀ i.
$
Since $sum_k α_(i k) = 0$, the linear term satisfies $sum_i α_(i y_i) = -sum_i sum_(k != y_i) α_(i k)$, which matches the form $sum_(i, k) α_(i k)$ (modulo sign conventions) of the stated objective.
