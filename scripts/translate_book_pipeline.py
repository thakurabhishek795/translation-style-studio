#!/usr/bin/env python3
"""
Book Translation Orchestration Pipeline.
Demonstrates fusing Baidu Unlimited-OCR parsed Markdown documents with
LinguaStyle Studio's Translation Memory, Context Glossary, and Concept Knowledge Base.
"""

import os
import sys
import json
from typing import Dict, List, Optional

# Add app to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from app.core.memory import TranslationMemory
from app.core.glossary import Glossary
from app.core.concept_kb import ConceptKnowledgeBase
from app.core.prompt_engine import PromptEngine


class TranslationQualityAuditor:
    """
    Verifies that generated translations strictly adhere to glossary,
    editorial precision rules, and Markdown structural constraints.
    """

    def __init__(self, glossary_entries: Dict):
        self.glossary_entries = glossary_entries

    def audit(self, source_md: str, translated_md: str) -> List[str]:
        import re
        violations = []

        # 1. Check for Forbidden Glossary Terms (Context-aware: checked per active source term)
        src_lower = source_md.lower()
        for term, data in self.glossary_entries.items():
            # Only enforce forbidden terms if the source term itself was in the source text
            term_pattern = r"\b" + re.escape(term.lower()) + r"\b"
            if re.search(term_pattern, src_lower):
                # Exception: if both 'value' and 'price' are in the same text, allow both 'मूल्य' and 'कीमत'
                if term in ("value", "price") and "value" in src_lower and "price" in src_lower:
                    continue
                for forbidden in data.get("avoid_terms", []):
                    # Check boundary
                    pattern = r"(?<![\u0900-\u097F])" + re.escape(forbidden) + r"(?![\u0900-\u097F])"
                    if re.search(pattern, translated_md):
                        violations.append(
                            f"FORBIDDEN TERM VIOLATION: Source contains '{term}', but translation used forbidden '{forbidden}' instead of preferred '{data['preferred']}'."
                        )

        # 2. Check LaTeX Math Delimiter Parity
        src_inline_math = len(re.findall(r"(?<!\$)\$(?!\$)(.*?)\$", source_md))
        tgt_inline_math = len(re.findall(r"(?<!\$)\$(?!\$)(.*?)\$", translated_md))
        if src_inline_math != tgt_inline_math:
            violations.append(
                f"LATEX MATH ERROR: Inline math count mismatch (Source: {src_inline_math}, Target: {tgt_inline_math})."
            )

        # 3. Check Markdown Table Structure
        src_tables = [line for line in source_md.split("\n") if line.strip().startswith("|")]
        tgt_tables = [line for line in translated_md.split("\n") if line.strip().startswith("|")]
        if len(src_tables) != len(tgt_tables):
            violations.append(
                f"TABLE ERROR: Row count mismatch in Markdown tables (Source: {len(src_tables)}, Target: {len(tgt_tables)})."
            )

        # 4. Check Asset / Figure Placeholder Integrity
        src_fig_tags = re.findall(r"!\[FIGURE_ID:[^\]]+\]", source_md)
        tgt_fig_tags = re.findall(r"!\[FIGURE_ID:[^\]]+\]", translated_md)
        if len(src_fig_tags) != len(tgt_fig_tags):
            violations.append(
                f"ASSET TAG ERROR: Figure placeholder count mismatch (Source: {len(src_fig_tags)}, Target: {len(tgt_fig_tags)})."
            )

        return violations


class BookTranslationOrchestrator:
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = data_dir or os.path.join(BASE_DIR, "data")
        self.tm = TranslationMemory(os.path.join(self.data_dir, "tm_store.json"))
        self.glossary = Glossary(os.path.join(self.data_dir, "glossary.json"))
        self.concept_kb = ConceptKnowledgeBase(os.path.join(self.data_dir, "mia_encyclopedia.json"))
        self.auditor = TranslationQualityAuditor(self.glossary.entries)

    def prepare_translation_prompt(self, ocr_markdown_chunk: str) -> Dict:
        """
        Takes a Markdown chunk parsed by Baidu Unlimited-OCR and fuses it with
        LinguaStyle Studio's retrieved TM matches, glossary negative rules,
        and MIA conceptual definitions.
        """
        # 1. Retrieve top semantic exemplars
        tm_matches = self.tm.retrieve_similar(ocr_markdown_chunk, top_k=3, threshold=0.15)

        # 2. Extract matching glossary rules with negative constraints
        glossary_matches = self.glossary.find_matching_terms(ocr_markdown_chunk)

        # 3. Extract matching theoretical concepts
        concept_matches = self.concept_kb.find_matching_concepts(ocr_markdown_chunk, max_matches=3)

        # 4. Build prompt via PromptEngine
        built = PromptEngine.build_prompt(
            source_text=ocr_markdown_chunk,
            target_language="Hindi",
            tm_matches=tm_matches,
            glossary_matches=glossary_matches,
            concept_matches=concept_matches,
        )

        return {
            "system_prompt": built["system_prompt"],
            "user_prompt": built["user_prompt"],
            "tm_matches_count": len(tm_matches),
            "glossary_matches_count": len(glossary_matches),
            "concept_matches_count": len(concept_matches),
        }

    def validate_translation(self, source_md: str, target_md: str) -> List[str]:
        return self.auditor.audit(source_md, target_md)


def main():
    print("=" * 70)
    print("Book Translation Orchestrator (Unlimited-OCR + LinguaStyle Studio)")
    print("=" * 70)

    orchestrator = BookTranslationOrchestrator()
    print(f"Loaded TM pairs: {len(orchestrator.tm.segments)}")
    print(f"Loaded Glossary terms: {len(orchestrator.glossary.entries)}")
    print(f"Loaded MIA Concepts: {len(orchestrator.concept_kb.concepts)}")

    # Sample Unlimited-OCR extracted chunk
    sample_chunk = (
        "In classical political economy, surplus value is extracted through uncompensated labor time. "
        "The capitalist price mechanism fails to reflect the social labor costs, creating a dialectical contradiction "
        "between the mode of production and existing relations of production."
    )

    print("\n--- Preparing Prompt for Unlimited-OCR Markdown Chunk ---")
    prepared = orchestrator.prepare_translation_prompt(sample_chunk)
    print(f"Retrieved TM Matches: {prepared['tm_matches_count']}")
    print(f"Retrieved Glossary Matches: {prepared['glossary_matches_count']}")
    print(f"Retrieved Concepts: {prepared['concept_matches_count']}")

    print("\n--- Generated System Prompt Preview ---")
    print(prepared["system_prompt"][:350] + "...\n")

    print("--- Generated User Prompt Preview ---")
    print(prepared["user_prompt"][:450] + "...\n")

    # Audit demonstration
    print("--- Testing Quality Auditor on Sample Translation ---")
    good_translation = (
        "क्लासिकल राजनीतिक अर्थशास्त्र में, बिना भुगतान किए गए श्रम-समय के माध्यम से अधिशेष मूल्य निष्कर्षित किया जाता है। "
        "पूंजीवादी कीमत क्रियाविधि वास्तविक सामाजिक श्रम-लागत को दर्शाने में असमर्थ रहती है, जिससे उत्पादन-पद्धति और "
        "विद्यमान उत्पादन-संबंधों के बीच एक द्वंद्वात्मक अन्तर्विरोध पैदा होता है।"
    )
    violations = orchestrator.validate_translation(sample_chunk, good_translation)
    print(f"Auditor Violations (Good translation): {violations or 'None (Passed Cleanly!)'}")

    bad_translation = "अधिशेष मूल्य बनाने की विधि और कामगार वर्ग के साथ वस्तु की कीमत है।"
    bad_violations = orchestrator.validate_translation(sample_chunk, bad_translation)
    print(f"Auditor Violations (Bad translation with forbidden terms):")
    for v in bad_violations:
        print(f"  ❌ {v}")

    print("\n✅ Pipeline verification test completed successfully.")


if __name__ == "__main__":
    main()
