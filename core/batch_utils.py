import pandas as pd
from core.shared_scan import SharedProcessor
from core.batch_processor import sanitize_dataframe, perturb_labels_column
from typing import Generator

def batch_iterator(df: pd.DataFrame, batch_size: int) -> Generator[pd.DataFrame, None, None]:
    """
    Yield DataFrame in batches.
    """
    for start in range(0, len(df), batch_size):
        yield df.iloc[start:start + batch_size]

def process_large_csv(
    input_path: str,
    output_path: str,
    processor: SharedProcessor,
    text_column: str,
    label_column: str = None,
    num_classes: int = None,
    batch_size: int = 1000
):
    """
    Process large CSV file in batches with text and optional label sanitization.
    Appends results to output file incrementally.
    """
    reader = pd.read_csv(input_path, chunksize=batch_size)
    header_written = False
    count = 0

    for chunk in reader:
        chunk = sanitize_dataframe(chunk, processor, text_column)

        if label_column and num_classes is not None:
            chunk = perturb_labels_column(chunk, processor, label_column, num_classes)

        # Write header only for first chunk
        chunk.to_csv(output_path, mode='a', index=False, header=not header_written)
        header_written = True
        
        count += batch_size
        print(f"- processed {count} records -")
        

    print(f"\nDone processing!!\n===> Batch-sanitized dataset written to {output_path}\n")