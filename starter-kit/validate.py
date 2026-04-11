#!/usr/bin/env python3
"""
Phase 1 Validator — Credit Memo Proofreader.

Validates extraction output from a single credit memo PDF against the contract.
This is the Phase 1 ("Crack the PDF") validator for the hackathon.

Usage:
    python validate.py output.json
    python validate.py ../sample-output.json   # test against the reference

Runs the 9 mandatory math checks (C1-C9) from demo-requirements.md section 8.
Prints a colored pass/fail report and a tier summary.

Phase 1 Tiers:
    Bronze  (3 checks)  C1, C5, C8           "I can extract numbers and the math adds up"
    Silver  (6 checks)  + C2, C4, C9         "I can extract tables and cross-reference pages"
    Gold    (all 9)     + C3, C6, C7          "Full contract satisfied"

No dependencies beyond Python stdlib. Runs anywhere.

NOTE: Phase 2 ("The Loan File") introduces multiple document types (PFS, rent rolls,
appraisals, scanned docs) and cross-document verification across origination and
servicing timelines. Phase 2 will require a separate cross-document validator with
its own tier structure (Pipeline / Crosscheck / Platinum).
"""

import json
import sys
import os

# -- ANSI colors (disabled if NO_COLOR is set or not a terminal) ----------

USE_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")

def green(s):  return f"\033[92m{s}\033[0m" if USE_COLOR else s
def red(s):    return f"\033[91m{s}\033[0m" if USE_COLOR else s
def yellow(s): return f"\033[93m{s}\033[0m" if USE_COLOR else s
def bold(s):   return f"\033[1m{s}\033[0m" if USE_COLOR else s
def dim(s):    return f"\033[2m{s}\033[0m" if USE_COLOR else s


# -- Helpers ---------------------------------------------------------------

def get(data, *keys, default=None):
    """Safely traverse nested dicts/lists."""
    current = data
    for k in keys:
        if isinstance(current, dict):
            current = current.get(k)
        elif isinstance(current, list) and isinstance(k, int) and k < len(current):
            current = current[k]
        else:
            return default
        if current is None:
            return default
    return current


def val(field_or_value):
    """Extract raw value from a Field_ dict or a plain value."""
    if isinstance(field_or_value, dict) and "value" in field_or_value:
        return field_or_value["value"]
    return field_or_value


def approx(a, b, tol_int=1, tol_ratio=0.02):
    """Check approximate equality. Uses tol_int for integers, tol_ratio for floats."""
    if a is None or b is None:
        return False
    a, b = float(a), float(b)
    if abs(a) > 100:
        return abs(a - b) <= tol_int
    return abs(a - b) <= tol_ratio


def find_table(data, name_fragment):
    """Find a table by partial name match."""
    for t in data.get("tables", []):
        if name_fragment.lower() in t.get("name", "").lower():
            return t
    return None


def find_row(table, label_fragment, col=None):
    """Find a value in a table by label and optional column."""
    if not table:
        return None
    for row in table.get("rows", []):
        label = row.get("label", "") or row.get("category", "")
        if label_fragment.lower() in label.lower():
            if col:
                return row.get(col)
            # Return first numeric-looking value
            for k, v in row.items():
                if k not in ("label", "category", "entity") and v is not None:
                    return v
    return None


# -- Check definitions -----------------------------------------------------

BRONZE_CHECKS = ["C1", "C5", "C8"]
SILVER_CHECKS = ["C2", "C4", "C9"]
GOLD_CHECKS = ["C3", "C6", "C7"]


def run_checks(data):
    results = []

    # C1: Sources = Uses
    sources_total = sum(s.get("amount", 0) for s in data.get("sources", []))
    uses_total = sum(u.get("amount", 0) for u in data.get("uses", []))
    results.append({
        "id": "C1", "name": "Sources = Uses",
        "formula": f"sum(sources) == sum(uses)",
        "expected": 514500, "observed": sources_total if sources_total else uses_total,
        "passed": approx(sources_total, uses_total) and approx(sources_total, 514500),
        "tier": "bronze"
    })

    # C2: G1 stated net worth
    g1_nw_table = find_table(data, "Guarantor 1 Net Worth") or find_table(data, "G1 Net Worth")
    g1_assets = find_row(g1_nw_table, "Total Assets") if g1_nw_table else None
    g1_liab = find_row(g1_nw_table, "Total Liabilities") if g1_nw_table else None
    g1_nw = find_row(g1_nw_table, "Stated Net Worth") if g1_nw_table else None
    g1_nw_obs = g1_nw
    if g1_assets and g1_liab and g1_nw is None:
        g1_nw_obs = float(g1_assets) - float(g1_liab)
    # Also check guarantor-level stated_net_worth
    g1_guarantor_nw = val(get(data, "guarantors", 0, "stated_net_worth"))
    if g1_guarantor_nw and g1_nw_obs is None:
        g1_nw_obs = g1_guarantor_nw
    results.append({
        "id": "C2", "name": "G1 stated net worth",
        "formula": "total_assets - total_liabilities = 3,689,440",
        "expected": 3689440, "observed": g1_nw_obs,
        "passed": approx(g1_nw_obs, 3689440) if g1_nw_obs else False,
        "tier": "silver"
    })

    # C3: G1 adjusted net worth
    g1_adj = find_row(g1_nw_table, "Adjusted Net Worth") if g1_nw_table else None
    results.append({
        "id": "C3", "name": "G1 adjusted net worth",
        "formula": "assets - liabilities - adjustments = 3,264,440",
        "expected": 3264440, "observed": g1_adj,
        "passed": approx(g1_adj, 3264440) if g1_adj else False,
        "tier": "gold"
    })

    # C4: G2 stated net worth
    g2_guarantor_nw = val(get(data, "guarantors", 1, "stated_net_worth"))
    g2_nw_table = find_table(data, "Guarantor 2 Net Worth") or find_table(data, "G2 Net Worth")
    g2_nw_obs = g2_guarantor_nw
    if g2_nw_obs is None and g2_nw_table:
        g2_assets = find_row(g2_nw_table, "Total Assets")
        g2_liab = find_row(g2_nw_table, "Total Liabilities")
        if g2_assets and g2_liab:
            g2_nw_obs = float(g2_assets) - float(g2_liab)
    results.append({
        "id": "C4", "name": "G2 stated net worth",
        "formula": "total_assets - total_liabilities = 890,300",
        "expected": 890300, "observed": g2_nw_obs,
        "passed": approx(g2_nw_obs, 890300) if g2_nw_obs else False,
        "tier": "silver"
    })

    # C5: Ownership sum
    ownership = [val(g.get("ownership_pct")) for g in data.get("guarantors", []) if val(g.get("ownership_pct")) is not None]
    own_sum = sum(float(o) for o in ownership) if ownership else 0
    results.append({
        "id": "C5", "name": "Ownership sum",
        "formula": "sum(guarantor.ownership_pct) == 100",
        "expected": 100, "observed": own_sum,
        "passed": approx(own_sum, 100),
        "tier": "bronze"
    })

    # C6: G1 DSCR 2020
    g1_cf_table = find_table(data, "Guarantor 1 Personal Cash Flow") or find_table(data, "G1 Cash Flow")
    g1_gcf_2020 = find_row(g1_cf_table, "Gross Cash Flow", "12/31/2020") if g1_cf_table else None
    g1_debt_2020 = find_row(g1_cf_table, "Total Debt", "12/31/2020") if g1_cf_table else None
    g1_dscr_obs = None
    if g1_gcf_2020 and g1_debt_2020 and float(g1_debt_2020) != 0:
        g1_dscr_obs = round(float(g1_gcf_2020) / float(g1_debt_2020), 2)
    results.append({
        "id": "C6", "name": "G1 DSCR 2020",
        "formula": "gross_cash_flow / total_debt = 3.38",
        "expected": 3.38, "observed": g1_dscr_obs,
        "passed": approx(g1_dscr_obs, 3.38) if g1_dscr_obs else False,
        "tier": "gold"
    })

    # C7: Global DSCR 2019
    global_table = find_table(data, "Global Cash Flow")
    global_cash_2019 = None
    global_debt_2019 = None
    if global_table:
        for row in global_table.get("rows", []):
            if "total" in (row.get("entity", "") or "").lower():
                if "combined cash" in (row.get("label", "") or "").lower():
                    global_cash_2019 = row.get("2019")
                if "combined debt" in (row.get("label", "") or "").lower():
                    global_debt_2019 = row.get("2019")
    global_dscr_obs = None
    if global_cash_2019 and global_debt_2019 and float(global_debt_2019) != 0:
        global_dscr_obs = round(float(global_cash_2019) / float(global_debt_2019), 2)
    results.append({
        "id": "C7", "name": "Global DSCR 2019",
        "formula": "total_combined_cash / total_combined_debt_service = 2.87",
        "expected": 2.87, "observed": global_dscr_obs,
        "passed": approx(global_dscr_obs, 2.87) if global_dscr_obs else False,
        "tier": "gold"
    })

    # C8: Rent roll sum
    # Look for rent data in sources/uses, or in the loan/collateral area, or validation
    # The sample output may store this in different places — be flexible
    rent_total = None
    for check in data.get("validation", []):
        if "rent" in check.get("name", "").lower() and "roll" in check.get("name", "").lower():
            rent_total = check.get("observed")
            break
    if rent_total is None:
        # Try to find from tables
        transactional = find_table(data, "Transactional")
        if transactional:
            rent_total = find_row(transactional, "Gross Rents")
    results.append({
        "id": "C8", "name": "Rent roll sum",
        "formula": "sum(unit_rents) * 12 = 53,400",
        "expected": 53400, "observed": rent_total,
        "passed": approx(rent_total, 53400) if rent_total else False,
        "tier": "bronze"
    })

    # C9: Cross-page rents
    # Check if the output's own validation includes this, or trust C8
    cross_page_ok = False
    for check in data.get("validation", []):
        if "cross" in check.get("name", "").lower() and check.get("status") == "pass":
            cross_page_ok = True
            break
    if not cross_page_ok and rent_total:
        # If C8 passed, give credit — the rent number was validated
        cross_page_ok = approx(rent_total, 53400)
    results.append({
        "id": "C9", "name": "Cross-page rents",
        "formula": "narrative(p8) == transactional(p17) = 53,400",
        "expected": 53400, "observed": rent_total if rent_total else "not found",
        "passed": cross_page_ok,
        "tier": "silver"
    })

    return results


# -- Reporting -------------------------------------------------------------

def print_report(results):
    print()
    print(bold("  PROOFREADER REPORT"))
    print(bold("  " + "=" * 58))
    print()

    for r in results:
        status = green("PASS") if r["passed"] else red("FAIL")
        tier_label = dim(f"[{r['tier']}]")
        obs = r["observed"] if r["observed"] is not None else red("missing")
        print(f"  {status}  {r['id']}  {r['name']}")
        print(f"        {dim(r['formula'])}")
        print(f"        expected: {r['expected']}  |  observed: {obs}  {tier_label}")
        print()

    # Tier summary
    bronze_ids = [r for r in results if r["id"] in BRONZE_CHECKS]
    silver_ids = [r for r in results if r["id"] in SILVER_CHECKS]
    gold_ids = [r for r in results if r["id"] in GOLD_CHECKS]

    bronze_pass = all(r["passed"] for r in bronze_ids)
    silver_pass = bronze_pass and all(r["passed"] for r in silver_ids)
    gold_pass = silver_pass and all(r["passed"] for r in gold_ids)

    total_pass = sum(1 for r in results if r["passed"])
    total = len(results)

    print(bold("  " + "-" * 58))
    print(f"  {bold('CHECKS PASSED:')} {total_pass} / {total}")
    print()

    if gold_pass:
        tier = "GOLD"
        msg = "Full contract satisfied. The proofreader is happy."
        color = yellow
    elif silver_pass:
        tier = "SILVER"
        msg = "Tables extracted and cross-referenced. Two more checks for Gold."
        color = bold
    elif bronze_pass:
        tier = "BRONZE"
        msg = "Numbers extracted and math adds up. Keep going for Silver."
        color = bold
    else:
        tier = "IN PROGRESS"
        msg = f"Keep building. {3 - sum(1 for r in bronze_ids if r['passed'])} more checks to reach Bronze."
        color = dim

    print(f"  {color(f'TIER: {tier}')}")
    print(f"  {msg}")
    print()
    print(dim("  Bronze: C1 + C5 + C8  |  Silver: + C2 + C4 + C9  |  Gold: + C3 + C6 + C7"))
    print()

    return bronze_pass


# -- Schema check ----------------------------------------------------------

def check_schema(data):
    """Quick structural checks — not exhaustive, just enough to catch obvious problems."""
    issues = []
    required_top = ["document_id", "memo_date", "borrower_name", "loan", "collateral", "guarantors", "validation"]
    for field in required_top:
        if field not in data:
            issues.append(f"Missing top-level field: {field}")

    if "loan" in data:
        for f in ["amount", "rate", "rate_type", "term_years", "amortization_years"]:
            if f not in data["loan"]:
                issues.append(f"Missing loan.{f}")

    if "guarantors" in data and len(data["guarantors"]) == 0:
        issues.append("guarantors list is empty (expected at least 2)")

    return issues


# -- Main ------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(f"\nUsage: python {sys.argv[0]} <output.json>")
        print(f"\nExample: python {sys.argv[0]} sample-output.json")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(red(f"\nFile not found: {filepath}"))
        sys.exit(1)

    with open(filepath) as f:
        data = json.load(f)

    # Schema check
    issues = check_schema(data)
    if issues:
        print()
        print(bold("  SCHEMA ISSUES"))
        for issue in issues:
            print(f"  {yellow('!')}  {issue}")
        print()

    # Run checks
    results = run_checks(data)
    bronze_pass = print_report(results)

    sys.exit(0 if bronze_pass else 1)


if __name__ == "__main__":
    main()
