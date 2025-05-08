
import argparse
import pandas as pd
import json
import os
import time
from core.shared_scan import SharedProcessor
from core.batch_processor import sanitize_dataframe, sanitize_text_list, perturb_labels_column
from core.data_loader import load_data
from core.batch_utils import process_large_csv
from module_customization.config_parser import load_config

def parse_args():
    parser = argparse.ArgumentParser(description="Run Privacy-Preserving Data Sanitization Pipeline")

    parser.add_argument("--input", "-i", required=True, help="Input file path (.csv or .txt)")
    parser.add_argument("--output", "-o", required=True, help="Path to save sanitized output (.csv or .txt)")
    parser.add_argument("--config", "-c", default="config/default_config.yaml", help="Path to config YAML")
    parser.add_argument("--text-column", "-tc", default="text", help="Text column name (for CSV)")
    parser.add_argument("--label-column", "-lc", default=None, help="Label column name (for CSV)")
    parser.add_argument("--num-classes", "-nc", type=int, default=None, help="Total number of label classes (for DP label perturbation)")
    parser.add_argument("--batch", "-b", action="store_true", help="Enable batch mode for large CSV files")
    
    return parser.parse_args()


def main():
    args = parse_args()
    config = load_config(args.config)
    processor = SharedProcessor(config)
    
    print()
    start_time = time.time()
    total_entities_anonymized = 0

    ext = os.path.splitext(args.input)[-1].lower()

    if ext == ".csv":
        if args.batch:
            process_large_csv(
                input_path=args.input,
                output_path=args.output,
                processor=processor,
                text_column=args.text_column,
                label_column=args.label_column,
                num_classes=args.num_classes,
                batch_size=config["processing"].get("batch_size", 500)
            )
        else:
            df = pd.read_csv(args.input)
            df = sanitize_dataframe(df, processor, args.text_column)

            if args.label_column and args.num_classes:
                df = perturb_labels_column(df, processor, args.label_column, args.num_classes)

            df.to_csv(args.output, index=False)
            print(f"===> Sanitized CSV written to {args.output}")

    elif ext == ".txt":
        data = load_data(args.input)
        sanitized = sanitize_text_list(data, processor)

        with open(args.output, "w", encoding="utf-8") as f:
            for line in sanitized:
                f.write(line + "\n")
        print(f"===> Sanitized TXT written to {args.output}")

    else:
        raise ValueError(f"Unsupported file type: {ext}")

    end_time = time.time()
    elapsed = end_time - start_time
    print("\n========== Time Taken =============\n")
    print(f"⏱ Time taken: {elapsed:.2f} seconds\n")
    print("=====================================\n")
    
    if processor.store_enabled:
        print("\n=== saving the mappings ===\n")
        processor.save_deanonymization_store("output/mapping")

if __name__ == "__main__":
    main()