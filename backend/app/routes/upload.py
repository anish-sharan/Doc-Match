import json
import re
from typing import List
from fastapi import APIRouter, UploadFile
from app.services.ocr_service import process_image, compare_po_and_invoice

router = APIRouter()

def extract_json_from_codeblock(text: str) -> str:
    """Remove Markdown-style ```json code block wrappers."""
    match = re.search(r"```json\s*(\{.*\})\s*```", text, re.DOTALL)
    if match:
        return match.group(1)
    return text  # fallback if no code block

@router.post("/upload")
async def upload_files(files: List[UploadFile]):
    """
    Accept multiple files and process them in pairs: PO -> Invoice.
    Assumes files are uploaded in order: [po1, invoice1, po2, invoice2, ...]
    """
    results = []

    # Make sure we have an even number of files (PO + Invoice pairs)
    if len(files) % 2 != 0:
        return {"error": "Files must be uploaded in PO/Invoice pairs"}

    # Process each pair
    for i in range(0, len(files), 2):
        po_file = files[i]
        invoice_file = files[i + 1]

        po_text = await process_image(po_file)
        invoice_text = await process_image(invoice_file)

        comparison_result = await compare_po_and_invoice(po_text, invoice_text)
        cleaned_json_text = extract_json_from_codeblock(comparison_result)

        try:
            comparison_result_json = json.loads(cleaned_json_text)
        except json.JSONDecodeError:
            comparison_result_json = {"error": "Invalid JSON returned by LLM", "raw_output": comparison_result}

        results.append({
            "po_file": po_file.filename,
            "invoice_file": invoice_file.filename,
            "comparison_result": comparison_result,
            "comparison_result_json": comparison_result_json
        })

    return {"results": results}
