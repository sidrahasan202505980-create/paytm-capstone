"""
advisory_agent.py
Part 3A - Portfolio advisory agent (agentic think-act-observe pattern)
MOCK_LLM baseline: no API calls, deterministic rule-based + f-string narrative.
"""

import math
from stock_universe import STOCK_UNIVERSE, RISK_FREE_RATE, MARKET_RETURN
from investor_profiles import INVESTOR_PROFILES

# Fixed correlation assumption (given in assignment) - every pair of stocks
# is assumed to move together with this correlation coefficient.
CORRELATION = 0.3

# THINK stage: prescribed lookup table (exact rule given by assignment)
RISK_TOLERANCE_ALLOCATION = {
    "Conservative": ["PAYBOND", "PAYGOLD", "PAYRETAIL"],
    "Moderate": ["PAYRETAIL", "PAYINFRA", "PAYGOLD"],
    "Aggressive": ["PAYTECH", "PAYFIN", "PAYINFRA"],
}

ESCALATION_THRESHOLD = 0.20  # 20% portfolio std dev triggers human review


def think(investor_profile: dict) -> list:
    """THINK: decide which 3 tickers to recommend based on risk_tolerance."""
    risk_tolerance = investor_profile["risk_tolerance"]
    return RISK_TOLERANCE_ALLOCATION[risk_tolerance]


def get_stock_data(ticker: str) -> dict:
    """ACT (tool call): simulates an external API call fetching stock data."""
    return STOCK_UNIVERSE[ticker]


def capm_expected_return(beta: float) -> float:
    """CAPM formula: E(R) = Rf + beta * (Rm - Rf)"""
    return RISK_FREE_RATE + beta * (MARKET_RETURN - RISK_FREE_RATE)


def observe_and_decide(tickers: list) -> dict:
    """
    OBSERVE -> DECIDE:
    - fetch data for each ticker via the 'tool call' (Act)
    - compute CAPM expected return per stock
    - compute equal-weighted (1/3 each) portfolio expected return
    - compute portfolio variance/std using pairwise covariance = rho*sigma_i*sigma_j
    - decide whether to escalate to a human advisor
    """
    n = len(tickers)
    weight = 1 / n

    stock_data = {t: get_stock_data(t) for t in tickers}
    capm_returns = {t: capm_expected_return(stock_data[t]["beta"]) for t in tickers}

    # Portfolio expected return = weighted average of each stock's CAPM return
    portfolio_return = sum(weight * capm_returns[t] for t in tickers)

    # Portfolio variance = sum(wi^2 * sigma_i^2) + 2 * sum_{i<j}(wi*wj*Cov(i,j))
    variance = 0.0
    for t in tickers:
        sigma_i = stock_data[t]["std_dev"]
        variance += (weight ** 2) * (sigma_i ** 2)

    for i in range(n):
        for j in range(i + 1, n):
            sigma_i = stock_data[tickers[i]]["std_dev"]
            sigma_j = stock_data[tickers[j]]["std_dev"]
            cov_ij = CORRELATION * sigma_i * sigma_j
            variance += 2 * weight * weight * cov_ij

    portfolio_std = math.sqrt(variance)
    escalate = portfolio_std > ESCALATION_THRESHOLD

    return {
        "tickers": tickers,
        "portfolio_return": portfolio_return,
        "portfolio_std": portfolio_std,
        "escalate": escalate,
        "capm_returns": capm_returns,
    }


def build_narrative(investor_profile: dict, result: dict) -> str:
    """
    MOCK_LLM baseline: deterministic f-string narrative sentence.
    (Optional MOCK_LLM=0 extension would call a real LLM here instead -
    not required, not attempted in this submission.)
    """
    risk_tolerance = investor_profile["risk_tolerance"]
    investor_id = investor_profile["investor_id"]
    tickers = result["tickers"]
    ret_pct = result["portfolio_return"] * 100
    vol_pct = result["portfolio_std"] * 100

    return (
        f"For {risk_tolerance} investor {investor_id}, we recommend an allocation "
        f"across {tickers} with an expected portfolio return of {ret_pct:.1f}% "
        f"and volatility of {vol_pct:.1f}%."
    )


def run_advisory_agent(investor_profile: dict) -> dict:
    """Full pipeline for one investor: Think -> Act -> Observe/Decide -> narrate."""
    tickers = think(investor_profile)
    result = observe_and_decide(tickers)
    narrative = build_narrative(investor_profile, result)

    output = {
        "investor_id": investor_profile["investor_id"],
        "risk_tolerance": investor_profile["risk_tolerance"],
        "tickers": tickers,
        "portfolio_return": result["portfolio_return"],
        "portfolio_std": result["portfolio_std"],
        "narrative": narrative,
    }

    if result["escalate"]:
        output["flag"] = "ESCALATED_TO_HUMAN_ADVISOR"
    else:
        output["recommendation_finalized"] = True

    return output


if __name__ == "__main__":
    print("=== Paytm Money -- Portfolio Advisory Agent (MOCK_LLM mode) ===\n")
    for profile in INVESTOR_PROFILES:
        result = run_advisory_agent(profile)
        print(f"Investor: {result['investor_id']} ({result['risk_tolerance']})")
        print(f"  Tickers: {result['tickers']}")
        print(f"  Expected Return: {result['portfolio_return']*100:.2f}%")
        print(f"  Volatility (Std Dev): {result['portfolio_std']*100:.2f}%")
        if "flag" in result:
            print(f"  STATUS: {result['flag']}")
        else:
            print(f"  STATUS: Recommendation finalized")
        print(f"  Narrative: {result['narrative']}")
        print()