import csv
import random
import string
from faker import Faker
from typing import List, Tuple

fake = Faker()

def generate_encrypted_token(length=8, style="random"):
    if style == "base64":
        base64_chars = string.ascii_letters + string.digits + "+/"
        return ''.join(random.choices(base64_chars, k=length))
    elif style == "hex":
        return ''.join(random.choices("0123456789abcdef", k=length))
    else:  # random
        return ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*()-_+=|\\[]{}\"':;/?.>,<", k=length))

def inject_encrypted_token(tokens: List[str], enc_style: str = "random", prob=0.3) -> Tuple[List[str], List[str]]:
    new_tokens = []
    labels = []
    for tok in tokens:
        if random.random() < prob:
            enc_token = generate_encrypted_token(length=random.randint(6, 12), style=enc_style)
            new_tokens.append(enc_token)
            labels.append("B-ENC")
        else:
            new_tokens.append(tok)
            labels.append("O")
    return new_tokens, labels

def create_synthetic_sentence(max_len=10) -> Tuple[List[str], List[str]]:
    base = fake.sentence(nb_words=random.randint(5, max_len)).strip(".").split()
    return inject_encrypted_token(base)

def generate_dataset(num_samples=1000, enc_style="random") -> List[Tuple[str, str]]:
    dataset = []
    for _ in range(num_samples):
        tokens, labels = create_synthetic_sentence()
        token_str = " ".join(tokens)
        label_str = " ".join(labels)
        dataset.append((token_str, label_str))
    return dataset

def save_dataset_csv(dataset: List[Tuple[str, str]], filename: str):
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["tokens", "labels"])
        for row in dataset:
            writer.writerow(row)

# Example usage
# if __name__ == "__main__":
#     dataset = generate_dataset(num_samples=5000, enc_style="base64")
#     save_dataset_csv(dataset, "synthetic_enc_dataset.csv")

