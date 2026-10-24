# LinguaStyle Studio 🌐
### Interactive Translation Memory (TM) via RAG, Context Glossary & LoRA Fine-Tuning Studio

**LinguaStyle Studio** is a translation environment designed to capture, enforce, and train your **personal translation style, voice, and domain vocabulary**—eliminating rigid, word-for-word machine translation.

---

## 🌟 Key Features

### 1. Translation Memory (TM) via Semantic RAG
- **Dynamic Style Matching**: Traditional CAT tools only match exact sentences. LinguaStyle Studio uses subword vector similarity and fuzzy n-gram matching to find semantically similar sentences you translated in the past.
- **Contrastive Exemplars**: Store not only the approved translation, but also the *bad literal translation* you want the model to avoid. These are injected side-by-side into the prompt as few-shot guides.
- **Zero-Dependency Native Vector Engine**: Runs out of the box with zero external dependencies (pure Python standard library), with plug-and-play support for SentenceTransformers and ChromaDB.

### 2. Advanced Terminology & Context Glossary
- **Context-Aware Rules**: Define usage constraints (e.g. *"Use only in political economy chapters; keep transliterated in computing contexts"*).
- **Negative Constraints**: Register forbidden / literal alternatives (e.g., for `surplus labor`, mandate `अधिशेष श्रम` and forbid `बचा हुआ काम`).
- **Automatic Entity Detection**: The engine scans every input sentence and automatically surfaces matching glossary rules.

### 3. Document & PDF Ingestion Pipeline
- Ingest dense book chapters, PDFs, or articles.
- Intelligently segments text into clean sentences while preserving abbreviations (e.g., `Dr.`, `e.g.`, `U.S.S.R.`), citations (`[Smith, 1776]`), and decimal formulas.

### 4. LoRA / QLoRA Dataset Exporter (For Fine-Tuning)
- Export approved translation memory pairs into standard fine-tuning formats with one click:
  - **Unsloth / HuggingFace TRL** (ChatML conversational JSONL)
  - **Alpaca Format** (`instruction`, `input`, `output`)
  - **ShareGPT Format**
- Automatic train/validation split (configurable, e.g., 90% train / 10% val).
- Includes an auto-generated, ready-to-run **Unsloth QLoRA training script** (`train_lora_unsloth.py`) for fine-tuning open-weights models such as **Qwen 2.5 7B/14B**, **Llama 3.3 70B**, or **Gemma 2 9B**.

---

## 💡 What Input Is Needed From You? (PDF vs. Small Sentences)

You can provide **both**, and each serves a complementary purpose:

| Input Type | Best For | How LinguaStyle Studio Uses It |
|---|---|---|
| **Small Sentences / Contrastive Pairs** *(5 – 20 pairs)* | **Immediate Style Calibration** | Feed these into the **Translation Memory** tab. Include the *bad literal translation* vs. your *preferred wording*. The RAG engine instantly mirrors your cadence, voice, and non-literal sentence structure. |
| **Full PDF / Book Chapter** *(1 – 100+ pages)* | **Vocabulary Scaling & Document Flow** | Paste text or upload a chapter in the **Document Ingestion** tab. The app breaks it down into discrete sentences so you can rapidly review, translate, and grow your translation corpus. |
| **Glossary Terms** *(Keywords)* | **Domain Accuracy** | Add key terms in the **Context Glossary** tab with preferred translations, forbidden terms, and context notes. |

---

## 🚀 Quick Start

### 1. Run the Studio (Zero Dependencies)
LinguaStyle Studio uses a self-contained Python architecture. You do not need to install heavy database drivers or complex npm packages:

```bash
# Clone the repository
git clone https://github.com/thakurabhishek795/translation-style-studio.git
cd translation-style-studio

# Start the studio
python3 run.py
```
Open your browser at **`http://127.0.0.1:8080`**.

### 2. Preload Demo Data
Click the **"⚡ Load Demo Data"** button in the top right to pre-populate:
- 6 Contrastive translation memory pairs in political economy and philosophy.
- 6 Advanced glossary entries (e.g., *mode of production*, *surplus labor*, *feedback*, *commodity*).

### 3. Translate with RAG
Go to the **Translation Studio** tab:
1. Enter an English sentence (e.g. *"The capitalist price mechanism fails to reflect social costs."*).
2. Click **"Translate with Your Style & RAG"**.
3. Inspect the **RAG Memory Inspector** to see which past translations and glossary rules were dynamically retrieved.
4. Edit the translation to your liking and click **"✅ Approve & Add to Translation Memory"**.

---

## 🛠️ Architecture & Project Structure

```
translation-style-studio/
├── app/
│   ├── server.py              # Lightweight REST API server
│   ├── core/
│   │   ├── memory.py          # Semantic RAG Translation Memory engine
│   │   ├── glossary.py        # Context glossary with auto-detection
│   │   ├── prompt_engine.py   # Dynamic prompt assembler
│   │   ├── lora_exporter.py   # Alpaca / ShareGPT / Unsloth dataset exporter
│   │   ├── document_parser.py # Intelligent sentence segmentation
│   │   └── translator.py      # LLM provider interface (Ollama, OpenAI, Mock)
│   └── web/
│       ├── index.html         # Responsive dashboard UI
│       ├── app.js             # Interactive client logic
│       └── style.css          # Modern dark-mode styling
├── data/
│   ├── tm_store.json          # Persistent Translation Memory pairs
│   ├── glossary.json          # Persistent glossary entries
│   └── exports/               # Exported LoRA JSONL datasets & scripts
├── scripts/
│   ├── start.sh               # Quick startup shell script
│   └── seed_demo_data.py      # Demo seed script
├── tests/
│   └── test_suite.py          # Comprehensive unit test suite
├── run.py                     # Root execution script
├── requirements.txt           # Optional dependencies
└── LICENSE                    # MIT License
```

---

## 🧪 Running Tests

To verify that the RAG retrieval, glossary matching, sentence segmenter, and LoRA export pass all checks:

```bash
python3 tests/test_suite.py
```

---

## 🔮 Roadmap: Fine-Tuning Open-Weights Models (LoRA / QLoRA)

Once your Translation Memory reaches **50–200+ approved sentence pairs**:
1. Navigate to the **LoRA / Fine-Tuning Exporter** tab.
2. Select your desired format (`Unsloth`, `Alpaca`, or `ShareGPT`).
3. Click **"Generate Fine-Tuning Datasets"**.
4. The studio outputs `lora_unsloth_train.jsonl`, `lora_unsloth_val.jsonl`, and an automated `train_lora_unsloth.py` script to run on Google Colab or any GPU machine.

---

## 📄 License
MIT License © 2026 Abhishek Thakur.
