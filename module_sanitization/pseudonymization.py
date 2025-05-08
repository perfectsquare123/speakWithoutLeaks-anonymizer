import random
from config.dictionary import PSEUDO_DICT

def pseudonymize(text: str, label: str = "PERSON"):
    """Replace with a random pseudonym from a predefined list for the entity label."""
    return random.choice(PSEUDO_DICT.get(label, [f"[{label}]"]))