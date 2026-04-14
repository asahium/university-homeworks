#set document(
  title: "Homework 2",
  author: "Danila Biktimirov",
  date: auto,
)
#set text(font: "Linux Libertine", lang: "en")
#set heading(numbering: "1.")
// #set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 20pt, weight: "bold")[Optimization Methods in Machine Learning, CUB, Spring 2026]
  #v(0.01em)
  #text(size: 16pt)[Theory 2. Convex sets and functions.]
  #v(0.01em)
  #text(size: 12pt)[Danila Biktimirov]
  #v(0.01em)
  March 17, 2026
]

= Task 1

Let $z = λ x + (1 - λ) y$, $λ ∈ [0,1]$.

For $op("cl")(C)$: take $x_k, y_k ∈ C$ such that
$
x_k → x, quad y_k → y.
$
Since $C$ is convex,
$
λ x_k + (1 - λ) y_k ∈ C.
$
Passing to the limit,
$
λ x_k + (1 - λ) y_k → z,
$
hence $z ∈ op("cl")(C)$.

For $op("int")(C)$: if $λ = 0$ or $1$, trivial. Let $0 < λ < 1$.
Take open sets $U, V$ such that
$
x ∈ U ⊆ C, quad y ∈ V ⊆ C.
$
Then $λ U + (1 - λ) V$ is open, contains $z$, and by convexity of $C$,
$
λ U + (1 - λ) V ⊆ C.
$
So $z ∈ op("int")(C)$.

Therefore $op("cl")(C)$ and $op("int")(C)$ are convex.

= Task 2

== (a)

Since $C ⊆ op("Conv")(C)$ and $D ⊆ op("Conv")(D)$,
$
op("Conv")(C ∪ D) ⊆ op("Conv")(op("Conv")(C) ∪ op("Conv")(D)).
$
Also $op("Conv")(C ∪ D)$ is convex and contains both $C$ and $D$, hence it contains $op("Conv")(C)$ and $op("Conv")(D)$.
So
$
op("Conv")(op("Conv")(C) ∪ op("Conv")(D)) ⊆ op("Conv")(C ∪ D).
$
Therefore
$
op("Conv")(C ∪ D) = op("Conv")(op("Conv")(C) ∪ op("Conv")(D)).
$

== (b)

Since $C ∩ D ⊆ C$ and $C ∩ D ⊆ D$,
$
op("Conv")(C ∩ D) ⊆ op("Conv")(C), quad op("Conv")(C ∩ D) ⊆ op("Conv")(D).
$
Hence
$
op("Conv")(C ∩ D) ⊆ op("Conv")(C) ∩ op("Conv")(D).
$

= Task 3

Let
$
S = {x ∈ RR^n : x^T P x <= (c^T x)^2, c^T x >= 0}.
$
Since $P ≻ 0$,
$
x^T P x = ||P^(1/2)x||_2^2.
$
Because $c^T x >= 0$,
$
x ∈ S <==> ||P^(1/2) x||_2 <= c^T x.
$
Take $x,y ∈ S$, $λ ∈ [0,1]$. Then
$
||P^(1/2)(λ x + (1-λ) y)||_2
<= λ ||P^(1/2) x||_2 + (1-λ) ||P^(1/2) y||_2
<= λ c^T x + (1-λ) c^T y
= c^T (λ x + (1-λ) y).
$
Hence $λ x + (1-λ) y ∈ S$, so $S$ is convex.

= Task 4

== (a)

Write
$
S = S_1 ∩ S_2 ∩ S_3,
$
where
$
S_1 = {X ∈ S^n : A^T X + X A + I ⪯ 0},
$
$
S_2 = {X ∈ S^n : tr(X) <= 1},
$
$
S_3 = {X ∈ S^n : X ⪰ 0}.
$
$S_1$ is convex because $A^T X + X A + I$ is affine in $X$.
$S_2$ is a halfspace.
$S_3$ is the PSD cone.
Therefore $S$ is convex.

== (b)

Since $X ⪰ I$, $X$ is positive definite. By Schur complement,
$
u^T X^(-1) u <= 1 <==> mat(X, u; u^T, 1) ⪰ 0.
$
So the set equals
$
{(u, X) : mat(X, u; u^T, 1) ⪰ 0, I ⪯ X ⪯ 2I}.
$
This is an intersection of LMIs, hence convex.

= Task 5

Let
$
K = {x x^T : ||x||_2 = 1}.
$

If
$
A = ∑_(i=1)^m θ_i x_i x_i^T, quad θ_i >= 0, quad ∑_(i=1)^m θ_i = 1,
$
then
$
A ⪰ 0,
$
and
$
tr(A) = ∑_(i=1)^m θ_i tr(x_i x_i^T)
= ∑_(i=1)^m θ_i ||x_i||_2^2
= ∑_(i=1)^m θ_i
= 1.
$
Hence
$
op("Conv")(K) ⊆ {A ∈ S_+^n : tr(A) = 1}.
$

Conversely, let $A ∈ S_+^n$ and $tr(A)=1$. Spectral decomposition gives
$
A = ∑_(i=1)^n λ_i q_i q_i^T,
$
where
$
λ_i >= 0, quad ||q_i||_2 = 1, quad ∑_(i=1)^n λ_i = tr(A) = 1.
$
So $A$ is a convex combination of matrices $q_i q_i^T ∈ K$.
Therefore
$
op("Conv")(K) = {A ∈ S_+^n : tr(A) = 1}.
$

= Task 6

`=>`
If $f$ is convex, then for $t ∈ (0,1]$,
$
f(x + t (y-x)) <= (1-t) f(x) + t f(y).
$
Hence
$
(f(x + t (y-x)) - f(x)) / t <= f(y) - f(x).
$
Let $t → 0+$:
$
∇f(x)^T (y-x) <= f(y) - f(x).
$
So
$
f(y) >= f(x) + ∇f(x)^T (y-x).
$

`<=`
Assume
$
f(y) >= f(x) + ∇f(x)^T (y-x), quad ∀ x,y.
$
Take
$
z = (1-λ) x + λ y.
$
Then
$
f(x) >= f(z) + ∇f(z)^T (x-z),
$
$
f(y) >= f(z) + ∇f(z)^T (y-z).
$
Multiply by $1-λ$ and $λ$ and add:
$
(1-λ) f(x) + λ f(y)
>= f(z) + ∇f(z)^T ((1-λ)(x-z) + λ (y-z))
= f(z).
$
Hence
$
f((1-λ) x + λ y) <= (1-λ) f(x) + λ f(y),
$
so $f$ is convex.

= Task 7

== (a)

Let
$
g_i(t) = max(0,t)^2.
$
The map $t ↦ max(0,t)$ is convex and nondecreasing, and $s ↦ s^2$ is convex and nondecreasing on $RR_+$.
Hence each $g_i$ is convex.

Now define
$
L(z) = log(∑_(i=1)^n exp(z_i)).
$
$L$ is convex and nondecreasing in each coordinate. Therefore
$
f(x) = L(g_1(x_1), ..., g_n(x_n))
$
is convex.

== (b)

Let
$
M = {P ∈ S^n : I ⪯ P ⪯ 5I}.
$
Then
$
op("epi") f = {(x,t) : ∃ P ∈ M, x^T P^(-1) x + tr(P) <= t}.
$
Since $P ⪰ I$, $P$ is positive definite, and by Schur complement
$
x^T P^(-1) x + op("tr")(P) <= t
<==>
mat(P, x; x^T, t - op("tr")(P)) ⪰ 0.
$
Hence
$
op("epi") f = op("proj")_(x,t) {(x,t,P) : P ∈ M, mat(P, x; x^T, t - op("tr")(P)) ⪰ 0 }.
$
The set inside is convex (LMIs + affine terms), and projection preserves convexity.
So $op("epi") f$ is convex, hence $f$ is convex.

= Task 8

For
$
f(x) = ∏_(i=1)^n x_i^(α_i), quad α_i >= 0, quad ∑_(i=1)^n α_i = 1,
$
set
$
a_i = α_i / x_i.
$
Then
$
∇f(x) = f(x)(a_1, ..., a_n)^T,
$
$
∇^2 f(x) = f(x)(a a^T - op("diag")(α_1/x_1^2, ..., α_n/x_n^2)).
$
So for any $h ∈ RR^n$,
$
h^T ∇^2 f(x) h
= f(x)[(∑_(i=1)^n α_i h_i/x_i)^2 - ∑_(i=1)^n α_i (h_i/x_i)^2].
$
Let $z_i = h_i / x_i$. Then
$
(∑_(i=1)^n α_i z_i)^2
<= (∑_(i=1)^n α_i)(∑_(i=1)^n α_i z_i^2)
= ∑_(i=1)^n α_i z_i^2.
$
Hence
$
h^T ∇^2 f(x) h <= 0.
$
So $∇^2 f(x) ⪯ 0$, therefore $f$ is concave.

= Task 9

Define
$
g_n(x) = x_n,
$
$
g_k(x) = x_k - 1/g_(k+1)(x), quad k = n-1, ..., 1.
$
Then
$
f(x) = 1/g_1(x).
$

Also define
$
D_n = {x : x_n > 0},
$
$
D_k = {x ∈ D_(k+1) : g_k(x) > 0}.
$
So the domain is $D_1$.

Now induct on $k$:
$g_n$ is affine, hence concave.
If $g_(k+1)$ is concave and positive on $D_(k+1)$, then $1/g_(k+1)$ is convex on $D_(k+1)$ because $t ↦ 1/t$ is convex and decreasing on $RR_(++)$.
Therefore
$
g_k = x_k - 1/g_(k+1)
$
is concave on $D_(k+1)$, and
$
D_k = {x ∈ D_(k+1) : g_k(x) > 0}
$
is convex.

So $g_1$ is positive and concave on the convex set $D_1$.
Again $t ↦ 1/t$ is convex and decreasing on $RR_(++)$, hence
$
f = 1/g_1
$
is convex on $D_1$.

= Task 10

`=>`
If $f$ is convex, then with $λ = 1/2$,
$
f((x+y)/2) <= (f(x) + f(y))/2.
$

`<=`
Assume
$
f((u+v)/2) <= (f(u) + f(v))/2, quad ∀ u,v ∈ RR^n.
$
For every dyadic $λ = m/2^k$, repeated use of the midpoint inequality gives
$
f((1-λ) x + λ y) <= (1-λ) f(x) + λ f(y).
$
Now take arbitrary $λ ∈ [0,1]$ and choose dyadics $λ_j → λ$.
By continuity,
$
f((1-λ) x + λ y)
= lim_(j→∞) f((1-λ_j) x + λ_j y)
<= lim_(j→∞) ((1-λ_j) f(x) + λ_j f(y))
= (1-λ) f(x) + λ f(y).
$
Hence $f$ is convex.