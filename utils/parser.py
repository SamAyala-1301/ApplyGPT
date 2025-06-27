import docx2txt

def load_resume(docx_path: str) -> str:
    try:
        text = docx2txt.process(docx_path)
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Error loading resume: {e}")

# Optional - only keep if you plan to load JDs from txt files
# def load_job_description(txt_path: str) -> str:
#     try:
#         with open(txt_path, 'r', encoding='utf-8') as f:
#             return f.read().strip()
#     except Exception as e:
#         raise RuntimeError(f"Error loading job description: {e}")