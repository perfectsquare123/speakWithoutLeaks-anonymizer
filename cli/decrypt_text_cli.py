import argparse
import re
from module_sanitization import fpe_encrypt, aes_encrypt
import yaml
from module_detection import encrypted_word_detector

def decrypt_line(line: str, method: str, config: dict) -> str:
    words = line.strip().split()
    decrypted_words = []

    for word in words:
        if encrypted_word_detector.is_suspicious(word):
            try:
                if method == "fpe":
                    decrypted = fpe_encrypt.decrypt(word, config)
                    print(decrypted)
                elif method == "aes":
                    decrypted = aes_encrypt.decrypt(word, config)
                else:
                    decrypted = word
            except Exception:
                decrypted = word
        else:
            decrypted = word
        decrypted_words.append(decrypted)

    return ' '.join(decrypted_words)

def decrypt_file(input_path: str, output_path: str, method: str, config_path: str):
    with open(config_path, "r") as f:
        full_config = yaml.safe_load(f)
    config = full_config["sanitization"]["technique_params"]["encrypt"]

    with open(input_path, "r", encoding="utf-8") as fin:
        lines = fin.readlines()

    decrypted_lines = [decrypt_line(line, method, config) for line in lines]

    with open(output_path, "w", encoding="utf-8") as fout:
        for line in decrypted_lines:
            fout.write(line + ("\n" if not line.endswith("\n") else ""))

    print(f"===> Decrypted file written to {output_path}")

def parse_args():
    parser = argparse.ArgumentParser(description="Decrypt FPE or AES encrypted text lines")
    parser.add_argument("--input", "-i", required=True, help="Path to encrypted input file (.txt)")
    parser.add_argument("--output", "-o", required=True, help="Path to save decrypted text file")
    parser.add_argument("--method", "-m", required=True, choices=["fpe", "aes"], help="Decryption method to use")
    parser.add_argument("--config", "-c", required=True, help="Path to YAML config file containing the encryption key")

    return parser.parse_args()

def main():
    args = parse_args()
    decrypt_file(
        input_path=args.input,
        output_path=args.output,
        method=args.method,
        config_path=args.config
    )

if __name__ == "__main__":
    main()