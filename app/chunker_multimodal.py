import os
import fitz  # PyMuPDF
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import tempfile

# Load BLIP model for image captioning
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

def extract_text_and_images(pdf_path, chunk_size=300):
    doc = fitz.open(pdf_path)
    text_chunks = []
    image_chunks = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        # Chunk text
        for i in range(0, len(text), chunk_size):
            chunk = {
                "chunk_type": "text",
                "content": text[i:i+chunk_size],
                "source_page": page_num + 1
            }
            text_chunks.append(chunk)

        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
                tmp_img.write(image_bytes)
                tmp_img.flush()
                image = Image.open(tmp_img.name).convert("RGB")
                inputs = processor(image, return_tensors="pt").to(device)
                out = model.generate(**inputs)
                caption = processor.decode(out[0], skip_special_tokens=True)

                image_chunks.append({
                    "chunk_type": "figure",
                    "content": caption,
                    "source_page": page_num + 1
                })

            os.unlink(tmp_img.name)

    return text_chunks + image_chunks