import docx2txt

import os
import docx2txt
import fitz  # PyMuPDF

def load_resume(file_path: str, file_ext: str) -> str:
    try:
        if file_ext == ".docx":
            return docx2txt.process(file_path).strip()
        elif file_ext == ".pdf":
            text = ""
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()
            return text.strip()
        elif file_ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        else:
            raise ValueError("Unsupported file format.")
    except Exception as e:
        raise RuntimeError(f"Failed to load resume: {e}")

# Optional - only keep if you plan to load JDs from txt files
# def load_job_description(txt_path: str) -> str:
#     try:
#         with open(txt_path, 'r', encoding='utf-8') as f:
#             return f.read().strip()
#     except Exception as e:
#         raise RuntimeError(f"Error loading job description: {e}")