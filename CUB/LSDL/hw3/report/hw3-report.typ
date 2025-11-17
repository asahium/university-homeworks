#set document(
  title: "Homework 3",
  author: "Danila Biktimirov",
  date: auto
)
#set text(font: "Linux Libertine", lang: "en")
#set heading(numbering: "1.")

#align(center)[
  #text(size: 20pt, weight: "bold")[Homework 3 Report]
  #v(1em)
  #text(size: 12pt)[
    Danila Biktimirov
  ]
  #v(1em)
]

= Pre-training Methods and Hyperparameters
Four distinct training strategies were executed to generate feature encoders.

== Supervised Baseline
A baseline model was trained using the labeled data to establish a performance benchmark. This model was trained for 100 epochs with a batch size of 256. It utilized an SGD optimizer with a learning rate of 0.1, momentum of 0.9, and a weight decay of 5e-4.

== SimCLR (Simple Contrastive Learning)
SimCLR is a contrastive method that learns representations by maximizing agreement between two differently augmented views of the same image (positive pairs) while contrasting them against augmented views of other images (negative pairs) within the same batch. This approach requires a large batch size to provide a sufficient number of negative examples. The model was trained for 100 epochs with a batch size of 4096, an Adam optimizer with a learning rate of 3e-4, a temperature of 0.5 for the loss function, and a projection dimension of 128.

== BYOL (Bootstrap Your Own Latent)
BYOL learns by using an asymmetric architecture with two networks: an online network and a target network, where the target network is a slow-moving average of the online network. It predicts the target network's representation of one augmented view from the online network's representation of another view. This method avoids the need for negative pairs. BYOL was trained for 100 epochs with a batch size of 512, a learning rate of 3e-4, an EMA momentum of 0.996, a projection dimension of 256, and a hidden dimension of 4096.

== MoCo (Momentum Contrast)
MoCo implements contrastive learning using a dictionary look-up approach. It maintains a dynamic queue of negative samples, allowing it to use a much larger set of negatives than the batch size would typically allow. A momentum-updated encoder is used to ensure the queue's representations are consistent. MoCo was trained for 40 epochs with a batch size of 256. Key parameters included an SGD optimizer with a learning rate of 0.03, an encoder momentum of 0.999, a temperature of 0.2, a queue size of 4096, a projection dimension of 128, and weight decay of 1e-4.

= Evaluation Protocols
To assess the quality of the pre-trained encoders, two downstream tasks were performed using the labeled STL10 data.

== Linear Probing
In this setup, the weights of the pre-trained encoder backbone were frozen. A single linear classification layer was trained on top of these fixed features. This protocol measures the linear separability of the learned representations. The linear probe was trained for 50 epochs with a learning rate of 1e-3.

== Fine-Tuning
The fine-tuning process ran for 50 epochs using an SGD optimizer with a learning rate of 0.01, momentum of 0.9, and weight decay of 5e-4.

= Results and Analysis

The performance of each pre-trained model was measured by its final test accuracy on the downstream classification task. The learning curves for all experiments, logged via wandb, are to be inserted below.

#image("train_loss.png")

#image("train_acc.png")

#image("test_acc.png")

#image("projection_srd.png")

#image("image (1).png")
The t-SNE plot provides a strong qualitative justification for the results. The SimCLR shows some separation, but clusters are mixed. BYOL is cleaner, but Supervised model produce exceptionally tight, well-defined, and linearly separable clusters. This visualization matches the theoretical results if BYOL and SimCLR were trained longer.

The final accuracy results are summarized in the table below.

#table(
  columns: (auto, auto, auto, auto),
  align: (center, center, center, center),
  stroke: 0.5pt,
  [*Model*], [*Epochs*], [*STL-10 Test Acc (%)*], [*CIFAR-10 OOD Acc (%)*],
  
  [Supervised],
  [100],
  [ 74.51 ],
  [ 21.78 ],
  
  [SimCLR + Linear Probe],
  [50],
  [ 55.71 ],
  [ 32.58 ],
  
  [SimCLR + Fine-tuning],
  [50],
  [ 70.62 ],
  [ 20.93 ],

  [BYOL + Linear Probe],
  [50],
  [ 64.76 ],
  [ 45.34 ],
  
  [BYOL + Fine-tuning],
  [50],
  [ 74.86 ],
  [ 17.23 ],
  
  [MoCo + Linear Probe],
  [50],
  [ 57.30 ],
  [ 45.68 ],

  [MoCo + Fine-tuning],
  [50],
  [ 72.95 ],
  [ 20.02 ]
)

== Analysis

#image("plot results.png")

The experimental results, summarized in the table, reveal a complex trade-off between in-distribution performance and out-of-distribution (OOD) generalization.

1.  *In-Distribution (STL-10) Performance:*
    -   The Supervised model (74.51%) sets a strong baseline.
    -   SSL fine-tuning provides minimal benefit. BYOL (74.86%) just barely surpasses the supervised model. MoCo (72.95%) and SimCLR (70.62%) actually underperform, suggesting the pre-training did not provide a clear advantage for this specific task and set of hyperparameters.
    -   There is a large performance gap between linear probing (e.g., BYOL 64.76%) and fine-tuning (BYOL 74.86%). This indicates that, unlike in some other studies, the pre-trained features were not perfectly linearly separable and required significant fine-tuning of the backbone to achieve competitive accuracy.

2.  *Out-of-Distribution (CIFAR-10) Generalization:*
    -   This is the most critical finding. The SSL linear probes (frozen backbones) show vastly superior OOD performance compared to all other methods.
    -   MoCo (45.68%) and BYOL (45.34%) are the clear winners, more than doubling the OOD accuracy of the Supervised baseline (21.78%). This proves that SSL pre-training learns more general and robust features that transfer better to new domains.
    -   Crucially, this advantage is lost during fine-tuning. When the SSL backbones are unfrozen and fine-tuned on STL-10, their OOD accuracy collapses to (or below) the supervised level. BYOL, the best OOD linear probe, becomes the worst OOD model after fine-tuning (17.23%).

*Conclusion:* SSL pre-training (especially MoCo and BYOL) is highly effective at learning general, robust representations that excel at out-of-distribution tasks. However, fine-tuning these models on a specific downstream task (STL-10) causes them to "catastrophically forget" this generality and specialize, destroying their OOD performance. For tasks requiring robustness to domain shift, using a frozen SSL backbone with a linear probe is demonstrably superior to end-to-end fine-tuning.