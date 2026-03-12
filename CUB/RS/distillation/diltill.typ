#import "@preview/touying:0.6.1": *
#import themes.university: *

#let accent = rgb("#2563eb")
#let accent-light = rgb("#dbeafe")
#let accent2 = rgb("#059669")
#let accent2-light = rgb("#d1fae5")
#let warn = rgb("#d97706")
#let warn-light = rgb("#fef3c7")
#let neutral = rgb("#64748b")

#let info-box(body, title: none, color: accent) = block(
  width: 100%,
  inset: (x: 14pt, y: 10pt),
  radius: 6pt,
  fill: color.lighten(88%),
  stroke: (left: 3pt + color),
)[
  #if title != none {
    text(weight: "bold", fill: color)[#title]
    parbreak()
  }
  #body
]

#let placeholder-box(body) = block(
  width: 100%,
  height: 1fr,
  inset: 16pt,
  radius: 8pt,
  fill: luma(96%),
  stroke: (dash: "dashed", paint: luma(75%), thickness: 1.2pt),
)[
  #align(center + horizon)[
    #text(fill: luma(45%), size: 0.85em)[#body]
  ]
]

#let kv(key, val) = [*#key:* #val]

#show: university-theme.with(
  aspect-ratio: "16-9",
  config-info(
    title: [Model Distillation],
    subtitle: [Research Seminar],
    author: [Danila Biktimirov],
    date: datetime.today(),
    institution: [CUB],
  ),
  config-colors(
    primary: accent,
    secondary: rgb("#1e40af"),
    tertiary: accent-light,
    neutral-lightest: white,
  ),
)

#set text(size: 20pt)
#set list(spacing: 0.65em)
#set enum(spacing: 0.65em)

#title-slide()

// =====================================================================
// PART I — Hinton et al. 2015
// =====================================================================

// = Distilling the Knowledge in a Neural Network

== Introduction

#grid(
  columns: (1fr, 1fr),
  gutter: 1.5em,
  [
    #v(4em)
    #align(center)[
      #image("overview.png", width: 100%)
    ]
  ],
  [
    #v(5.5em)
    #align(center)[
      #image("quant.png", width: 100%)
    ]

  ],
)

== Motivation

#v(3em)
SOTA models are too large and slow
#v(0.3em)
Ensembles improve quality but complicate deployment
#v(0.3em)
We want a solution for industrial use
#v(0.3em)
The solution itself: distillation

== Classical Distillation Method

#grid(
  columns: (1fr, 1fr),
  gutter: 1.5em,
  [
    #v(2em)
    Notation:
    - $N$ — number of samples  
    - $K$ — number of classes  
    - $L_("KD")$ — distillation loss function  
    - $p_(i j)$ — class probabilities predicted by the student  
    - $y_(i j)$ — class labels (hard labels)  
    - $q_(i j)$ — class probabilities predicted by the teacher (soft labels) 
  ],
  [
    #v(3em)
    $ L_("KD") =
    1/N sum_(i=1)^N (
    - sum_(j=1)^K y_(i j) log p_(i j)
    + lambda D_("KL")(p_(i) || q_(i)))
    $

    $ =
    1/N sum_(i=1)^N (
    - sum_(j=1)^K y_(i j) log p_(i j)
    + lambda sum_(j=1)^K q_(i j) log (q_(i j) / p_(i j))
    )
    $

    $ approx
    -1/N sum_(i=1)^N ((
    sum_(j=1)^K y_(i j) log p_(i j)
    + lambda sum_(j=1)^K q_(i j) log p_(i j) ))
    $
  ],
)

#v(4em)
#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/1503.02531")[Hinton, G., Vinyals, O., & Dean, J. (2015). Distilling the knowledge in a neural network.]
]

== Classical Distillation Method

#v(2em)
    #align(center)[
      $ q_(i) = exp(z_(i) / T) / (sum_(j=1)^K exp(z_(j) / T))$
      #v(0.5em)
      #image("image.png", width: 70%)
      #v(0.5em)
      $ L_("KD") = - 1/N sum_(i=1)^N (sum_(j=1)^K y_(i j) log p_(i j) + lambda T^2 sum_(j=1)^K q_(i j)^T log p_(i j)^T)$
    ]

#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/1503.02531")[Hinton, G., Vinyals, O., & Dean, J. (2015). Distilling the knowledge in a neural network.]
]


== Experiments with MNIST

#v(2em)
Experiment 1:

- Teacher: 67 errors
- Student without distillation: 144 errors
- Student with distillation: 74 errors

Experiment 2:

- Without one class (3)
- 206 test errors, among which 133 are threes out of 1010 threes in MNIST
- If to add 3.5 to the bias, the model makes 109 errors, among which only 14 are threes and accuracy is 98.6%


#v(3.5em)
#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/1503.02531")[Hinton, G., Vinyals, O., & Dean, J. (2015). Distilling the knowledge in a neural network.]
]

== Distillation in Speech Recognition
#v(2em)
- Mapping an audio signal to text
- 8 layers
- 2560 neurons
- 85 million parameters
- 10 models in the ensemble
#align(center)[
#table(
  columns: 3,
  align: center,
  [*System*], [*Test Frame Accuracy*], [*WER*],
  [Baseline], [58.9%], [10.9%],
  [10× Ensemble], [61.1%], [10.7%],
  [Distilled Single Model], [60.8%], [10.7%],
)
]
#v(4.5em)
#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/1503.02531")[Hinton, G., Vinyals, O., & Dean, J. (2015). Distilling the knowledge in a neural network.]
]

== Specialist Ensembles

#v(2em)
=== JFT Dataset

- Internal Google dataset
- 100 million images
- 15,000 classes
- The base model was trained for 6 months
- Training an ensemble of models would take years

=== Solution

- Introduce one shared model
- Many specialists for similar classes

#v(4em)
#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/1503.02531")[Hinton, G., Vinyals, O., & Dean, J. (2015). Distilling the knowledge in a neural network.]
]

== Specialist Ensembles

#align(center)[
#table(
  columns: 3,
  align: center,
  [*System*], [*Conditional Test Accuracy*], [*Test Accuracy*],
  [Baseline], [43.1%], [25.0%],
  [+61 Specialist models], [45.9%], [26.1%],
)
#image("image copy.png", width: 90%)
]
#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/1503.02531")[Hinton, G., Vinyals, O., & Dean, J. (2015). Distilling the knowledge in a neural network.]
]

== Soft Targets as Regularizers

#v(2em)
#align(center)[
#image("image copy 2.png", width: 90%)
]

#v(10.5em)
#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/1503.02531")[Hinton, G., Vinyals, O., & Dean, J. (2015). Distilling the knowledge in a neural network.]
]

== Research / Practice

#v(1.5em)
=== On the one hand:

- SOTA models are huge
- Accuracy is high
- Require expensive hardware

=== On the other hand:

- In practice, small models are used
- ResNet-50, MobileNet
- Accuracy is lower, but they are fast and cheap to operate

#v(1.5em)

*Fact:* ResNet-50 is downloaded 10× more often than larger BiT models!


=== Goal of this paper

To analyze already existing methods

== Two Approaches to Compression

#v(2em)

1. *Pruning:*
  - Removes parts of a trained model
  - Problems:
    - Cannot change the model family (ResNet → MobileNet)
    - Architectural difficulties (GroupNorm, rebalancing)

2. *Distillation:*
  - Transfer of knowledge from teacher to student
  - The architecture can be changed!

== Proposals of This Paper

#v(2em)
1. *Consistency*
  - Teacher and student see the same crop/augmentation
  - No precomputation (no fixed teacher!)

2. *Aggressiveness*
  - Aggressive mixup
  - Creation of "synthetic" data outside the natural diversity

3. *Patience*
  - Very long training (thousands of epochs)
  - On ImageNet: 9600 epochs
// #text(size: 28pt, weight: "bold")[
// Knowledge distillation:
// ]

// #text(size: 28pt, weight: "bold")[
// A good teacher is patient and consistent
// ]

// #v(2em)

// Lucas Beyer*  
// Xiaohua Zhai*  
// Amélie Royer†  
// Larisa Markeeva‡  
// Rohan Anil  
// Alexander Kolesnikov*  

// Google Research, Brain Team

// #v(2em)

// 2022
#v(4em)
#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/2203.08674")[Beyer, L., Zhai, X., Royer, A., Markeeva, L., Anil, R., & Kolesnikov, A. (2022). Knowledge distillation: A good teacher is patient and consistent.]
]

== A good teacher is patient and consistent

#align(center)[
#image("distill.png", width: 90%)
]


#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/2203.08674")[Beyer, L., Zhai, X., Royer, A., Markeeva, L., Anil, R., & Kolesnikov, A. (2022). Knowledge distillation: A good teacher is patient and consistent.]
]

== Experiments

=== Data:

- 5 datasets: Flowers102, Pets, Food101, SUN397, ImageNet
- From 1,020 to 1.28M images and from 37 to 1000 classes

=== Models:

- Teacher: BiT-ResNet-152x2 (pretrained on ImageNet-21k)
- Student: ResNet-50 (with GroupNorm instead of BatchNorm)

=== Loss Function:

- KL divergence (soft targets only)
- With temperature T (as in Hinton)

=== Training:

- Adam, cosine schedule, gradient clipping
- Mixup with aggressive coefficients

#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/2203.08674")[Beyer, L., Zhai, X., Royer, A., Markeeva, L., Anil, R., & Kolesnikov, A. (2022). Knowledge distillation: A good teacher is patient and consistent.]
]

== Importance of Consistency

#v(2em)
#align(center)[
#image("consist1.png", width: 100%)
]

#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/2203.08674")[Beyer, L., Zhai, X., Royer, A., Markeeva, L., Anil, R., & Kolesnikov, A. (2022). Knowledge distillation: A good teacher is patient and consistent.]
]

== Importance of Patience

#v(2em)
#align(center)[
#image("consist2.png", width: 100%)
]

#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/2203.08674")[Beyer, L., Zhai, X., Royer, A., Markeeva, L., Anil, R., & Kolesnikov, A. (2022). Knowledge distillation: A good teacher is patient and consistent.]
]

== SoTA Compression

#v(2em)
#align(center)[
#image("sota.png", width: 70%)
]

#v(1em)
#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/2203.08674")[Beyer, L., Zhai, X., Royer, A., Markeeva, L., Anil, R., & Kolesnikov, A. (2022). Knowledge distillation: A good teacher is patient and consistent.]
]

== ImageNet Results

#v(2em)
#align(center)[
#image("imagnet.png", width: 80%)
]

#v(2.5em)
#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/2203.08674")[Beyer, L., Zhai, X., Royer, A., Markeeva, L., Anil, R., & Kolesnikov, A. (2022). Knowledge distillation: A good teacher is patient and consistent.]
]

== Function Matching

#v(2em)
#align(center)[
#image("func.png", width: 30%)
]

#v(1em)
#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/2203.08674")[Beyer, L., Zhai, X., Royer, A., Markeeva, L., Anil, R., & Kolesnikov, A. (2022). Knowledge distillation: A good teacher is patient and consistent.]
]

== Reasons of Bad Distillation

#v(2em)
1. It is bad to precompute the teacher (for computational savings),
   because consistency is lost, leading to poor results.

2. Training is too short
  - Distillation requires 10–100× more epochs

#v(11em)
#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/2203.08674")[Beyer, L., Zhai, X., Royer, A., Markeeva, L., Anil, R., & Kolesnikov, A. (2022). Knowledge distillation: A good teacher is patient and consistent.]
]


== Conclusions

#v(2em)
1. The knowledge distillation process should be viewed as a function approximation problem.

2. It is important to ensure that the teacher and student models receive the same and sufficiently diverse input data.

3. To achieve better student model performance, a large number of epochs should be used —
   significantly more than in standard training.

#v(8.5em)
#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/2203.08674")[Beyer, L., Zhai, X., Royer, A., Markeeva, L., Anil, R., & Kolesnikov, A. (2022). Knowledge distillation: A good teacher is patient and consistent.]
]

== Distillation in Language Models

#v(2em)
#align(center)[
#image("lang.png", width: 60%)
]

#v(2em)
#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/1908.08962")[Sanh, V., Debut, L., Chaumond, J., Wolf, T., & Rush, A. M. (2019). DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter.]
]

== Distillation in Generative Language Models

#v(2em)
#grid(
  columns: 2,
  gutter: 1.5em,
  [
    #align(center)[#image("gen1.png", width: 100%)]
  ],
  [
    #v(5em)
    #align(center)[#image("gen2.png", width: 100%)]
  ],
)

#v(3em)
#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/2306.08543")[Gu, Y., Dong, L., Wei, F., Huang, M., et al. (2023). MiniLLM: On-Policy Distillation of Large Language Models]
]

== Distillation in Generative Language Models

#v(2em)
$ 
L_("OD")(theta)
:= E_(x ~ X) [
  E_(y ~ p_S(. | x)) [
    D_("KL")(p_T || p_S^theta)(y | x)
  ]
]
$

#align(center)[
#image("algo.png", width: 50%)
]

$
L_("GKD")(theta)
:=
(1 - lambda)
  E_((x,y) ~ (X,Y))
    [ D(p_T || p_S^theta)(y | x) ]
+
lambda
  E_(x ~ X)
    [
      E_(y ~ p_S(. | x))
        [ D(p_T || p_S^theta)(y | x) ]
    ]
$

#v(2.5em)
#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/2306.13649")[Agarwal, R., Vieillard, N., Zhou, Y., Stanczyk, P., Ramos, S., Geist, M., Bachem, O. (2023). On-Policy Distillation of Language Models: Learning from Self-Generated Mistakes]
]

== Gemini 1.5 Flash (1)

#v(2em)
#align(center)[
#image("gemini1.png", width: 80%)
]

#v(5em)
#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/2403.05530")[Google DeepMind. (2024). Gemini 1.5: Unlocking Multimodal Understanding Across Millions of Tokens of Context.]
]

== Gemini 1.5 Flash (2)

#v(2em)
#align(center)[
#image("gemini2.png", width: 80%)
]

#v(2.5em)
#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/2403.05530")[Google DeepMind. (2024). Gemini 1.5: Unlocking Multimodal Understanding Across Millions of Tokens of Context.]
]

== Gemini 1.5 Flash (3)

#v(2em)
#align(center)[
#image("gemini3.png", width: 80%)
]

#v(6.5em)
#text(size: 0.7em, fill: luma(45%))[
  #link("https://arxiv.org/pdf/2403.05530")[Google DeepMind. (2024). Gemini 1.5: Unlocking Multimodal Understanding Across Millions of Tokens of Context.]
]

== References

#v(2em)
+ #link("https://arxiv.org/pdf/1503.02531")[Hinton, G., Vinyals, O., & Dean, J. (2015). _Distilling the Knowledge in a Neural Network._]

+ #link("https://education.yandex.ru/handbook/ml/article/distillyaciya-znanij")[Yandex Handbook — Knowledge Distillation]

+ #link("https://arxiv.org/pdf/2106.05237")[Beyer, L., Zhai, X., Royer, A., et al. (2022). _Knowledge Distillation: A Good Teacher is Patient and Consistent._]

+ #link("https://arxiv.org/pdf/2306.08543")[Gu, Y., Dong, L., Wei, F., Huang, M., et al. (2023). _MiniLLM: On-Policy Distillation of Large Language Models_]

+ #link("https://arxiv.org/pdf/2306.13649")[Agarwal, R., Vieillard, N., Zhou, Y., Stanczyk, P., Ramos, S., Geist, M., Bachem, O. (2023). _On-Policy Distillation of Language Models: Learning from Self-Generated Mistakes_]

+ #link("https://arxiv.org/pdf/2403.05530")[Google DeepMind. (2024). _Gemini 1.5: Unlocking Multimodal Understanding Across Millions of Tokens of Context._]

+ #link("https://arxiv.org/pdf/2305.02301")[Hsieh, C.-Y., et al. (2023). _Distilling Step-by-Step! Outperforming Larger Language Models with Less Training Data and Smaller Model Sizes._]

+ #link("https://arxiv.org/pdf/1908.08962")[Sanh, V., Debut, L., Chaumond, J., Wolf, T., & Rush, A. M. (2019). _DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter._]