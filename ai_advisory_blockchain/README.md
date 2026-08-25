# ai_advisory_blockchain -- Part 3 Notes

## MOCK_LLM Mode

MOCK_LLM was left **unset** (the default) for this entire submission.
Every script below ran in the fully deterministic, rule-based mock mode,
with no signup, no API key, and no network call to any LLM provider.
The optional MOCK_LLM=0 extension (real LLM calls via Groq's free tier)
was **not** attempted for this submission, so there are no free-tier
usage notes to report.

## How to reproduce these transcripts

From inside the ai_advisory_blockchain folder, run:

```
python advisory_agent.py
python extract_disclosure.py
python debate.py
python dfc_calculator.py
```

All four scripts use only the local data files in this folder
(stock_universe.py, investor_profiles.py, disclosure_snippets.py)
and require no external services.

## Recorded Run Transcript -- advisory_agent.py

```
=== Paytm Money -- Portfolio Advisory Agent (MOCK_LLM mode) ===

Investor: INV01 (Conservative)
  Tickers: ['PAYBOND', 'PAYGOLD', 'PAYRETAIL']
  Expected Return: 9.20%
  Volatility (Std Dev): 8.44%
  STATUS: Recommendation finalized
  Narrative: For Conservative investor INV01, we recommend an allocation across ['PAYBOND', 'PAYGOLD', 'PAYRETAIL'] with an expected portfolio return of 9.2% and volatility of 8.4%.

Investor: INV02 (Moderate)
  Tickers: ['PAYRETAIL', 'PAYINFRA', 'PAYGOLD']
  Expected Return: 11.30%
  Volatility (Std Dev): 12.57%
  STATUS: Recommendation finalized
  Narrative: For Moderate investor INV02, we recommend an allocation across ['PAYRETAIL', 'PAYINFRA', 'PAYGOLD'] with an expected portfolio return of 11.3% and volatility of 12.6%.

Investor: INV03 (Aggressive)
  Tickers: ['PAYTECH', 'PAYFIN', 'PAYINFRA']
  Expected Return: 15.00%
  Volatility (Std Dev): 20.58%
  STATUS: ESCALATED_TO_HUMAN_ADVISOR
  Narrative: For Aggressive investor INV03, we recommend an allocation across ['PAYTECH', 'PAYFIN', 'PAYINFRA'] with an expected portfolio return of 15.0% and volatility of 20.6%.

Investor: INV04 (Moderate)
  Tickers: ['PAYRETAIL', 'PAYINFRA', 'PAYGOLD']
  Expected Return: 11.30%
  Volatility (Std Dev): 12.57%
  STATUS: Recommendation finalized
  Narrative: For Moderate investor INV04, we recommend an allocation across ['PAYRETAIL', 'PAYINFRA', 'PAYGOLD'] with an expected portfolio return of 11.3% and volatility of 12.6%.

Investor: INV05 (Aggressive)
  Tickers: ['PAYTECH', 'PAYFIN', 'PAYINFRA']
  Expected Return: 15.00%
  Volatility (Std Dev): 20.58%
  STATUS: ESCALATED_TO_HUMAN_ADVISOR
  Narrative: For Aggressive investor INV05, we recommend an allocation across ['PAYTECH', 'PAYFIN', 'PAYINFRA'] with an expected portfolio return of 15.0% and volatility of 20.6%.


```

## Recorded Run Transcript -- extract_disclosure.py

```
=== Paytm Disclosure Signal Extraction (MOCK_LLM mode) ===

Snippet: doc_01: Assuming input costs remain stable through the next two quarters, we expect margins to hold at current levels.
  Risk Flags: []
  Hedging Detected: True
  Sentiment: cautious

Snippet: doc_02: The company faces an ongoing litigation matter related to a former vendor contract; management believes the exposure is not material.
  Risk Flags: ['litigation']
  Hedging Detected: False
  Sentiment: neutral

Snippet: doc_03: Our top three customers together account for approximately 42 percent of total revenue this year.
  Risk Flags: ['customer_concentration']
  Hedging Detected: False
  Sentiment: neutral

Snippet: doc_04: We remain cautiously optimistic about demand recovery, though visibility beyond the next quarter is limited given macro uncertainty.
  Risk Flags: []
  Hedging Detected: True
  Sentiment: cautious

Snippet: doc_05: The board is confident in the long-term strategy and has approved an expanded capital expenditure plan for the coming year.
  Risk Flags: []
  Hedging Detected: False
  Sentiment: confident

Snippet: doc_06: A recent regulatory notice has been received regarding data-localization compliance; the company is in active dialogue with the regulator.
  Risk Flags: ['regulatory']
  Hedging Detected: False
  Sentiment: neutral


```

## Recorded Run Transcript -- debate.py

```
=== Paytm Money -- Multi-Agent Debate Demo (MOCK_LLM mode) ===
Ticker under debate: PAYTECH

BULL on PAYTECH: With an expected return of 19.0% against a beta of 1.55, this offers attractive risk-adjusted upside. The higher beta means PAYTECH is well positioned to outperform when the market is strong, rewarding investors who can tolerate the swings.

BEAR on PAYTECH: A standard deviation of 34.0% signals real volatility risk -- this stock's returns can swing sharply from year to year. Combined with a beta of 1.55, PAYTECH is likely to fall hard in a market downturn, which is a serious concern for capital preservation.

SYNTHESIS on PAYTECH: The bull case highlights an expected return of 19.0% driven by strong market-linked upside, while the bear case warns that 34.0% volatility makes this a genuinely risky holding. On balance, PAYTECH suits investors with a higher risk tolerance and a longer time horizon, rather than conservative or short-term investors.

```

## Recorded Run Transcript -- dfc_calculator.py (includes DCF sensitivity table)

```
=== Paytm Postpaid (illustrative BNPL line) -- DCF Valuation ===

Cost of Equity (CAPM, beta=1.35): 15.10%
WACC (base case): 12.60%
Terminal growth rate: 5.00%
Cushion (WACC - terminal growth): 7.60 percentage points

5-Year FCFF Projection (INR):
  Year 1: EBIT=177,000,000  FCFF=115,050,000
  Year 2: EBIT=203,550,000  FCFF=132,307,500
  Year 3: EBIT=227,976,000  FCFF=148,184,400
  Year 4: EBIT=248,493,840  FCFF=161,520,996
  Year 5: EBIT=265,888,409  FCFF=172,827,466

Terminal Value: INR 2,389,319,803
PV of 5-year FCFF: INR 506,354,663
PV of Terminal Value: INR 1,320,318,645
Enterprise Value (DCF, base case): INR 1,826,673,308

=== 3x3 Sensitivity Table (Enterprise Value, INR) ===
WACC \ Growth              4.0%           5.0%           6.0%
          11.6%   1,887,369,247 2,109,849,381 2,411,857,713
          12.6%   1,661,947,107 1,826,673,308 2,041,354,383
          13.6%   1,483,672,853 1,609,532,074 1,768,533,947

=== EV/EBITDA Cross-Check ===
Base-year EBITDA: INR 170,000,000
EV/EBITDA method (8.0x multiple): INR 1,360,000,000
DCF method (base case): INR 1,826,673,308

Comment: The DCF valuation is 34.3% higher than the simple EV/EBITDA cross-check. This gap reflects the DCF's sensitivity to the chosen growth trajectory and terminal assumptions, versus the EV/EBITDA method's reliance on a single sector-average multiple that ignores this specific business's above-average growth profile.

```
