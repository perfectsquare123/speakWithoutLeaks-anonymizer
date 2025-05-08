# core/shared_scan.py

from module_detection.ner_detector import NERDetector
from module_detection.regex_detector import RegexDetector
from module_sanitization import tokenization, pseudonymization, generalization, redaction, fpe_encrypt, dp_sanitize, aes_encrypt, label_perturb
from typing import List, Dict, Any
import copy
import re
from module_deanonymization.reversible_store import DeanonymizationStore


class SharedProcessor:
    def __init__(self, config: Dict[str, Any]):
        # Load config
        self.config = config

        # Initialize detectors
        self.ner_detector = NERDetector(method=config["detection"]["ner_model"])
        self.regex_detector = RegexDetector(config["detection"].get("regex_patterns", {}))

        # Priority: 'regex' or 'ner'
        self.priority = config["detection"].get("priority", "regex")

        # Strategy config
        self.entity_strategies = config["sanitization"]["entity_strategies"]
        self.technique_params = config["sanitization"].get("technique_params", {})
        
        # Initialize optional deanonymization store
        self.store_enabled = config.get("processing", {}).get("deanonymization_store", False)
        self.store = DeanonymizationStore() if self.store_enabled else None

    def detect_entities(self, text: str) -> List[Dict[str, Any]]:
        """Run both NER and regex detection, resolve overlap."""
        ner_entities = self.ner_detector.detect(text)
        regex_entities = self.regex_detector.detect(text)

        if self.priority == "regex":
            ner_entities = [e for e in ner_entities if not self._overlap(e, regex_entities)]
            merged = regex_entities + ner_entities
        else:
            regex_entities = [e for e in regex_entities if not self._overlap(e, ner_entities)]
            merged = ner_entities + regex_entities

        return sorted(merged, key=lambda e: e["start"])

    def _overlap(self, entity: Dict, others: List[Dict]) -> bool:
        """Check if an entity overlaps with any in the other list."""
        for o in others:
            if not (entity["end"] <= o["start"] or entity["start"] >= o["end"]):
                return True
        return False

    def sanitize_text(self, text: str) -> str:
        """Main entrypoint. Detect and sanitize sensitive entities in text."""
        entities = self.detect_entities(text)

        if not entities:
            return text

        # Perform replacement in reverse order to preserve indices
        sanitized = text
        for entity in reversed(entities):
            sanitized_text = self.apply_sanitization(entity, text)
            sanitized = sanitized[:entity["start"]] + sanitized_text + sanitized[entity["end"]:]

        return sanitized

    def apply_sanitization(self, entity: Dict[str, Any], original_text: str):
        label = entity["label"]
        raw_text = entity["text"]
        method = self.entity_strategies.get(label)

        if not method:
            return raw_text  # skip if no strategy defined

        # Dispatch to appropriate method
        if method == "tokenize":
            return tokenization.tokenize(raw_text,label,store=self.store)
        elif method == "pseudonymize":
            return pseudonymization.pseudonymize(raw_text, label)
        elif method == "generalize":
            return generalization.generalize(raw_text, label)
        elif method == "redact":
            return redaction.redact(raw_text)
        elif method == "fpe":
            return fpe_encrypt.encrypt(raw_text, self.technique_params.get("encrypt", {}))
        elif method == "aes":
            return aes_encrypt.encrypt(raw_text, self.technique_params.get("encrypt", {}))
        elif method == "dp":
            return dp_sanitize.perturb(raw_text, self.technique_params.get("dp", {}).get("text_perturb", {}))
        else:
            return raw_text  # fallback

    def save_deanonymization_store(self, path_prefix: str):
        """Save the reversible mappings if enabled."""
        if self.store_enabled and self.store:
            self.store.save(path_prefix)
            
    def perturb_labels(self, labels: List[int], num_classes: int) -> List[int]:
        """Apply label-level DP perturbation to a list of labels."""
        config = self.technique_params.get("dp", {}).get("label_perturb", {})
        if config.get("enable", False):
            epsilon = config.get("epsilon", 1.0)
            return label_perturb.add_label_noise(labels, num_classes, epsilon)
        return labels

    def _is_text_dp_enabled(self) -> bool:
        return self.technique_params.get("dp", {}).get("text_perturb", {}).get("enable", False)