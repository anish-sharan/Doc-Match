from pdf2image import convert_from_bytes
import pytesseract
from .llm_compare_service import compare_po_invoice_with_llm

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

async def process_image(file):
    contents = await file.read()
    images = convert_from_bytes(contents)

    # Extract text from all pages
    full_text = ""
    for img in images:
        full_text += extract_text_from_image(img) + "\n"

    return full_text

async def compare_po_and_invoice(po_text, invoice_text):
    # Use LLM for comparison
    result = await compare_po_invoice_with_llm(po_text, invoice_text)
    return result
