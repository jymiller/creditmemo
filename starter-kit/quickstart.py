#!/usr/bin/env python3
"""
Quickstart — extract one field from the sample PDF in under 5 minutes.

This script proves the round trip works:
    PDF  -->  LLM  -->  structured output with provenance

Run it:
    export ANTHROPIC_API_KEY=sk-ant-...
    pip install anthropic pdfplumber pydantic
    python quickstart.py

Then look at the JSON output. You just extracted your first field.
Now fork this script and extract more.
"""

import json
import os
import sys

try:
    import anthropic
except ImportError:
    print("Run: pip install anthropic")
    sys.exit(1)

try:
    import pdfplumber
except ImportError:
    print("Run: pip install pdfplumber")
    sys.exit(1)


PDF_PATH = os.path.join(os.path.dirname(__file__), "..", "Sample-Enhanced-Memo.pdf")


def extract_page_text(pdf_path: str, page_num: int) -> str:
    """Extract text from a single page (0-indexed)."""
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        return page.extract_text() or ""


def extract_loan_amount(page_text: str) -> dict:
    """Ask Claude to extract the loan amount from page 1 text."""
    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": f"""Extract the loan amount from this credit memo page.

Return ONLY a JSON object with this exact shape:
{{"loan_amount": <number>, "rate": <number>, "rate_type": "<string>", "term_years": <number>, "amortization_years": <number>}}

Page text:
{page_text}"""
        }]
    )

    # Parse the JSON from Claude's response
    text = response.content[0].text
    # Find JSON in the response
    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        return json.loads(text[start:end])
    return {}


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY first:")
        print("  export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    if not os.path.exists(PDF_PATH):
        print(f"Sample PDF not found at: {PDF_PATH}")
        print("Make sure you're running from the starter-kit/ directory")
        sys.exit(1)

    print("Extracting text from page 1...")
    page_text = extract_page_text(PDF_PATH, 0)  # page 1 is index 0

    print("Asking Claude to extract loan terms...")
    extracted = extract_loan_amount(page_text)

    # Wrap in the contract schema shape
    output = {
        "document_id": "quickstart-demo",
        "loan": {
            "amount": {
                "value": extracted.get("loan_amount"),
                "source": {"page": 1, "agent": "form", "method": "claude-sonnet", "confidence": 1.0}
            },
            "rate": {
                "value": extracted.get("rate"),
                "source": {"page": 1, "agent": "form", "method": "claude-sonnet", "confidence": 1.0}
            },
            "rate_type": {
                "value": extracted.get("rate_type"),
                "source": {"page": 1, "agent": "form", "method": "claude-sonnet", "confidence": 1.0}
            },
            "term_years": {
                "value": extracted.get("term_years"),
                "source": {"page": 1, "agent": "form", "method": "claude-sonnet", "confidence": 1.0}
            },
            "amortization_years": {
                "value": extracted.get("amortization_years"),
                "source": {"page": 1, "agent": "form", "method": "claude-sonnet", "confidence": 1.0}
            }
        }
    }

    print()
    print(json.dumps(output, indent=2))
    print()
    print("You just extracted your first fields with provenance.")
    print("Now extend this to extract guarantors, tables, narrative...")
    print("Run: python validate.py your-output.json  to check your progress.")


if __name__ == "__main__":
    main()
