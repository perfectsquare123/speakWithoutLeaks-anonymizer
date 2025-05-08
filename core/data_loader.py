# core/data_loader.py

import os
import csv
import json

def load_csv(path, batch_size=None):
    """Load CSV file. Returns list of dicts (each row as dict) or batches."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"CSV file not found at {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    if batch_size:
        return [data[i:i+batch_size] for i in range(0, len(data), batch_size)]
    return data


def load_txt(path, batch_size=None):
    """Load TXT file. Returns list of strings or batches."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"TXT file not found at {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    if batch_size:
        return [lines[i:i+batch_size] for i in range(0, len(lines), batch_size)]
    return lines


def load_data(path, batch_size=None):
    """Auto-detect file type and delegate to correct loader."""
    ext = os.path.splitext(path)[-1].lower()
    if ext == '.csv':
        return load_csv(path, batch_size)
    elif ext == '.txt':
        return load_txt(path, batch_size)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
