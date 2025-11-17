#set document(
  title: "Homework 2",
  author: "Danila Biktimirov",
  date: auto
)
#set text(font: "Linux Libertine", lang: "en")
#set heading(numbering: "1.")

#align(center)[
  #text(size: 20pt, weight: "bold")[Homework 2 Report]
  #v(0.1em)
  // #text(size: 16pt)[Self-Supervised Pre-training with Pretext Tasks]
  // #v(2em)
  #text(size: 12pt)[
    Danila Biktimirov
  ]
  #v(1em)
  // #today("October 18, 2025")
]

= Methods Explored

Three self-supervised pre-training strategies were investigated to learn robust features from the unlabeled dataset.

== Method 1: Rotation Prediction (RotNet)

This pretext task is based on the idea that a model must understand an object's features to determine its orientation.

- *Pre-training:* A `ResNet-18` model, with its final layer modified to have 4 outputs, was trained on the unlabeled dataset. For each image, a random rotation (0°, 90°, 180°, or 270°) was applied, and the model's task was to predict which of the four rotations was used.

- *Fine-tuning:* The weights from the pre-trained backbone were transferred to a new `ResNet-18` model with a 10-class classifier for the downstream task.

== Method 2: Jigsaw Puzzles

This is a more complex task designed to teach the model about the spatial relationship between an object's parts.

- *Pre-training:* Each unlabeled image was divided into a 3x3 grid of 9 patches. These patches were shuffled according to one of 100 predefined permutations. A Siamese network, using a shared `ResNet-18` backbone to process each patch, was trained to predict which of the 100 permutations was applied.

- *Fine-tuning:* The learned weights of the shared `ResNet-18` backbone were used to initialize the final 10-class model.

= Experiments to choose pre-traing method

#table(
  columns: (auto, auto, auto, auto),
  align: (center, center, center, center),
  stroke: 0.5pt,
  [*Method*], [*Pre-training Final Accuracy*], [*Fine-tuning Final Val Accuracy*], [*Kaggle Public Score*],
  
  [Jigsaw Puzzles 30/30],
  [0.9322],
  [0.6251],
  [0.6283],
  
  [Jigsaw Puzzles 100/50],
  [0.9733],
  [0.6731],
  [0.6351],
  
  [RotNet 30/30],
  [0.8394],
  [0.6442],
  [0.6556],

  [RotNet 100/50],
  [0.9238],
  [0.7356],
  [0.6917],

)

At this stage, I decided to choose RotNet and improve it rather than conducting 100,500 different experiments with all possible models. It would probably be possible to continue trying to extract a decent score from the JigSaw method. How else can pretraining be improved?

== Method 3: Multi-Task Pre-training (Rotation + Color)

To learn a richer set of features, a multi-task approach was implemented, training the model on two pretext tasks simultaneously.

- *Pre-training Architecture:* The `ResNet-18` backbone was equipped with two separate linear heads: one for rotation prediction (4 classes) and another for a colorization proxy task (2 classes).
- *Tasks:*
  + *Rotation:* Same as Method 1.
  + *Colorization Proxy:* With a 50% probability, input images were converted to grayscale. The second head was trained to predict whether the image was in its original color or had been converted to grayscale.
- *Training:* The model was trained to minimize the sum of the losses from both tasks, forcing the backbone to learn features useful for both geometric understanding (from rotation) and texture/detail analysis (from color).
// ===============================================
// Enhancements to the Fine-Tuning Process
// ===============================================
= Enhancements to the Fine-Tuning Process

To maximize the final classification accuracy, several advanced techniques were applied during the fine-tuning stage.

== Advanced Augmentation Strategies

- *RandAugment:* The initial set of simple augmentations was replaced with `RandAugment`, which automatically applies a diverse sequence of transformations with random magnitudes. This provides strong regularization.
- *CutMix:* A more advanced technique where a random patch from one image is cut and pasted onto another image in the same batch. The labels are then mixed proportionally to the area of the patch. This forces the model to learn to identify objects without relying on their full context and improves localization.

== Two-Stage Fine-Tuning

A gradual unfreezing strategy was adopted to stabilize training and protect the learned features.

*Stage 1 (Head Training):* The pre-trained backbone was "frozen" (weights were not updated), and only the newly added 10-class classification head was trained for a few epochs with a higher learning rate. This allows the head to adapt without corrupting the backbone's weights with large, random gradients.

*Stage 2 (Full Fine-tuning):* The entire model was "unfrozen," and all layers were trained end-to-end with a smaller learning rate to fine-tune the complete network.

== Optimization and Regularization Improvements

- *Optimizer:* The standard `Adam` optimizer was replaced with `AdamW`, an improved version that handles weight decay more effectively, often leading to better generalization.
- *Learning Rate Scheduler:* A `CosineAnnealingLR` scheduler was used to smoothly decay the learning rate from its initial value to a minimum, which helps the model converge more stably to a better minimum.
- *Label Smoothing:* Instead of using hard one-hot encoded labels, a `CrossEntropyLoss` with `label_smoothing` was used. This technique prevents the model from becoming overconfident in its predictions, acting as a powerful regularizer.

= Final experiments and Results

To find the optimal strategy, several experiments were conducted. All approaches utilized a multi-task pre-training objective (combining Rotation and Color prediction) before the fine-tuning stage.

The primary and most successful experiment involved pre-training a standard `ResNet-18` model for 100 epochs. On the pretext tasks, this model achieved a final accuracy of #strong("89% for rotation prediction") and #strong("96% for the color prediction task"). The resulting backbone was then fine-tuned using a comprehensive strategy that included:
- A #strong("two-stage fine-tuning process"), where the classification head was trained first for 10 epochs.
- The use of #strong("CutMix") augmentation and #strong("Label Smoothing") (`0.1`).
- The #strong("AdamW") optimizer with a #strong("Cosine Annealing learning rate scheduler").
This combination of techniques proved highly effective, achieving a final and best validation accuracy of #strong("75.96%").

An alternative approach was also explored, leveraging the rules to pre-train a more powerful `ResNet-34` backbone. This pre-training process was manually interrupted after 86 epochs, at which point it had reached accuracies of #strong("~88% for rotation") and #strong("~96% for color"). The partially trained backbone was subsequently used to fine-tune a `ResNet-18` model using an advanced strategy with CutMix, Label Smoothing, AdamW, and #strong("discriminative learning rates"). Due to the incomplete pre-training, this experiment yielded a significantly lower validation accuracy of #strong("62.02%"), highlighting the critical importance of a fully converged pre-training stage for achieving optimal performance.

P.S. Sorry that this report is without any plots, I am balbes and I forgot to do this homework with WandB
  