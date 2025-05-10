import re
from typing import Dict

def parse_ocr_text(text: str) -> Dict[str, str]:
    """Extract structured fields from OCR text."""
    fields = {
        "vendor": None,
        "date": None,
        "amount": None,
        "fuel_quantity": None
    }

    # 🏪 Vendor (first non-empty line, usually at the top)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if lines:
        fields["vendor"] = lines[0]  # crude assumption for now

    # 📅 Date
    date_pattern = r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\w+ \d{1,2}, \d{4})\b"
    date_match = re.search(date_pattern, text)
    if date_match:
        fields["date"] = date_match.group()

    # 💲 Amount
    amount_pattern = r"(?i)(total|amount)\D{0,5}(\$|₹)?\s?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)"
    amount_match = re.search(amount_pattern, text)
    if amount_match:
        fields["amount"] = amount_match.group(3)

    # 🛢️ Quantity (litres or gallons)
    qty_pattern = r"(\d{2,6})\s?(litres|liters|gallons|gal)"
    qty_match = re.search(qty_pattern, text, re.IGNORECASE)
    if qty_match:
        fields["fuel_quantity"] = f"{qty_match.group(1)} {qty_match.group(2)}"

    return fields
