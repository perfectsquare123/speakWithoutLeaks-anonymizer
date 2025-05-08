import re
from typing import Dict

def load_reverse_mapping(path_prefix: str) -> Dict[str, str]:
    """Load the token-to-entity mapping from a saved deanonymization store."""
    import json
    with open(f"{path_prefix}_token2entity.json", "r", encoding="utf-8") as f:
        return json.load(f)

def reverse_text(sanitized_text: str, token_to_entity: Dict[str, str]) -> str:
    """
    Replace anonymized tokens (e.g., [PERSON_001]) in text with their original values.
    """
    # Match tokens like [PERSON_001], [ORG_005], etc.
    pattern = re.compile(r"\[(\w+_\d{3})\]")

    def replace_token(match):
        token = f"[{match.group(1)}]"
        return token_to_entity.get(token, token)

    return pattern.sub(replace_token, sanitized_text)

def reverse_file(input_path: str, output_path: str, mapping_prefix: str):
    """Reverse all deanonymized tokens in a text file using stored mappings."""
    token_to_entity = load_reverse_mapping(mapping_prefix)

    with open(input_path, "r", encoding="utf-8") as fin:
        lines = fin.readlines()

    reversed_lines = [reverse_text(line, token_to_entity) for line in lines]

    with open(output_path, "w", encoding="utf-8") as fout:
        fout.writelines(line + ("\n" if not line.endswith("\n") else "") for line in reversed_lines)

    print(f"===> Reversed file written to {output_path}")