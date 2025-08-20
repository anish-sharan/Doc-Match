def compare_documents(po_tokens, invoice_tokens):
    # Simple exact match
    if po_tokens == invoice_tokens:
        return "MATCH"
    else:
        return "MISMATCH"
