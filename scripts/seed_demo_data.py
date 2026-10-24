"""
Seed demo Translation Memory (TM) pairs and Context Glossary entries
derived from the 'How the World Works' and 'Imperialism' book translation project.
"""

def seed_data(tm, glossary):
    # 1. Aligned Translation Memory Pairs (Contrastive: Source, Target, Bad Literal)
    tm_pairs = [
        {
            "source": "The capitalist price mechanism fails to reflect the true social labor costs.",
            "target": "पूंजीवादी मूल्य प्रणाली वास्तविक सामाजिक श्रम-लागत को दर्शाने में असमर्थ रहती है।",
            "bad_literal": "पूंजीवादी कीमत तंत्र सच सामाजिक काम लागत दिखाने में असफल है।",
            "category": "economics",
            "notes": "Use 'मूल्य प्रणाली' for 'price mechanism' and active voice."
        },
        {
            "source": "Surplus value is extracted from the working class through uncompensated labor time.",
            "target": "अवैतनिक श्रम-समय के जरिए मजदूर वर्ग से अधिशेष मूल्य का दोहन किया जाता है।",
            "bad_literal": "अधिशेष मूल्य बिना मुआवजा काम समय के माध्यम से कामगार वर्ग से निकाला जाता है।",
            "category": "economics",
            "notes": "Always use 'अधिशेष मूल्य' and 'अवैतनिक श्रम-समय'."
        },
        {
            "source": "A transition to renewable energy requires a planned reallocation of labor resources.",
            "target": "नवीकरणीय ऊर्जा की ओर बदलाव के लिए श्रम संसाधनों का सुनियोजित पुनर्वितरण आवश्यक है।",
            "bad_literal": "अक्षय ऊर्जा में संक्रमण के लिए श्रम संसाधनों के एक नियोजित पुनः आवंटन की आवश्यकता होती है।",
            "category": "energy",
            "notes": "Use 'नवीकरणीय ऊर्जा' and 'सुनियोजित पुनर्वितरण'."
        },
        {
            "source": "The development of productive forces inevitably comes into conflict with existing relations of production.",
            "target": "जैसे-जैसे उत्पादन क्षमताएं विकसित होती हैं, उनका मौजूदा सामाजिक व आर्थिक व्यवस्था से टकराव होना तय है।",
            "bad_literal": "उत्पादक शक्तियों का विकास अनिवार्य रूप से उत्पादन के मौजूदा संबंधों के साथ संघर्ष में आता है।",
            "category": "philosophy",
            "notes": "Avoid calque English phrasing; use fluid natural Hindi cadence."
        },
        {
            "source": "The planning committee decided to use cybernetic feedback algorithms for material balances.",
            "target": "योजना समिति ने भौतिक संतुलन साधने के लिए साइबरनेटिक फीडबैक एल्गोरिदम का इस्तेमाल करने का फैसला किया।",
            "bad_literal": "योजना समिति द्वारा सामग्री संतुलन के लिए साइबरनेटिक फीडबैक एल्गोरिदम का उपयोग करने का निर्णय लिया गया था।",
            "category": "cybernetics",
            "notes": "Transliterate cybernetic feedback algorithms in Devanagari; avoid passive voice."
        },
        {
            "source": "The rate of exploitation can be mathematically represented as the ratio of surplus labor to necessary labor.",
            "target": "शोषण की दर को गणितीय रूप से अधिशेष श्रम और आवश्यक श्रम के अनुपात के रूप में दर्शाया जा सकता है।",
            "bad_literal": "शोषण की दर अधिशेष श्रम से आवश्यक श्रम का अनुपात है।",
            "category": "mathematics",
            "notes": "Preserve mathematical terms accurately."
        }
    ]

    for p in tm_pairs:
        tm.add_segment(
            source=p["source"],
            target=p["target"],
            bad_literal=p.get("bad_literal"),
            category=p.get("category", "general"),
            notes=p.get("notes", "")
        )

    # 2. Context Glossary Terms
    glossary_terms = [
        {
            "term": "mode of production",
            "preferred": "उत्पादन की प्रणाली (mode of production)",
            "avoid_terms": ["उत्पादन का तरीका", "बनाने की विधि"],
            "context_notes": "Standard Marxist concept; preserve transliteration or formal term."
        },
        {
            "term": "surplus labor",
            "preferred": "अधिशेष श्रम",
            "avoid_terms": ["बचा हुआ काम", "अतिरिक्त मेहनत", "फाालतू काम"],
            "context_notes": "Essential political economy term; do not use casual words."
        },
        {
            "term": "commodity",
            "preferred": "कमोडिटी",
            "avoid_terms": ["वस्तु", "चीज़"],
            "context_notes": "Keep transliterated when referring to goods produced specifically for exchange."
        },
        {
            "term": "feedback",
            "preferred": "फीडबैक",
            "avoid_terms": ["प्रतिक्रिया"],
            "context_notes": "In cybernetic and systems engineering contexts, transliterate as फीडबैक."
        },
        {
            "term": "algorithm",
            "preferred": "एल्गोरिदम",
            "avoid_terms": ["कलन विधि"],
            "context_notes": "Use modern transliterated Devanagari for computing terms."
        },
        {
            "term": "proletariat",
            "preferred": "सर्वहारा वर्ग",
            "avoid_terms": ["गरीब लोग", "मजदूर लोग"],
            "context_notes": "Formal sociological/political term."
        }
    ]

    for g in glossary_terms:
        glossary.add_entry(
            term=g["term"],
            preferred=g["preferred"],
            avoid_terms=g.get("avoid_terms", []),
            context_notes=g.get("context_notes", ""),
            category="economics"
        )

    print(f"Seeded {len(tm_pairs)} TM pairs and {len(glossary_terms)} glossary terms.")

if __name__ == "__main__":
    import os, sys
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)
    from app.core.memory import TranslationMemory
    from app.core.glossary import Glossary
    tm = TranslationMemory(storage_path=os.path.join(BASE_DIR, "data", "tm_store.json"))
    glossary = Glossary(storage_path=os.path.join(BASE_DIR, "data", "glossary.json"))
    seed_data(tm, glossary)
