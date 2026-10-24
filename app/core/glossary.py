"""
Advanced Terminology & Context Glossary Engine.
Manages domain-specific vocabulary, preferred translations, forbidden terms, and usage guidelines.
Automatically identifies and extracts matching terms from source texts.
"""

import json
import os
import re
from typing import List, Dict, Optional

class Glossary:
    def __init__(self, storage_path: str = "data/glossary.json"):
        self.storage_path = storage_path
        self.entries: Dict[str, Dict] = {}
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self.entries = json.load(f)
            except Exception as e:
                print(f"[Glossary] Error loading {self.storage_path}: e")
                self.entries = {}
        else:
            self.entries = {}
            self._save()

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=2)

    def add_entry(
        self,
        term: str,
        preferred: str,
        avoid_terms: Optional[List[str]] = None,
        context_notes: str = "",
        category: str = "general",
        case_sensitive: bool = False
    ) -> Dict:
        term_clean = term.strip()
        if not term_clean or not preferred.strip():
            raise ValueError("Term and preferred translation are required.")

        key = term_clean if case_sensitive else term_clean.lower()
        entry = {
            "term": term_clean,
            "preferred": preferred.strip(),
            "avoid_terms": [a.strip() for a in (avoid_terms or []) if a.strip()],
            "context_notes": context_notes.strip(),
            "category": category.strip(),
            "case_sensitive": case_sensitive,
            "updated_at": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        self.entries[key] = entry
        self._save()
        return entry

    def delete_entry(self, term: str) -> bool:
        term_clean = term.strip()
        keys_to_delete = [k for k, v in self.entries.items() if v["term"].lower() == term_clean.lower()]
        if keys_to_delete:
            for k in keys_to_delete:
                del self.entries[k]
            self._save()
            return True
        return False

    def find_matching_terms(self, text: str) -> List[Dict]:
        """
        Scans input text and returns all glossary entries that appear in it.
        Longer multi-word phrases match first before single words.
        """
        if not text:
            return []

        matches = []
        # Sort terms by length descending to match multi-word phrases first
        sorted_entries = sorted(
            self.entries.values(),
            key=lambda x: len(x["term"]),
            reverse=True
        )

        for entry in sorted_entries:
            flags = 0 if entry.get("case_sensitive") else re.IGNORECASE
            pattern = r"\b" + re.escape(entry["term"]) + r"\b"
            if re.search(pattern, text, flags):
                matches.append(entry)

        return matches

    def get_all(self) -> List[Dict]:
        return sorted(self.entries.values(), key=lambda x: x["term"].lower())

    def import_entries(self, entries_list: List[Dict]) -> int:
        count = 0
        for item in entries_list:
            if "term" in item and "preferred" in item:
                self.add_entry(
                    term=item["term"],
                    preferred=item["preferred"],
                    avoid_terms=item.get("avoid_terms", []),
                    context_notes=item.get("context_notes", ""),
                    category=item.get("category", "general")
                )
                count += 1
        return count
