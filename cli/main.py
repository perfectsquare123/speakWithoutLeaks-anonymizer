# cli/main.py

import argparse
import json
from core.data_loader import load_data
from module_customization.config_parser import load_config

def parse_args():
    parser = argparse.ArgumentParser(description="Privacy-Preserving Data Pipeline CLI")

    parser.add_argument('--input', '-i', type=str, required=True,
                        help='Path to input file (.csv or .txt)')
    parser.add_argument('--output', '-o', type=str, required=True,
                        help='Path to write sanitized output')
    parser.add_argument('--config', '-c', type=str, default='config/default_config.json',
                        help='Path to sanitization config file (JSON)')
    parser.add_argument('--batch-size', '-b', type=int, default=None,
                        help='Optional batch size for large data processing')

    return parser.parse_args()


def main():
    args = parse_args()

    print(f"[INFO] Loading data from {args.input}...")
    data = load_data(args.input, args.batch_size)
    print(f"[INFO] Loaded {len(data)} records{' (batched)' if args.batch_size else ''}.")

    # Load config
    config = load_config(args.config)
    print(f"[INFO] Using config: {args.config}")

    # Here: you will call the pipeline (e.g., shared_scan.process(data, config)) later

    # Placeholder output
    print(f"[INFO] Would write sanitized output to {args.output} (not yet implemented).")


if __name__ == '__main__':
    main()
