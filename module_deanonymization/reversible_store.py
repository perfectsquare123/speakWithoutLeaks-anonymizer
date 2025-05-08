import json
import os
from typing import Dict


class DeanonymizationStore:
    """
    Keeps track of mappings for reversible anonymization methods like tokenization and pseudonymization.
    """
    def __init__(self):
        self.entity_to_token: Dict[str, str] = {}
        self.token_to_entity: Dict[str, str] = {}
        self.counters: Dict[str, int] = {}

    def get_token(self, entity: str, label: str):
        """
        Returns an anonymized token for an entity, generates one if unseen.
        """
        if entity in self.entity_to_token:
            return self.entity_to_token[entity]

        # Generate new token
        self.counters[label] = self.counters.get(label, 0) + 1
        token = f"[{label}_{self.counters[label]:03d}]"
        self.entity_to_token[entity] = token
        self.token_to_entity[token] = entity
        
        return token

    def save(self, path_prefix: str):
        """
        Saves the mappings to disk as JSON files.
        """
        os.makedirs(os.path.dirname(path_prefix), exist_ok=True)

        with open(f"{path_prefix}_entity2token.json", "w") as f:
            json.dump(self.entity_to_token, f, indent=2)

        with open(f"{path_prefix}_token2entity.json", "w") as f:
            json.dump(self.token_to_entity, f, indent=2)

        with open(f"{path_prefix}_counters.json", "w") as f:
            json.dump(self.counters, f, indent=2)

    def load(self, path_prefix: str):
        """
        Loads mappings from disk.
        """
        with open(f"{path_prefix}_entity2token.json") as f:
            self.entity_to_token = json.load(f)

        with open(f"{path_prefix}_token2entity.json") as f:
            self.token_to_entity = json.load(f)

        with open(f"{path_prefix}_counters.json") as f:
            self.counters = json.load(f)