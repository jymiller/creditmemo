"""
Credit Memo Extraction Schema — from demo-requirements.md section 7.

Import and use:
    from schemas import CreditMemo, Field_, SourceRef, ValidationCheck

These are the contract types. Your output JSON must match this shape
regardless of what language or framework you use to build it.
"""

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal


class SourceRef(BaseModel):
    """Where a value came from — page number, which agent/tool, which method."""
    page: int
    agent: str          # e.g. "form", "table", "narrative", "visual", or custom
    method: str         # e.g. "pdfplumber-lattice", "claude-vision", "regex"
    confidence: float = 1.0


class Field_(BaseModel):
    """A single extracted value with its provenance."""
    value: str | float | int | None
    source: SourceRef


class Guarantor(BaseModel):
    name: Field_
    credit_score: Field_
    ownership_pct: Field_
    stated_net_worth: Field_ | None = None


class LoanTerms(BaseModel):
    amount: Field_
    rate: Field_
    rate_type: Field_
    term_years: Field_
    amortization_years: Field_


class Collateral(BaseModel):
    asset_type: Field_
    address: Field_
    estimated_value: Field_
    ltv_pct: Field_
    lien_position: Field_


class FinancialTable(BaseModel):
    name: str
    rows: list[dict] = Field(default_factory=list)
    source: SourceRef


class ValidationCheck(BaseModel):
    name: str
    formula: str
    expected: float | str
    observed: float | str
    status: Literal["pass", "fail", "warning"]
    source_pages: list[int] = Field(default_factory=list)


class CreditMemo(BaseModel):
    document_id: str
    memo_date: Field_
    borrower_name: Field_
    loan: LoanTerms
    collateral: Collateral
    guarantors: list[Guarantor] = Field(default_factory=list)
    sources: list[dict] = Field(default_factory=list)
    uses: list[dict] = Field(default_factory=list)
    tables: list[FinancialTable] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    analyst_notes: str | None = None
    validation: list[ValidationCheck] = Field(default_factory=list)
