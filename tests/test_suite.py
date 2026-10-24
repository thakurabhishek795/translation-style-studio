import unittest
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.core.memory import TranslationMemory
from app.core.glossary import Glossary
from app.core.concept_kb import ConceptKnowledgeBase
from app.core.prompt_engine import PromptEngine
from app.core.lora_exporter import LoRAExporter
from app.core.document_parser import DocumentParser

class TestLinguaStyleStudio(unittest.TestCase):
    def setUp(self):
        self.test_tm_file = os.path.join(BASE_DIR, "data", "test_tm.json")
        self.test_gl_file = os.path.join(BASE_DIR, "data", "test_gl.json")
        self.tm = TranslationMemory(storage_path=self.test_tm_file)
        self.gl = Glossary(storage_path=self.test_gl_file)
        self.concept_kb = ConceptKnowledgeBase(storage_path=os.path.join(BASE_DIR, "data", "mia_encyclopedia.json"))

    def tearDown(self):
        if os.path.exists(self.test_tm_file):
            os.remove(self.test_tm_file)
        if os.path.exists(self.test_gl_file):
            os.remove(self.test_gl_file)

    def test_tm_add_and_retrieve(self):
        self.tm.add_segment(
            source="The capitalist price mechanism fails to reflect true costs.",
            target="पूंजीवादी मूल्य प्रणाली वास्तविक लागत दर्शाने में असफल रहती है।",
            bad_literal="पूंजीवादी कीमत तंत्र सच लागत दिखाने में असफल है।",
            category="economics"
        )
        matches = self.tm.retrieve_similar("The price mechanism under capitalism fails.", top_k=1, threshold=0.2)
        self.assertEqual(len(matches), 1)
        self.assertIn("मूल्य प्रणाली", matches[0]["target"])
        self.assertTrue(matches[0]["similarity"] > 0.2)

    def test_glossary_match(self):
        self.gl.add_entry(
            term="surplus labor",
            preferred="अधिशेष श्रम",
            avoid_terms=["बचा हुआ काम"],
            context_notes="Core Marxist concept"
        )
        text = "Under feudalism, the lord extracted surplus labor from the peasant."
        matches = self.gl.find_matching_terms(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["preferred"], "अधिशेष श्रम")

    def test_concept_kb_match(self):
        text = "The extraction of absolute surplus value requires lengthening the working day."
        matches = self.concept_kb.find_matching_concepts(text)
        self.assertTrue(len(matches) >= 1)
        term_names = [m["term"] for m in matches]
        self.assertTrue(any("Surplus Value" in t for t in term_names))

    def test_prompt_assembler(self):
        prompt = PromptEngine.build_prompt(
            source_text="Test source text",
            target_language="Hindi",
            tm_matches=[{"source": "S1", "target": "T1", "similarity": 0.85}],
            glossary_matches=[{"term": "labor", "preferred": "श्रम", "avoid_terms": ["काम"]}]
        )
        self.assertIn("Approved Translation Memory", prompt["user_prompt"])
        self.assertIn("Mandatory Terminology", prompt["user_prompt"])
        self.assertIn("Test source text", prompt["user_prompt"])

    def test_sentence_segmentation(self):
        text = "Dr. Smith stated that e.g. labor time is 12.5 hours. He was right! What about capitalism?"
        sentences = DocumentParser.segment_sentences(text)
        self.assertEqual(len(sentences), 3)
        self.assertIn("Dr. Smith stated that e.g. labor time is 12.5 hours.", sentences[0])

    def test_lora_export(self):
        segments = [
            {"source": "S1", "target": "T1"},
            {"source": "S2", "target": "T2"},
            {"source": "S3", "target": "T3"},
            {"source": "S4", "target": "T4"},
            {"source": "S5", "target": "T5"},
            {"source": "S6", "target": "T6"}
        ]
        export_res = LoRAExporter.export_dataset(
            segments=segments,
            output_dir=os.path.join(BASE_DIR, "data", "test_exports"),
            format_type="alpaca",
            val_split=0.2
        )
        self.assertEqual(export_res["format"], "alpaca")
        self.assertTrue(os.path.exists(export_res["train_file"]))
        self.assertTrue(os.path.exists(export_res["val_file"]))

if __name__ == "__main__":
    unittest.main()
