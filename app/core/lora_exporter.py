"""
LoRA / QLoRA Dataset Preparation & Export Engine.
Converts Translation Memory (TM) pairs and style exemplars into standard fine-tuning datasets:
- Alpaca Format (instruction, input, output)
- ShareGPT / ChatML Multi-turn Format
- Unsloth / HuggingFace TRL JSONL Format
Includes train/validation splitting and training statistics.
"""

import json
import os
import random
from typing import List, Dict, Tuple

class LoRAExporter:
    @staticmethod
    def format_alpaca(
        segments: List[Dict],
        instruction: str = "Translate the following English academic prose into formal, fluent Hindi matching the author's refined style."
    ) -> List[Dict]:
        dataset = []
        for s in segments:
            dataset.append({
                "instruction": instruction,
                "input": s["source"],
                "output": s["target"]
            })
        return dataset

    @staticmethod
    def format_sharegpt(
        segments: List[Dict],
        system_msg: str = "You are an expert translator specializing in translating English into elegant, natural Hindi prose."
    ) -> List[Dict]:
        dataset = []
        for s in segments:
            dataset.append({
                "conversations": [
                    {"from": "system", "value": system_msg},
                    {"from": "human", "value": f"Translate this text into Hindi:\n\n{s['source']}"},
                    {"from": "gpt", "value": s["target"]}
                ]
            })
        return dataset

    @staticmethod
    def format_unsloth(segments: List[Dict]) -> List[Dict]:
        # Formatted directly as conversational messages for modern HuggingFace / Unsloth trainers
        dataset = []
        for s in segments:
            dataset.append({
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a specialized translator producing high-quality, non-literal Hindi translations."
                    },
                    {
                        "role": "user",
                        "content": s["source"]
                    },
                    {
                        "role": "assistant",
                        "content": s["target"]
                    }
                ]
            })
        return dataset

    @classmethod
    def export_dataset(
        cls,
        segments: List[Dict],
        output_dir: str = "data/exports",
        format_type: str = "unsloth",
        val_split: float = 0.1,
        seed: int = 42
    ) -> Dict:
        """
        Exports segments into train.jsonl and val.jsonl in the chosen format.
        """
        if not segments:
            raise ValueError("No translation segments available to export.")

        os.makedirs(output_dir, exist_ok=True)
        items = list(segments)
        random.seed(seed)
        random.shuffle(items)

        # Split into train and validation
        val_count = max(1, int(len(items) * val_split)) if len(items) > 5 else 0
        train_items = items[val_count:]
        val_items = items[:val_count]

        # Convert to target format
        formatter = {
            "alpaca": cls.format_alpaca,
            "sharegpt": cls.format_sharegpt,
            "unsloth": cls.format_unsloth
        }.get(format_type.lower(), cls.format_unsloth)

        train_data = formatter(train_items)
        val_data = formatter(val_items)

        train_path = os.path.join(output_dir, f"lora_{format_type}_train.jsonl")
        val_path = os.path.join(output_dir, f"lora_{format_type}_val.jsonl")

        with open(train_path, "w", encoding="utf-8") as f:
            for row in train_data:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

        with open(val_path, "w", encoding="utf-8") as f:
            for row in val_data:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

        # Generate a sample Unsloth training script template
        script_path = os.path.join(output_dir, "train_lora_unsloth.py")
        cls._generate_training_script(script_path, train_path, val_path)

        total_words_en = sum(len(s["source"].split()) for s in segments)
        total_words_hi = sum(len(s["target"].split()) for s in segments)

        return {
            "format": format_type,
            "total_segments": len(segments),
            "train_count": len(train_data),
            "val_count": len(val_data),
            "train_file": train_path,
            "val_file": val_path,
            "training_script": script_path,
            "stats": {
                "total_english_words": total_words_en,
                "total_hindi_words": total_words_hi,
                "avg_en_sentence_length": round(total_words_en / max(len(segments), 1), 1),
                "estimated_tokens": int((total_words_en + total_words_hi) * 1.3)
            }
        }

    @staticmethod
    def _generate_training_script(script_path: str, train_file: str, val_file: str):
        script_code = f'''"""
Unsloth LoRA Fine-Tuning Script Template for Translation Style
Install: pip install unsloth "xformers<0.0.28" trl peft accelerate bitsandbytes
"""

from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset

max_seq_length = 2048
dtype = None # Auto detection
load_in_4bit = True # 4bit QLoRA for fast training with low VRAM

# 1. Load Base Model (e.g. Qwen2.5-7B, Llama-3.1-8B, or Gemma-2-9B)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen2.5-7B-Instruct",
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=load_in_4bit,
)

# 2. Add LoRA Adapters
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=3407,
)

# 3. Load Exported Datasets
dataset = load_dataset("json", data_files={{"train": "{os.path.basename(train_file)}", "validation": "{os.path.basename(val_file)}"}})

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"],
    dataset_text_field="messages",
    max_seq_length=max_seq_length,
    dataset_num_proc=2,
    packing=False,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        max_steps=60,
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=1,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        output_dir="lora_translation_model",
    ),
)

trainer.train()

# 4. Save Fine-Tuned Model & Adapters
model.save_pretrained_merged("translation_style_lora_merged", tokenizer, save_method="merged_16bit")
print("LoRA training complete! Model saved to translation_style_lora_merged")
'''
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_code)
