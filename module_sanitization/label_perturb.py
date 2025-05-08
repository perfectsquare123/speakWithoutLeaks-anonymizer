
import random
import math
from typing import List

def add_label_noise(labels: List[int], num_classes: int, epsilon: float) -> List[int]:
    """
    Apply ε-DP label perturbation using the randomized response mechanism.
    Args:
        labels: list of integer class labels
        num_classes: total number of possible classes
        epsilon: privacy budget
    Returns:
        noisy_labels: list of perturbed labels
    """
    remain_ori_label_prob = math.exp(epsilon) / (math.exp(epsilon) + num_classes - 1)
    noise_prob = 1 - remain_ori_label_prob
    noisy_labels = []

    for label in labels:
        if random.random() < noise_prob:
            noisy = random.choice([x for x in range(num_classes) if x != label])
        else:
            noisy = label
        noisy_labels.append(noisy)

    return noisy_labels