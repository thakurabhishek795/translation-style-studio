"""
Document Parser & Sentence Segmenter.
Handles PDF extraction, plain text, and intelligent sentence segmentation
(preserving abbreviations, citations, decimal numbers, and headings).
"""

import re
from typing import List

class DocumentParser:
    # Common abbreviations to prevent false sentence splits
    ABBREVIATIONS = (
        r"\b(?:e\.g|i\.e|etc|mr|mrs|ms|dr|prof|vs|al|fig|chap|vol|no|pp|p|ref|dept|univ|approx|est)\."
    )

    @classmethod
    def segment_sentences(cls, text: str) -> List[str]:
        """
        Splits a passage into clean, discrete sentence segments while preserving
        abbreviations, decimals (e.g. 3.14), citations ([Smith, 1974]), and list numbers.
        """
        if not text:
            return []

        # Normalize line breaks and tabs
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        
        # Split on paragraph breaks first
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        all_sentences = []

        for para in paragraphs:
            # Mask abbreviations with a placeholder
            def mask_abbr(m):
                return m.group(0).replace(".", "§DOT§")

            masked = re.sub(cls.ABBREVIATIONS, mask_abbr, para, flags=re.IGNORECASE)
            # Mask decimals like 12.5% or 3.14
            masked = re.sub(r"(\d+)\.(\d+)", r"\1§DOT§\2", masked)
            # Mask citations like [1.2] or [Marx, 1910]
            masked = re.sub(r"\[([^\]]+)\]", lambda m: m.group(0).replace(".", "§DOT§"), masked)

            # Split on sentence boundaries: (. ! ?) followed by whitespace and capital letter or quote
            raw_splits = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'“‘\u0900-\u097F])", masked)

            for s in raw_splits:
                # Restore masked dots
                clean_s = s.replace("§DOT§", ".").strip()
                # Clean up repeated inner spaces
                clean_s = re.sub(r"[ \t]+", " ", clean_s)
                if len(clean_s) > 5: # Filter out stray punctuation
                    all_sentences.append(clean_s)

        return all_sentences

    @classmethod
    def extract_from_pdf(cls, pdf_path: str) -> List[str]:
        """Extract text from a PDF file using pypdf or PyMuPDF if installed."""
        try:
            import fitz # PyMuPDF
            doc = fitz.open(pdf_path)
            full_text = []
            for page in doc:
                full_text.append(page.get_text())
            return cls.segment_sentences("\n".join(full_text))
        except ImportError:
            pass

        try:
            import pypdf
            reader = pypdf.PdfReader(pdf_path)
            full_text = []
            for page in reader.pages:
                full_text.append(page.extract_text() or "")
            return cls.segment_sentences("\n".join(full_text))
        except ImportError:
            raise RuntimeError("Neither PyMuPDF ('fitz') nor 'pypdf' is installed to parse PDF files.")
