import random
import math
from typing import List, Dict
import spacy
from faker import Faker
import numpy as np
from sentence_transformers import SentenceTransformer

# Load semantic model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_similarity(a: str, b: str):
    emb_a = model.encode(a)
    emb_b = model.encode(b)
    score = float(np.dot(emb_a, emb_b) / (np.linalg.norm(emb_a) * np.linalg.norm(emb_b)))
    # print("score: ", score)
    
    return score

# def allocate_budget(entities: List, total_epsilon: float) -> Dict:
#     """Allocate more epsilon to more sensitive entities"""
#     sensitivities = {
#         "PERSON": 0.6,
#         "CREDIT_CARD": 0.9,
#         "GPE": 0.4,
#         "EMAIL": 0.8,
#         "PHONE": 0.5,
#         "DATE": 0.3
#     }
#     total_weight = sum(sensitivities.get(e.label_, 0.1) for e in entities)
#     return {e: (sensitivities.get(e.label_, 0.1)/total_weight)*total_epsilon for e in entities}

class EntityPerturber:
    def __init__(self, epsilon: float = 1.0, protected_entity_types: List[str] = None):
        self.epsilon = epsilon
        self.entity_types = set(protected_entity_types or [])
        self.fake = Faker()
        self.replacement_dict = {
            "PERSON": [self.fake.name() for _ in range(5)],
            "GPE": [self.fake.city() for _ in range(5)],
            "DATE": [self.fake.date() for _ in range(5)],
            "PHONE": [self.fake.phone_number() for _ in range(5)],
            "EMAIL": [self.fake.email() for _ in range(5)],
            "CREDIT_CARD": [self.fake.credit_card_number() for _ in range(5)]
        }
        self.nlp = spacy.load("en_core_web_sm")
        
    def _exponential_mechanism(self, original: str, candidates: List[str], epsilon: float) -> str:
        scores = [math.exp(epsilon * semantic_similarity(original, c)) for c in candidates]
        total = sum(scores)
        probs = [s / total for s in scores]
        # print("candidates: ", candidates)
        # print("probability: ", probs)
        return random.choices(candidates, weights=probs, k=1)[0]

    def perturb_entity(self, entity_text: str, entity_type: str, epsilon: float) -> str:
        if entity_type not in self.replacement_dict:
            return entity_text
        candidates = self.replacement_dict[entity_type]
        return self._exponential_mechanism(entity_text, candidates, epsilon)

    def perturb_text(self, text: str):
        doc = self.nlp(text)
        segments = []
        last_end = 0

        protected_ents = [ent for ent in doc.ents if ent.label_ in self.entity_types]
        if not protected_ents:
            return text

        epsilon_per_entity = self.epsilon / len(protected_ents)

        for ent in doc.ents:
            segments.append(text[last_end:ent.start_char])
            if ent.label_ in self.entity_types:
                perturbed = self.perturb_entity(ent.text, ent.label_, epsilon_per_entity)
                segments.append(perturbed)
            else:
                segments.append(ent.text)
            last_end = ent.end_char

        segments.append(text[last_end:])
        return ''.join(segments)
    
# Main entrypoint for the pipeline
def perturb(text: str, config: Dict):
    epsilon = config.get("epsilon", 1.0)
    enabled = config.get("enable", True)
    protected_types = config.get("protected_entity_types", ["PERSON", "GPE", "DATE"])

    if not enabled:
        return text

    perturber = EntityPerturber(epsilon=epsilon, protected_entity_types=protected_types)
    return perturber.perturb_text(text)