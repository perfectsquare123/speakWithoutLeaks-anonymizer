import re
from typing import List, Dict, Any


class RegexDetector:
    def __init__(self, regex_patterns: Dict[str, str]):
        """
        regex_patterns: dict mapping entity label to regex pattern
        """
        self.regex_patterns = regex_patterns

    def detect(self, text: str) -> List[Dict[str, Any]]:
        entities = []

        for label, pattern in self.regex_patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                entities.append({
                    "text": match.group(),
                    "label": label,
                    "start": match.start(),
                    "end": match.end()
                })

        return entities