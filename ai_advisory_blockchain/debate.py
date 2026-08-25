"""
debate.py
Part 3C - Multi-agent debate demo (3-agent: bull, bear, synthesizer)
MOCK_LLM baseline: template-based arguments using the ticker's real numbers.
"""

from stock_universe import STOCK_UNIVERSE

# Pick one ticker for the debate demo
DEBATE_TICKER = "PAYTECH"


def bull_agent(ticker: str) -> str:
    """Optimist agent: argues FOR the stock using its expected return and beta."""
    data = STOCK_UNIVERSE[ticker]
    r = data["analyst_expected_return"]
    b = data["beta"]
    return (
        f"BULL on {ticker}: With an expected return of {r:.1%} against a beta "
        f"of {b:.2f}, this offers attractive risk-adjusted upside. The higher "
        f"beta means {ticker} is well positioned to outperform when the market "
        f"is strong, rewarding investors who can tolerate the swings."
    )


def bear_agent(ticker: str) -> str:
    """Pessimist agent: argues AGAINST the stock using its std_dev (volatility) as the risk case."""
    data = STOCK_UNIVERSE[ticker]
    std = data["std_dev"]
    b = data["beta"]
    return (
        f"BEAR on {ticker}: A standard deviation of {std:.1%} signals real "
        f"volatility risk -- this stock's returns can swing sharply from year "
        f"to year. Combined with a beta of {b:.2f}, {ticker} is likely to fall "
        f"hard in a market downturn, which is a serious concern for capital "
        f"preservation."
    )


def synthesizer_agent(ticker: str, bull_text: str, bear_text: str) -> str:
    """Neutral synthesizer: reads both arguments, produces a balanced 2-3 sentence summary."""
    data = STOCK_UNIVERSE[ticker]
    r = data["analyst_expected_return"]
    std = data["std_dev"]
    return (
        f"SYNTHESIS on {ticker}: The bull case highlights an expected return of "
        f"{r:.1%} driven by strong market-linked upside, while the bear case "
        f"warns that {std:.1%} volatility makes this a genuinely risky holding. "
        f"On balance, {ticker} suits investors with a higher risk tolerance and "
        f"a longer time horizon, rather than conservative or short-term investors."
    )


def run_debate(ticker: str) -> dict:
    """Runs the full 3-agent debate for one ticker and returns all outputs."""
    bull_text = bull_agent(ticker)
    bear_text = bear_agent(ticker)
    synthesis_text = synthesizer_agent(ticker, bull_text, bear_text)

    return {
        "ticker": ticker,
        "bull": bull_text,
        "bear": bear_text,
        "synthesis": synthesis_text,
    }


if __name__ == "__main__":
    print(f"=== Paytm Money -- Multi-Agent Debate Demo (MOCK_LLM mode) ===")
    print(f"Ticker under debate: {DEBATE_TICKER}\n")

    result = run_debate(DEBATE_TICKER)

    print(result["bull"])
    print()
    print(result["bear"])
    print()
    print(result["synthesis"])