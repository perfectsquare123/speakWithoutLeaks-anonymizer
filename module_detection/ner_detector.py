# detection/ner_detector.py

import spacy
import stanza
from stanza.pipeline.core import DownloadMethod
from transformers import pipeline
from typing import List, Dict, Any


class NERDetector:
    def __init__(self, method: str = "spacy", model_name: str = "en_core_web_sm"):
        self.method = method
        self.model_name = model_name

        if method == "spacy":
            self.nlp = spacy.load(model_name)
        elif method == "stanza":
            self.nlp = stanza.Pipeline(lang='en', processors='tokenize,ner', download_method=DownloadMethod.REUSE_RESOURCES)
        elif method == "transformers":
            self.ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")
        else:
            raise ValueError(f"Unsupported NER method: {method}")

    def detect(self, text: str) -> List[Dict[str, Any]]:
        entities = []

        if self.method == "spacy":
            doc = self.nlp(text)
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char
                })

        elif self.method == "stanza":
            doc = self.nlp(text)
            for sentence in doc.sentences:
                for ent in sentence.ents:
                    entities.append({
                        "text": ent.text,
                        "label": ent.type,
                        "start": ent.start_char,
                        "end": ent.end_char
                    })

        elif self.method == "transformers":
            results = self.ner_pipeline(text)
            for ent in results:
                entities.append({
                    "text": ent["word"],
                    "label": ent["entity_group"],
                    "start": ent["start"],
                    "end": ent["end"]
                })

        return entities
