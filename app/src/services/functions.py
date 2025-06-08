# External imports
import pdfplumber
import tiktoken as tk

def count_tokens(text: str, model: str):
    try:
        enc = tk.encoding_for_model(model)
        return len(enc.encode(text))
    except Exception as e:
        raise ValueError(f"Error counting tokens: {e}")

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts and returns all text from a PDF file using pdfplumber."""
    full_text = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text:
                    full_text.append(f"--- Page {page_number} ---\n{text}")
                else:
                    full_text.append(f"--- Page {page_number} ---\n[No extractable text]")

        return "\n\n".join(full_text)

    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {e}")