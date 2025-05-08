import math
import re
import nltk
from nltk.corpus import words

nltk.download('words')
english_words = set(words.words())

def shannon_entropy(token):
    from collections import Counter
    prob = [freq / len(token) for freq in Counter(token).values()]
    return -sum(p * math.log2(p) for p in prob)

def is_suspicious(token):
    entropy = shannon_entropy(token)
    is_dict_word = token.lower() in english_words
    contains_weird_chars = bool(re.search(r'[^a-zA-Z0-9]', token))
    digit_ratio = sum(c.isdigit() for c in token) / (len(token) + 1e-5)
    
    # thresholds may require tuning
    if entropy > 3.5 and (not is_dict_word or digit_ratio > 0.3 or contains_weird_chars):
        return True
    return False