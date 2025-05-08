import argparse
from module_deanonymization.reverse_text import reverse_file

def parse_args():
    parser = argparse.ArgumentParser(description="Reverse deanonymized text using saved token mappings")
    parser.add_argument("--input", "-i", required=True, help="Path to sanitized text file (.txt)")
    parser.add_argument("--output", "-o", required=True, help="Path to write reversed text file")
    parser.add_argument("--mapping", "-m", required=True, help="Prefix path to token2entity mapping (omit extension)")

    return parser.parse_args()

def main():
    args = parse_args()
    reverse_file(
        input_path=args.input,
        output_path=args.output,
        mapping_prefix=args.mapping
    )

if __name__ == "__main__":
    main()