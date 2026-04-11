"""
Credit Memo Extraction Schema — from demo-requirements.md section 7.

Import and use:
    from schemas import CreditMemo, Field_, SourceRef, ValidationCheck

These are the contract types. Your output JSON must match this shape
regardless of what language or framework you use to build it.

Phase 2 schemas (PersonalFinancialStatement, RentRoll, AppraisalSummary,
ScannedDocument, LoanFile, CrossDocumentCheck) are defined at the bottom
of this file for the "The Loan File" phase of the hackathon.
"""

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import date


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
    """Phase 1 schema: single credit memo extraction with 9 math checks (C1-C9)."""

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


# =============================================================================
# Phase 2 Schemas — "The Loan File"
#
# Multiple document types, cross-document verification, origination vs.
# servicing timeline. Tiers: Pipeline / Crosscheck / Platinum.
# =============================================================================


class PersonalFinancialStatement(BaseModel):
    """Personal Financial Statement (PFS) submitted by a borrower/guarantor."""

    borrower_name: str
    total_assets: float
    total_liabilities: float
    net_worth: float
    liquidity: float
    source_pages: list[int] = Field(default_factory=list)


class RentRollUnit(BaseModel):
    """A single unit within a rent roll."""

    unit_number: str
    tenant_name: str | None = None
    monthly_rent: float
    lease_start: date | None = None
    lease_end: date | None = None
    is_vacant: bool = False


class RentRoll(BaseModel):
    """Rent roll for a multi-unit property."""

    property_address: str
    units: list[RentRollUnit] = Field(default_factory=list)
    total_monthly_income: float
    occupancy_rate: float
    source_pages: list[int] = Field(default_factory=list)


class ComparableSale(BaseModel):
    """A comparable sale used in the sales comparison approach."""

    address: str
    sale_price: float
    sale_date: date | None = None
    price_per_unit: float | None = None


class AppraisalSummary(BaseModel):
    """Summary of a property appraisal report."""

    property_address: str
    appraised_value: float
    appraisal_date: date
    approach: Literal["income", "sales_comparison", "cost"]
    cap_rate: float | None = None
    comparable_sales: list[ComparableSale] = Field(default_factory=list)
    source_pages: list[int] = Field(default_factory=list)


class ScannedDocument(BaseModel):
    """A scanned/OCR'd document within the loan file."""

    document_type: str
    ocr_confidence: float
    page_count: int
    extracted_text: str
    source_file: str


class ServicingReview(BaseModel):
    """A periodic servicing review entry with associated documents."""

    review_date: date
    associated_documents: list[str] = Field(default_factory=list)


class LoanFile(BaseModel):
    """Phase 2 top-level schema: the full loan file aggregating all documents."""

    loan_id: str
    origination_date: date
    credit_memo: CreditMemo
    pfs: Optional[PersonalFinancialStatement] = None
    rent_roll: Optional[RentRoll] = None
    appraisal: Optional[AppraisalSummary] = None
    scanned_documents: list[ScannedDocument] = Field(default_factory=list)
    servicing_reviews: list[ServicingReview] = Field(default_factory=list)


class CrossDocumentCheck(BaseModel):
    """Result of a cross-document verification check (Phase 2)."""

    check_name: str
    status: Literal["pass", "fail", "skip"]
    expected_value: str | float | None = None
    actual_value: str | float | None = None
    source_document: str
    target_document: str
    message: str | None = None
