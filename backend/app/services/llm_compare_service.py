import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def compare_po_invoice_with_llm(po_text: str, invoice_text: str):
    prompt = f"""
    You are an expert financial auditor.
    Compare the following PO and Invoice:

    PO:
    {po_text}

    Invoice:
    {invoice_text}

    Return a JSON with:
    - status: "match" or "mismatch"
    - details: which fields/items match and which mismatch
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    # Extract content
    content = response.choices[0].message.content
    return content

def format_comparison_result(result_json):
    data = result_json.get("details", {})
    lines = []

    # Overall status
    status = result_json.get("status", "mismatch").capitalize()
    lines.append(f"Overall Status: {'✅ Match' if status=='Match' else '❌ Mismatch'}\n")

    # PO Number, Date, Supplier
    for field in ["PO_Number", "Date", "Supplier"]:
        po_val = data.get(field, {}).get("PO", "N/A")
        inv_val = data.get(field, {}).get("Invoice", "N/A")
        match = data.get(field, {}).get("match", False)
        lines.append(f"{field.replace('_', ' ')}: {po_val} {'✅ matches' if match else '❌ does not match'} Invoice {inv_val}")

    lines.append("\nItems:")
    items = data.get("Items", {}).get("match", [])
    for item in items:
        lines.append(f"- {item['Item']}")
        lines.append(f"  Quantity: {item['Quantity']['PO']} {'✅' if item['Quantity']['match'] else '❌'} matches Invoice")
        lines.append(f"  Unit Price: ${item['Unit_Price']['PO']:.2f} {'✅' if item['Unit_Price']['match'] else '❌'} matches Invoice")
        lines.append(f"  Total: ${item['Total']['PO']:.2f} {'✅' if item['Total']['match'] else '❌'} matches Invoice")

    # Total Amount
    total_po = data.get("Total_Amount", {}).get("PO", "N/A")
    total_inv = data.get("Total_Amount", {}).get("Invoice", "N/A")
    match = data.get("Total_Amount", {}).get("match", False)
    lines.append(f"\nTotal Amount: ${total_po} {'✅ matches' if match else '❌ does not match'} Invoice ${total_inv}")

    return "\n".join(lines)
