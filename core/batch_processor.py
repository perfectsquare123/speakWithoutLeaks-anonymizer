import pandas as pd
from typing import Union, List
from core.shared_scan import SharedProcessor


def sanitize_dataframe(
    df: pd.DataFrame,
    processor: SharedProcessor,
    text_column: str
) -> pd.DataFrame:
    """
    Sanitize a DataFrame column using the shared processor.
    Adds new columns: `sanitized_text` and `sanitized_pct`
    """
    sanitized_texts = []
    pct_modified = []

    for text in df[text_column]:
        original = str(text)
        sanitized = processor.sanitize_text(original)

        modified_pct = (
            (1 - sum(o == s for o, s in zip(original, sanitized)) / max(len(original), 1)) * 100
        )

        sanitized_texts.append(sanitized)
        pct_modified.append(round(modified_pct, 2))

    df["sanitized_text"] = sanitized_texts
    df["sanitized_pct"] = pct_modified
    return df


def sanitize_text_list(
    texts: List[str],
    processor: SharedProcessor
) -> List[str]:
    """
    Sanitize a list of text entries using the shared processor.
    """
    return [processor.sanitize_text(text) for text in texts]


def perturb_labels_column(
    df: pd.DataFrame,
    processor: SharedProcessor,
    label_column: str,
    num_classes: int
) -> pd.DataFrame:
    """
    Apply DP perturbation to classification labels in a DataFrame.
    Replaces the column with a new `perturbed_label` column.
    """
    labels = df[label_column].tolist()
    perturbed = processor.perturb_labels(labels, num_classes)
    df["perturbed_label"] = perturbed
    return df