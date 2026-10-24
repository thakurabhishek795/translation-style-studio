"""
MIA Concept Knowledge Base.
Provides theoretical definitions and historical context for 688 Marxist,
Hegelian, and philosophical terms from the Marxists Internet Archive (MIA) Encyclopedia.
Grounded context prevents LLMs from translating philosophical terms as colloquial words.
"""

import json
import os
import re
from typing import List, Dict, Optional

class ConceptKnowledgeBase:
    def __init__(self, storage_path: str = "data/mia_encyclopedia.json"):
        self.storage_path = storage_path
        self.concepts: List[Dict] = []
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self.concepts = json.load(f)
            except Exception as e:
                print(f"[ConceptKB] Error loading {self.storage_path}: {e}")
                self.concepts = []
        else:
            self.concepts = []

    def find_matching_concepts(self, text: str, max_matches: int = 3) -> List[Dict]:
        """
        Scans input text for occurrences of the 688 MIA encyclopedia concepts.
        Matches longer multi-word concepts first to avoid partial conflicts.
        """
        if not text or not self.concepts:
            return []

        # Sort concepts by term length descending
        sorted_concepts = sorted(self.concepts, key=lambda x: len(x.get("term", "")), reverse=True)
        matches = []
        seen_terms = set()

        for c in sorted_concepts:
            term = c.get("term", "").strip()
            if not term or len(term) < 4:
                continue

            # Strip parenthetical annotations for flexible matching, e.g. "Abstract (Althusser)" -> "Abstract"
            clean_term = re.sub(r"\(.*?\)", "", term).strip()
            if not clean_term:
                clean_term = term

            pattern = r"\b" + re.escape(clean_term) + r"\b"
            if re.search(pattern, text, re.IGNORECASE):
                # Clean up definition snippet (first 250 chars)
                def_text = c.get("definition_text", "").strip()
                short_def = (def_text[:280] + "...") if len(def_text) > 280 else def_text

                if clean_term.lower() not in seen_terms:
                    seen_terms.add(clean_term.lower())
                    matches.append({
                        "term": term,
                        "matched_text": clean_term,
                        "definition": short_def,
                        "full_definition": def_text,
                        "source_url": c.get("source_url", "")
                    })

                if len(matches) >= max_matches:
                    break

        return matches

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Search concepts by query string in term name or definition."""
        q = query.lower().strip()
        results = []
        for c in self.concepts:
            term = c.get("term", "")
            def_text = c.get("definition_text", "")
            if q in term.lower() or q in def_text.lower():
                results.append({
                    "term": term,
                    "definition": def_text[:300] + ("..." if len(def_text) > 300 else ""),
                    "source_url": c.get("source_url", "")
                })
                if len(results) >= limit:
                    break
        return results
