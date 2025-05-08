from config.dictionary import GENERALIZE_DICT

def generalize(text: str, label: str = "PERSON"):
    """Replace entity with a generalized placeholder value based on label."""
    return f"{GENERALIZE_DICT.get(label, label)}"