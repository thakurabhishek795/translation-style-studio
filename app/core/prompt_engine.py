"""
Dynamic Prompt Engine.
Assembles translation prompts by fusing:
1. Target style directives & negative constraints
2. Retrieved Translation Memory (TM) exemplars (including contrastive bad vs good examples)
3. Matching Context Glossary terms with 'avoid' restrictions
4. Source text segment
"""

from typing import List, Dict, Optional

class PromptEngine:
    DEFAULT_STYLE_DIRECTIVES = (
        "- Maintain natural syntactic flow in the target language; avoid calque sentence structures.\n"
        "- Prefer active voice and idiomatic cadence over awkward literal passive phrasing.\n"
        "- Strictly adhere to the approved Translation Memory examples for tone and phrasing patterns.\n"
        "- Enforce the mandatory Glossary vocabulary; never use forbidden/avoided translations.\n"
        "- Preserve all citations, equations, numerical quantities, URLs, and proper names untouched."
    )

    @classmethod
    def build_prompt(
        cls,
        source_text: str,
        target_language: str = "Hindi",
        tm_matches: Optional[List[Dict]] = None,
        glossary_matches: Optional[List[Dict]] = None,
        concept_matches: Optional[List[Dict]] = None,
        custom_style_directives: Optional[str] = None
    ) -> Dict:
        """
        Builds both a system prompt and a user prompt structured for modern LLMs.
        Fuses:
        1. Target style directives & negative constraints
        2. Retrieved Translation Memory (TM) exemplars
        3. Matching Context Glossary terms with 'avoid' restrictions
        4. Theoretical Concept Definitions (MIA Encyclopedia) for semantic grounding
        5. Source text segment
        """
        directives = custom_style_directives.strip() if custom_style_directives else cls.DEFAULT_STYLE_DIRECTIVES

        # 1. System Prompt
        system_prompt = (
            f"You are a master literary and academic translator specializing in English to {target_language}.\n"
            f"Your objective is to produce translations that sound naturally authored by a native writer in {target_language},\n"
            f"strictly matching the author's custom translation style and terminology rules rather than literal word-for-word translation.\n\n"
            f"### Core Style Directives:\n{directives}"
        )

        # 2. User Prompt Assembly
        user_parts = []

        # A. Theoretical Concept Grounding (MIA Encyclopedia)
        if concept_matches:
            user_parts.append("### Theoretical Context & Concept Definitions (MIA Encyclopedia):")
            user_parts.append("Understand the precise dialectical/Marxian meaning of these concepts before translating:")
            for c in concept_matches:
                user_parts.append(f"  • Concept: \"{c['term']}\"\n    Definition: {c['definition']}")
            user_parts.append("")

        # B. Translation Memory Section
        if tm_matches:
            user_parts.append("### Approved Translation Memory (Style & Rhythm References):")
            user_parts.append("Learn from the tone, cadence, and phrasing of these approved translations:")
            for i, match in enumerate(tm_matches, 1):
                block = f"Exemplar {i} (Match score: {match.get('similarity', 1.0)}):\n"
                block += f"  - English Source: \"{match['source']}\"\n"
                if match.get("bad_literal"):
                    block += f"  - AVOID (Literal Translation): \"{match['bad_literal']}\"\n"
                block += f"  - PREFERRED (Author Style): \"{match['target']}\""
                if match.get("notes"):
                    block += f"    [Note: {match['notes']}]"
                user_parts.append(block)
            user_parts.append("")

        # C. Context Glossary Section
        if glossary_matches:
            user_parts.append("### Mandatory Terminology & Context Guidelines:")
            for item in glossary_matches:
                g_line = f"  • Term: \"{item['term']}\" ➔ Preferred: \"{item['preferred']}\""
                if item.get("avoid_terms"):
                    avoids = ", ".join(f'"{a}"' for a in item["avoid_terms"])
                    g_line += f" | FORBIDDEN: [{avoids}]"
                if item.get("context_notes"):
                    g_line += f" | Guidance: {item['context_notes']}"
                user_parts.append(g_line)
            user_parts.append("")

        # D. Task Section
        user_parts.append(f"### Source Text to Translate into {target_language}:")
        user_parts.append(f"\"{source_text}\"\n")
        user_parts.append(f"### {target_language} Translation (Author Style):")

        user_prompt = "\n".join(user_parts)

        return {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "combined_prompt": f"{system_prompt}\n\n{'='*40}\n\n{user_prompt}"
        }
