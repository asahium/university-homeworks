#set document(
  title: "Homework 4",
  author: "Danila Biktimirov",
  date: auto,
)
#set text(font: "Linux Libertine", lang: "en")
#set heading(numbering: "1.")

#align(center)[
  #text(size: 20pt, weight: "bold")[Optimization Methods in Machine Learning, CUB, Spring 2026]
  #v(0.01em)
  #text(size: 16pt)[Theory 4. Conjugate functions and norms, proximal operators.]
  #v(0.01em)
  #text(size: 12pt)[Danila Biktimirov]
  #v(0.01em)
  May 21, 2026
]

= Task 1

In all four cases $f^*(y) = sup_x (x y - f(x))$ on the stated domain.

== (a) $f(x) = x log x - x$ on $[0, +∞)$, $f(0) = 0$

For $x > 0$, $partial_x (x y - x log x + x) = y - log x = 0 ==> x = e^y$. Then
$
f^*(y) = e^y y - e^y y + e^y = e^y.
$
The boundary value $x = 0$ gives $0 < e^y$, so
$
f^*(y) = e^y, quad y ∈ RR.
$

== (b) $f(x) = 1\/x$ on $(0, +∞)$

$f^*(y) = sup_(x > 0) (x y - 1\/x)$.
- $y > 0$: $x y - 1\/x -> +∞$ as $x -> ∞$.
- $y <= 0$: $partial_x = y + 1\/x^2 = 0 ==> x = 1\/sqrt(-y)$ (for $y < 0$).

For $y < 0$:
$
f^*(y) = frac(y, sqrt(-y)) - sqrt(-y) = -sqrt(-y) - sqrt(-y) = -2 sqrt(-y).
$
For $y = 0$: $sup_(x > 0) (-1\/x) = 0 = -2 sqrt(0)$. Hence
$
f^*(y) = cases(
  -2 sqrt(-y) &y <= 0,
  +∞ &y > 0.
)
$

== (c) $f(x) = -2 sqrt(-x)$ on $(-∞, 0]$

Let $t = -x >= 0$:
$
f^*(y) = sup_(t >= 0) (-t y + 2 sqrt(t)).
$
- $y <= 0$: as $t -> ∞$, $-t y + 2 sqrt(t) -> +∞$.
- $y > 0$: $partial_t = -y + 1\/sqrt(t) = 0 ==> t = 1\/y^2$, giving $-1\/y + 2\/y = 1\/y$.

Hence
$
f^*(y) = cases(
  1\/y &y > 0,
  +∞ &y <= 0.
)
$

== (d) $f(x) = max(0, x)$ on $RR$

$f^*(y) = sup_x (x y - max(0, x))$.
- $x >= 0$: $x(y - 1)$. Bounded above iff $y <= 1$, then $sup = 0$.
- $x <= 0$: $x y$. Bounded above iff $y >= 0$, then $sup = 0$.

So
$
f^*(y) = cases(
  0 &0 <= y <= 1,
  +∞ &"otherwise".
)
$

= Task 2

== (a) $f(x) = log sum_(i=1)^n exp(x_i)$

$f^*(y) = sup_x (x^T y - log sum_i exp(x_i))$. Stationarity:
$
y_i = frac(exp(x_i), sum_j exp(x_j)) ==> y_i >= 0, quad sum_i y_i = 1.
$
Then $x_i = log y_i + log Z$ with $Z = sum_j exp(x_j)$, and
$
x^T y - log Z = sum_i y_i log y_i + log Z dot sum_i y_i - log Z = sum_i y_i log y_i.
$
If $y$ has $y_i < 0$ or $sum_i y_i != 1$, shifting $x -> x + c bb(1)$ shows the sup is $+∞$. Let $Δ_n = {y ∈ RR^n : y >= 0, sum_i y_i = 1}$. Therefore
$
f^*(y) = cases(
  sum_(i=1)^n y_i log y_i &y ∈ Δ_n,
  +∞ &"otherwise",
)
$
with the convention $0 log 0 = 0$.

== (b) $f(x) = max(x_1, ..., x_n)$

Write $x_i = z + t_i$ with $t_i <= 0$ and $max_i t_i = 0$. Then $max x_i = z$ and
$
x^T y - max x_i = z (sum_i y_i - 1) + sum_i t_i y_i.
$
Need $sum_i y_i = 1$ (else $z -> ±∞$). With $t_i <= 0$, $sup sum_i t_i y_i < ∞$ requires $y_i >= 0$, and then $sup = 0$ at $t = 0$. Hence
$
f^*(y) = cases(
  0 &y ∈ Δ_n,
  +∞ &"otherwise".
)
$

== (c) $f(X) = -log det X$ on $S_(++)^n$

$f^*(Y) = sup_(X ≻ 0) (⟨Y, X⟩ + log det X)$. Stationarity:
$
Y + X^(-1) = 0 ==> X = -Y^(-1), quad "requires" Y ≺ 0.
$
Then
$
f^*(Y) = ⟨Y, -Y^(-1)⟩ + log det(-Y^(-1)) = -n - log det(-Y).
$
For $Y$ not in $-S_(++)^n$, the sup is $+∞$. So
$
f^*(Y) = cases(
  -n - log det(-Y) &Y ≺ 0,
  +∞ &"otherwise".
)
$

= Task 3

== (a) $f(x) = ||x||_∞$

Dual norm of $||·||_∞$ is $||·||_1$. For any norm,
$
∂||x|| = {y : ||y||_* <= 1, ⟨y, x⟩ = ||x||}.
$
Let $I = arg max_i |x_i|$. If $x != 0$,
$
∂f(x) = op("conv"){op("sign")(x_i) e_i : i ∈ I} = {y : op("supp")(y) ⊆ I, y_i op("sign")(x_i) >= 0, sum_(i ∈ I) y_i op("sign")(x_i) = 1}.
$
If $x = 0$,
$
∂f(0) = {y : ||y||_1 <= 1}.
$

== (b) $f(x) = sum_(1 <= i < j <= n) |x_i - x_j|$

By the sum rule, $∂f(x) = sum_(i < j) ∂|x_i - x_j|$, where
$
∂|x_i - x_j| (x) = cases(
  {e_i - e_j} &x_i > x_j,
  {e_j - e_i} &x_i < x_j,
  {s (e_i - e_j) : s ∈ [-1, 1]} &x_i = x_j.
)
$
Equivalently, with $op("Sgn")(t) = {op("sign")(t)}$ for $t != 0$ and $[-1, 1]$ for $t = 0$:
$
∂f(x) = { sum_(i < j) s_(i j) (e_i - e_j) : s_(i j) ∈ op("Sgn")(x_i - x_j) }.
$

= Task 4

Let $A = U Σ V^T$ be the SVD with $Σ = op("diag")(σ_1, ..., σ_n)$, $σ_i >= 0$.

== (a) Reduction to diagonal matrices

Set $Y = U^T X V$. Since $U, V$ are orthogonal, $||Y||_2 = ||X||_2$. Also
$
⟨A, X⟩ = op("tr")(V Σ U^T X) = op("tr")(Σ U^T X V) = op("tr")(Σ Y) = sum_(i=1)^n σ_i Y_(i i).
$
The objective depends only on $op("diag")(Y)$. For any $Y$, $||Y||_2 >= max_i |Y_(i i)|$, with equality at $Y = op("diag")(Y_(1 1), ..., Y_(n n))$. Hence the optimum is attained at diagonal $Y$:
$
||A||_(2*) = max_(d ∈ RR^n) {sum_(i=1)^n σ_i d_i : ||op("diag")(d)||_2 = ||d||_∞ <= 1}.
$

== (b)

Since $σ_i >= 0$, the maximum is at $d_i = 1$ for all $i$:
$
||A||_(2*) = sum_(i=1)^n σ_i (A),
$
attained at $Y = I_n$, i.e. $X^* = U V^T$.

= Task 5

Let $f$ be closed convex.

*(a) $==>$ (b).* By definition $u = arg min_v (f(v) + 1/2 ||v - x||^2)$. The optimality condition for a sum of a closed convex function and a smooth strictly convex one is
$
0 ∈ ∂f(u) + (u - x) ==> x - u ∈ ∂f(u).
$

*(b) $<=>$ (c).* Definition of subgradient:
$
g ∈ ∂f(u) <==> f(v) >= f(u) + ⟨g, v - u⟩ quad ∀ v.
$
Setting $g = x - u$ gives (c).

*(c) $==>$ (a).* From (c), for any $v$,
$
f(v) + 1/2 ||v - x||^2 >= f(u) + ⟨x - u, v - u⟩ + 1/2 ||v - x||^2.
$
Using $||v - x||^2 = ||v - u||^2 + 2 ⟨v - u, u - x⟩ + ||u - x||^2$,
$
f(v) + 1/2 ||v - x||^2 >= f(u) + 1/2 ||u - x||^2 + 1/2 ||v - u||^2 >= f(u) + 1/2 ||u - x||^2.
$
Hence $u$ minimizes $f(v) + 1/2 ||v - x||^2$, i.e. $u ∈ op("prox")_f (x)$.

Thus (a) $<=>$ (b) $<=>$ (c).

= Task 6

Let $u = op("prox")_f (x)$, $v = op("prox")_f (y)$. By Task 5(c),
$
f(v) >= f(u) + ⟨x - u, v - u⟩,
$
$
f(u) >= f(v) + ⟨y - v, u - v⟩.
$
Adding:
$
0 >= ⟨x - u, v - u⟩ + ⟨y - v, u - v⟩ = ⟨(x - y) - (u - v), v - u⟩.
$
Hence
$
⟨u - v, x - y⟩ >= ||u - v||^2,
$
i.e.
$
||op("prox")_f (x) - op("prox")_f (y)||^2 <= ⟨op("prox")_f (x) - op("prox")_f (y), x - y⟩. quad (*)
$
By Cauchy--Schwarz, $⟨u - v, x - y⟩ <= ||u - v|| ||x - y||$, so from $(*)$:
$
||u - v||^2 <= ||u - v|| ||x - y|| ==> ||u - v|| <= ||x - y||.
$
Thus $op("prox")_f$ is a contraction (in fact, firmly non-expansive).
