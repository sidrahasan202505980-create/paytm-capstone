"""
dfc_calculator.py
Part 3D - DCF valuation calculator for a hypothetical Paytm Postpaid (BNPL) business line.

All inputs below are ILLUSTRATIVE, chosen and stated by the analyst (not real Paytm
financials), as explicitly permitted by the assignment. Figures are in INR.
"""

from stock_universe import RISK_FREE_RATE, MARKET_RETURN, STOCK_UNIVERSE

# ---------------------------------------------------------------------------
# STATED INPUTS AND ASSUMPTIONS (illustrative, chosen for this exercise)
# ---------------------------------------------------------------------------

BASE_EBIT = 150_000_000          # INR 15 crore, base-year operating profit
TAX_RATE = 0.25                   # 25% illustrative Indian corporate tax rate
BASE_DA = 20_000_000              # INR 2 crore, base-year Depreciation & Amortization
BASE_CAPEX = 25_000_000           # INR 2.5 crore, base-year Capital Expenditure
BASE_NWC_CHANGE = 10_000_000      # INR 1 crore, base-year change in Net Working Capital

# Year-by-year EBIT growth rates (5-year forecast, decelerating as business matures)
GROWTH_RATES = [0.18, 0.15, 0.12, 0.09, 0.07]

# D&A, CapEx, and NWC change are assumed to scale proportionally with EBIT each year
# (a standard simplification when detailed line-item forecasts aren't available).

# Cost of equity inputs: we reuse PAYFIN's beta (1.35) as the closest proxy in our
# stock universe for a fintech lending business line, via CAPM.
BETA_FOR_WACC = STOCK_UNIVERSE["PAYFIN"]["beta"]

# Cost of debt (pre-tax) - illustrative lending rate for a mid-size Indian fintech
COST_OF_DEBT_PRETAX = 0.09

# Illustrative capital structure
EQUITY_WEIGHT = 0.70
DEBT_WEIGHT = 0.30

# Terminal growth rate - chosen to sit at least 3 percentage points below base WACC,
# so it survives every +-1pp sensitivity combination without WACC <= growth anywhere.
TERMINAL_GROWTH = 0.05

# Simple cross-check multiple
EBITDA_MULTIPLE = 8.0
# For the EV/EBITDA cross-check we treat EBITDA = EBIT + D&A (base year)
BASE_EBITDA = BASE_EBIT + BASE_DA


# ---------------------------------------------------------------------------
# CORE CALCULATIONS
# ---------------------------------------------------------------------------

def cost_of_equity_capm(beta: float) -> float:
    """CAPM: Re = Rf + beta * (Rm - Rf)"""
    return RISK_FREE_RATE + beta * (MARKET_RETURN - RISK_FREE_RATE)


def calculate_wacc(re: float, rd_pretax: float, tax: float,
                    e_weight: float, d_weight: float) -> float:
    """WACC = (E/V)*Re + (D/V)*Rd*(1 - tax)"""
    return e_weight * re + d_weight * rd_pretax * (1 - tax)


def project_fcff(base_ebit, base_da, base_capex, base_nwc_change,
                  growth_rates, tax_rate) -> list:
    """
    Projects 5 years of Unlevered Free Cash Flow to the Firm (FCFF).
    FCFF = EBIT*(1-tax) + D&A - CapEx - ChangeNWC
    D&A, CapEx, and NWC change scale with EBIT each year (stated assumption).
    """
    projections = []
    ebit = base_ebit
    da = base_da
    capex = base_capex
    nwc_change = base_nwc_change

    for year, g in enumerate(growth_rates, start=1):
        ebit = ebit * (1 + g)
        da = da * (1 + g)
        capex = capex * (1 + g)
        nwc_change = nwc_change * (1 + g)

        fcff = ebit * (1 - tax_rate) + da - capex - nwc_change

        projections.append({
            "year": year,
            "ebit": ebit,
            "da": da,
            "capex": capex,
            "nwc_change": nwc_change,
            "fcff": fcff,
        })

    return projections


def terminal_value(final_year_fcff: float, wacc: float, terminal_growth: float) -> float:
    """TV = FCFF_year5 * (1 + g) / (WACC - g)"""
    if wacc <= terminal_growth:
        raise ValueError("WACC must exceed terminal growth rate (formula breaks otherwise).")
    return final_year_fcff * (1 + terminal_growth) / (wacc - terminal_growth)


def present_value(cashflows_by_year: dict, wacc: float) -> float:
    """Discounts a dict of {year: cashflow} back to present value using WACC."""
    total = 0.0
    for year, cf in cashflows_by_year.items():
        total += cf / ((1 + wacc) ** year)
    return total


def run_dcf(wacc: float, terminal_growth: float) -> dict:
    """
    Runs the full DCF: projects FCFF, computes terminal value, discounts
    everything to present value, and returns the enterprise value plus detail.
    """
    projections = project_fcff(BASE_EBIT, BASE_DA, BASE_CAPEX, BASE_NWC_CHANGE,
                                GROWTH_RATES, TAX_RATE)

    cashflows_by_year = {p["year"]: p["fcff"] for p in projections}
    final_fcff = projections[-1]["fcff"]

    tv = terminal_value(final_fcff, wacc, terminal_growth)

    pv_of_fcff = present_value(cashflows_by_year, wacc)
    pv_of_tv = tv / ((1 + wacc) ** len(GROWTH_RATES))

    enterprise_value = pv_of_fcff + pv_of_tv

    return {
        "projections": projections,
        "terminal_value": tv,
        "pv_of_fcff": pv_of_fcff,
        "pv_of_terminal_value": pv_of_tv,
        "enterprise_value": enterprise_value,
    }


def build_sensitivity_table(base_wacc: float, base_growth: float) -> dict:
    """
    Builds a 3x3 sensitivity table varying WACC and terminal growth by +-1
    percentage point each, producing 9 enterprise value combinations.
    """
    wacc_options = [base_wacc - 0.01, base_wacc, base_wacc + 0.01]
    growth_options = [base_growth - 0.01, base_growth, base_growth + 0.01]

    table = {}
    for w in wacc_options:
        for g in growth_options:
            result = run_dcf(w, g)
            table[(round(w, 4), round(g, 4))] = result["enterprise_value"]

    return table


def ev_ebitda_cross_check(ebitda: float, multiple: float) -> float:
    """Simple valuation cross-check: EV = EBITDA x multiple."""
    return ebitda * multiple


# ---------------------------------------------------------------------------
# MAIN - run and print everything
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Paytm Postpaid (illustrative BNPL line) -- DCF Valuation ===\n")

    re = cost_of_equity_capm(BETA_FOR_WACC)
    wacc = calculate_wacc(re, COST_OF_DEBT_PRETAX, TAX_RATE, EQUITY_WEIGHT, DEBT_WEIGHT)

    print(f"Cost of Equity (CAPM, beta={BETA_FOR_WACC}): {re*100:.2f}%")
    print(f"WACC (base case): {wacc*100:.2f}%")
    print(f"Terminal growth rate: {TERMINAL_GROWTH*100:.2f}%")
    print(f"Cushion (WACC - terminal growth): {(wacc-TERMINAL_GROWTH)*100:.2f} percentage points\n")

    base_result = run_dcf(wacc, TERMINAL_GROWTH)

    print("5-Year FCFF Projection (INR):")
    for p in base_result["projections"]:
        print(f"  Year {p['year']}: EBIT={p['ebit']:,.0f}  "
              f"FCFF={p['fcff']:,.0f}")

    print(f"\nTerminal Value: INR {base_result['terminal_value']:,.0f}")
    print(f"PV of 5-year FCFF: INR {base_result['pv_of_fcff']:,.0f}")
    print(f"PV of Terminal Value: INR {base_result['pv_of_terminal_value']:,.0f}")
    print(f"Enterprise Value (DCF, base case): INR {base_result['enterprise_value']:,.0f}\n")

    print("=== 3x3 Sensitivity Table (Enterprise Value, INR) ===")
    sensitivity = build_sensitivity_table(wacc, TERMINAL_GROWTH)
    wacc_options = sorted(set(k[0] for k in sensitivity))
    growth_options = sorted(set(k[1] for k in sensitivity))

    header = "WACC \\ Growth".ljust(16) + "".join(f"{g*100:>14.1f}%" for g in growth_options)
    print(header)
    for w in wacc_options:
        row = f"{w*100:>14.1f}%  "
        for g in growth_options:
            ev = sensitivity[(w, g)]
            row += f"{ev:>14,.0f}"
        print(row)

    print(f"\n=== EV/EBITDA Cross-Check ===")
    ev_multiple = ev_ebitda_cross_check(BASE_EBITDA, EBITDA_MULTIPLE)
    print(f"Base-year EBITDA: INR {BASE_EBITDA:,.0f}")
    print(f"EV/EBITDA method (8.0x multiple): INR {ev_multiple:,.0f}")
    print(f"DCF method (base case): INR {base_result['enterprise_value']:,.0f}")

    diff_pct = (base_result['enterprise_value'] - ev_multiple) / ev_multiple * 100
    print(f"\nComment: The DCF valuation is {abs(diff_pct):.1f}% "
          f"{'higher' if diff_pct > 0 else 'lower'} than the simple EV/EBITDA "
          f"cross-check. This gap reflects the DCF's sensitivity to the chosen "
          f"growth trajectory and terminal assumptions, versus the EV/EBITDA "
          f"method's reliance on a single sector-average multiple that ignores "
          f"this specific business's above-average growth profile.")