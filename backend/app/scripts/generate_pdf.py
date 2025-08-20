from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path

def create_pdf(filename, content, output_dir="documents"):
    Path(output_dir).mkdir(exist_ok=True)
    c = canvas.Canvas(f"{output_dir}/{filename}", pagesize=letter)
    c.setFont("Helvetica", 12)
    y = 750  # Start near top of page
    for line in content.split('\n'):
        c.drawString(50, y, line)
        y -= 20  # Line spacing
        if y < 50:  # New page if needed
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 750
    c.save()

# Set 1: Matching PO and Invoice
match_po_content = """
Purchase Order
PO Number: PO12345
Date: 2025-08-01
Supplier: Acme Corp, 123 Main St, Springfield

Items:
1. Widget A, Quantity: 10, Unit Price: $50.00, Total: $500.00
2. Widget B, Quantity: 5, Unit Price: $20.00, Total: $100.00

Total Amount: $600.00
"""
match_inv_content = """
Invoice
Invoice Number: INV67890
PO Number: PO12345
Date: 2025-08-01
Supplier: Acme Corp, 123 Main St, Springfield

Items:
1. Widget A, Quantity: 10, Unit Price: $50.00, Total: $500.00
2. Widget B, Quantity: 5, Unit Price: $20.00, Total: $100.00

Total Amount: $600.00
"""

# Set 2: Mismatching PO and Invoice
mismatch_po_content = """
Purchase Order
PO Number: PO54321
Date: 2025-08-02
Supplier: Beta Supplies, 456 Oak St, Metropolis

Items:
1. Gadget X, Quantity: 20, Unit Price: $30.00, Total: $600.00
2. Gadget Y, Quantity: 10, Unit Price: $10.00, Total: $100.00

Total Amount: $700.00
"""
mismatch_inv_content = """
Invoice
Invoice Number: INV09876
PO Number: PO54321
Date: 2025-08-02
Supplier: Beta Supplies, 456 Oak St, Metropolis

Items:
1. Gadget X, Quantity: 15, Unit Price: $30.00, Total: $450.00
2. Gadget Y, Quantity: 10, Unit Price: $10.00, Total: $100.00

Total Amount: $550.00
"""

# Set 3: Random PO and Invoice
random_po_content = """
Purchase Order
PO Number: PO99999
Date: 2025-08-03
Supplier: Random Co, 789 Pine St, Gotham

Items:
1. Tool Z, Quantity: 8, Unit Price: $25.00, Total: $200.00

Total Amount: $200.00
"""
random_inv_content = """
Invoice
Invoice Number: INV55555
PO Number: PO11111
Date: 2025-07-01
Supplier: Other Inc, 101 Elm St, Star City

Items:
1. Service Fee, Quantity: 1, Unit Price: $300.00, Total: $300.00

Total Amount: $300.00
"""

# Generate PDFs in documents folder
create_pdf("po_match.pdf", match_po_content)
create_pdf("inv_match.pdf", match_inv_content)
create_pdf("po_mismatch.pdf", mismatch_po_content)
create_pdf("inv_mismatch.pdf", mismatch_inv_content)
create_pdf("po_random.pdf", random_po_content)
create_pdf("inv_random.pdf", random_inv_content)

print("Test PDFs generated in 'documents' directory")