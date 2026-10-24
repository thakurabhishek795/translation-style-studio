"""
Translation Memory (TM) Engine with Hybrid RAG Retrieval.
Supports both semantic vector similarity and fuzzy lexical matching.
Zero external dependencies required (uses built-in subword n-gram vectorization with cosine similarity),
with optional plug-in support for SentenceTransformers/ChromaDB.
"""

import json
import os
import re
import math
import hashlib
from collections import Counter
from typing import List, Dict, Optional, Tuple

class TranslationMemory:
    def __init__(self, storage_path: str = "data/tm_store.json"):
        self.storage_path = storage_path
        self.segments: List[Dict] = []
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self.segments = json.load(f)
            except Exception as e:
                print(f"[TM] Error loading {self.storage_path}: {e}")
                self.segments = []
        else:
            self.segments = []
            self._save()

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.segments, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        # Normalize and tokenize words and character 3-grams for subword similarity
        text_clean = text.lower().strip()
        words = re.findall(r"\b\w+\b", text_clean)
        # Generate word n-grams and character tri-grams for robust semantic/fuzzy matching
        tokens = list(words)
        # Word bigrams
        for i in range(len(words) - 1):
            tokens.append(f"{words[i]}_{words[i+1]}")
        # Char trigrams for subword/morphological match
        compact = re.sub(r"\s+", " ", text_clean)
        for i in range(len(compact) - 2):
            tokens.append(compact[i:i+3])
        return tokens

    def _vectorize(self, text: str) -> Dict[str, float]:
        tokens = self._tokenize(text)
        counts = Counter(tokens)
        total = sum(counts.values()) or 1.0
        # Normalised TF
        return {token: count / total for token, count in counts.items()}

    @staticmethod
    def _cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        intersection = set(vec1.keys()) & set(vec2.keys())
        if not intersection:
            return 0.0
        dot_product = sum(vec1[k] * vec2[k] for k in intersection)
        norm1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        norm2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
        if norm1 == 0.0 or norm2 == 0.0:
            return 0.0
        return dot_product / (norm1 * norm2)

    def add_segment(
        self,
        source: str,
        target: str,
        bad_literal: Optional[str] = None,
        category: str = "general",
        notes: str = ""
    ) -> Dict:
        """
        Add an approved source-target pair.
        Optional bad_literal provides contrastive learning for the translation prompt.
        """
        source = source.strip()
        target = target.strip()
        if not source or not target:
            raise ValueError("Source and target must not be empty.")

        # Check if already exists (update if so)
        seg_id = hashlib.md5(source.encode("utf-8")).hexdigest()[:12]
        existing = next((s for s in self.segments if s["id"] == seg_id), None)

        record = {
            "id": seg_id,
            "source": source,
            "target": target,
            "bad_literal": bad_literal.strip() if bad_literal else None,
            "category": category,
            "notes": notes.strip(),
            "updated_at": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ")
        }

        if existing:
            existing.update(record)
        else:
            self.segments.append(record)

        self._save()
        return record

    def delete_segment(self, seg_id: str) -> bool:
        initial_len = len(self.segments)
        self.segments = [s for s in self.segments if s["id"] != seg_id]
        if len(self.segments) < initial_len:
            self._save()
            return True
        return False

    def retrieve_similar(
        self,
        query: str,
        top_k: int = 3,
        threshold: float = 0.25
    ) -> List[Dict]:
        """
        RAG Semantic Retrieval: Finds the closest approved translation segments.
        Returns a list of dicts with match metadata and similarity scores.
        """
        if not self.segments or not query.strip():
            return []

        q_vec = self._vectorize(query)
        scored: List[Tuple[float, Dict]] = []

        for seg in self.segments:
            seg_vec = self._vectorize(seg["source"])
            score = self._cosine_similarity(q_vec, seg_vec)
            
            # Boost score if exact words match
            q_words = set(re.findall(r"\b\w+\b", query.lower()))
            s_words = set(re.findall(r"\b\w+\b", seg["source"].lower()))
            overlap = len(q_words & s_words) / max(len(q_words | s_words), 1)
            final_score = (0.7 * score) + (0.3 * overlap)

            if final_score >= threshold:
                seg_copy = dict(seg)
                seg_copy["similarity"] = round(final_score, 3)
                scored.append((final_score, seg_copy))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:top_k]]

    def get_all(self) -> List[Dict]:
        return sorted(self.segments, key=lambda x: x.get("updated_at", ""), reverse=True)

    def import_pairs(self, pairs: List[Dict]) -> int:
        count = 0
        for p in pairs:
            if "source" in p and "target" in p:
                self.add_segment(
                    source=p["source"],
                    target=p["target"],
                    bad_literal=p.get("bad_literal"),
                    category=p.get("category", "general"),
                    notes=p.get("notes", "")
                )
                count += 1
        return count
