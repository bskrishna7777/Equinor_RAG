
import pandas as pd
from PyPDF2 import PdfReader

def load_pdf_chunks(pdf_path, chunk_size=300):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def load_csv_context(csv_path, max_rows=20):
    df = pd.read_csv(csv_path)
    return df.head(max_rows).to_string(index=False)
