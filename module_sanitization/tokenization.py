from module_deanonymization.reversible_store import DeanonymizationStore

def tokenize(text: str, label: str, store: DeanonymizationStore = None):
    """
    Replace text with reversible placeholder like [PERSON_001].
    Uses reversible store to ensure consistent mapping.
    """
    if store:
        return store.get_token(text, label)
    return f"[{label}]"