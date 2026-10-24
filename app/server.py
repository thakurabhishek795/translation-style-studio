"""
Lightweight REST API & Static Server for Translation Style Studio.
Built on Python's native standard library (http.server) for maximum zero-dependency portability.
"""

import os
import json
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.core.memory import TranslationMemory
from app.core.glossary import Glossary
from app.core.concept_kb import ConceptKnowledgeBase
from app.core.prompt_engine import PromptEngine
from app.core.lora_exporter import LoRAExporter
from app.core.document_parser import DocumentParser
from app.core.translator import TranslatorClient

# Initialize singletons
DATA_DIR = os.path.join(BASE_DIR, "data")
tm = TranslationMemory(storage_path=os.path.join(DATA_DIR, "tm_store.json"))
glossary = Glossary(storage_path=os.path.join(DATA_DIR, "glossary.json"))
concept_kb = ConceptKnowledgeBase(storage_path=os.path.join(DATA_DIR, "mia_encyclopedia.json"))
translator = TranslatorClient()

WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")

class StudioRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length == 0:
                return {}
            raw = self.rfile.read(length).decode("utf-8")
            return json.loads(raw)
        except Exception as e:
            print(f"[Server] Failed to parse JSON: {e}")
            return {}

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # API Endpoints
        if path == "/api/status":
            return self._send_json({
                "status": "online",
                "tm_segments_count": len(tm.get_all()),
                "glossary_terms_count": len(glossary.get_all()),
                "mia_concepts_count": len(concept_kb.concepts),
                "llm_provider": translator.provider
            })

        if path == "/api/concepts":
            q = query.get("q", [""])[0]
            limit = int(query.get("limit", [10])[0])
            results = concept_kb.search(q, limit=limit) if q else concept_kb.concepts[:limit]
            return self._send_json(results)

        if path == "/api/tm":
            q = query.get("q", [""])[0]
            items = tm.get_all()
            if q:
                items = [item for item in items if q.lower() in item["source"].lower() or q.lower() in item["target"].lower()]
            return self._send_json(items)

        if path == "/api/glossary":
            return self._send_json(glossary.get_all())

        # Static file fallback
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self._read_json_body()

        # 1. Translation Memory Add/Edit
        if path == "/api/tm":
            source = body.get("source", "")
            target = body.get("target", "")
            if not source or not target:
                return self._send_json({"error": "source and target required"}, 400)
            record = tm.add_segment(
                source=source,
                target=target,
                bad_literal=body.get("bad_literal"),
                category=body.get("category", "general"),
                notes=body.get("notes", "")
            )
            return self._send_json({"success": True, "record": record})

        # 2. TM Query (RAG search)
        if path == "/api/tm/query":
            q = body.get("query", "")
            top_k = int(body.get("top_k", 3))
            threshold = float(body.get("threshold", 0.20))
            matches = tm.retrieve_similar(q, top_k=top_k, threshold=threshold)
            return self._send_json({"query": q, "matches": matches})

        # 3. Glossary Add/Edit
        if path == "/api/glossary":
            term = body.get("term", "")
            preferred = body.get("preferred", "")
            if not term or not preferred:
                return self._send_json({"error": "term and preferred required"}, 400)
            entry = glossary.add_entry(
                term=term,
                preferred=preferred,
                avoid_terms=body.get("avoid_terms", []),
                context_notes=body.get("context_notes", ""),
                category=body.get("category", "general")
            )
            return self._send_json({"success": True, "entry": entry})

        # 4. Translation Studio / Preview
        if path == "/api/translate/preview":
            source_text = body.get("source_text", "").strip()
            target_lang = body.get("target_language", "Hindi")
            top_k = int(body.get("top_k", 3))
            threshold = float(body.get("threshold", 0.20))
            custom_directives = body.get("custom_directives")

            # A. RAG retrieval from Translation Memory
            tm_matches = tm.retrieve_similar(source_text, top_k=top_k, threshold=threshold)
            # B. Glossary matching
            glossary_matches = glossary.find_matching_terms(source_text)
            # C. MIA Theoretical Concepts matching
            concept_matches = concept_kb.find_matching_concepts(source_text)

            # D. Prompt assembly
            assembled = PromptEngine.build_prompt(
                source_text=source_text,
                target_language=target_lang,
                tm_matches=tm_matches,
                glossary_matches=glossary_matches,
                concept_matches=concept_matches,
                custom_style_directives=custom_directives
            )
            # E. Execute translation (Ollama, OpenAI, or smart preview)
            result = translator.translate(
                system_prompt=assembled["system_prompt"],
                user_prompt=assembled["user_prompt"]
            )

            return self._send_json({
                "source_text": source_text,
                "tm_matches": tm_matches,
                "glossary_matches": glossary_matches,
                "concept_matches": concept_matches,
                "assembled_prompt": assembled,
                "translation_result": result
            })

        # 5. Sentence Segmenter for Documents/PDFs
        if path == "/api/document/segment":
            text = body.get("text", "")
            sentences = DocumentParser.segment_sentences(text)
            return self._send_json({"count": len(sentences), "sentences": sentences})

        # 6. LoRA / QLoRA Dataset Export
        if path == "/api/export/lora":
            fmt = body.get("format", "unsloth")
            val_split = float(body.get("val_split", 0.1))
            segments = tm.get_all()
            if not segments:
                return self._send_json({"error": "No translation memory segments to export"}, 400)
            export_summary = LoRAExporter.export_dataset(
                segments=segments,
                output_dir=os.path.join(DATA_DIR, "exports"),
                format_type=fmt,
                val_split=val_split
            )
            return self._send_json({"success": True, "export": export_summary})

        # 7. Seed Demo Data
        if path == "/api/seed":
            from scripts.seed_demo_data import seed_data
            seed_data(tm, glossary)
            return self._send_json({
                "success": True,
                "tm_count": len(tm.get_all()),
                "glossary_count": len(glossary.get_all())
            })

        return self._send_json({"error": "Not found"}, 404)

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/api/tm":
            seg_id = query.get("id", [""])[0]
            if tm.delete_segment(seg_id):
                return self._send_json({"success": True})
            return self._send_json({"error": "Not found"}, 404)

        if path == "/api/glossary":
            term = query.get("term", [""])[0]
            if glossary.delete_entry(term):
                return self._send_json({"success": True})
            return self._send_json({"error": "Not found"}, 404)

        return self._send_json({"error": "Not found"}, 404)

def run_server(port=8080):
    server = HTTPServer(("127.0.0.1", port), StudioRequestHandler)
    print(f"\n========================================================")
    print(f"🚀 Translation Style Studio running at: http://127.0.0.1:{port}")
    print(f"========================================================\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)
