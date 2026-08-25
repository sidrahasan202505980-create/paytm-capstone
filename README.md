# Paytm Analytics Capstone

One connected platform across Paytm's core businesses -- payments/fraud,
credit risk lending, and AI-augmented advisory + blockchain risk -- built
as three internally-linked parts of a single analyst-to-ML capstone project.

## Repository Structure

- `/payments_fraud_analytics` -- Part 1 (35 marks)
- `/credit_risk_lending_ml` -- Part 2 (40 marks)
- `/ai_advisory_blockchain` -- Part 3 (25 marks)
- `requirements.txt` -- one consolidated requirements file covering all three parts

## Setup

This project uses **one consolidated `requirements.txt`** at the repository
root (not a separate requirements file per part), since all three parts were
built and run in the same Python environment.

1. Install Python 3.x (this project was built and tested using Anaconda).
2. From the repository root, install dependencies:

   pip install -r requirements.txt

   (Dependencies used across the project: pandas, numpy, matplotlib.
   Modules such as sqlite3, random, math, and datetime are part of the
   Python standard library and require no separate installation.)

## How to Run Each Part

### Part 1 -- payments_fraud_analytics

Generates synthetic payment transaction data and builds a fraud-detection
SQL and dashboard analysis on top of it.

    cd payments_fraud_analytics
    python generate_data.py
    python build_database.py
    python fraud_queries.py
    python dashboard.py

Run each script with `payments_fraud_analytics` as the working directory,
as generate_data.py writes its output CSVs using relative paths.

### Part 2 -- credit_risk_lending_ml

Generates synthetic credit applicant data and builds a machine-learning
credit-risk model, analyzed inside the Jupyter notebook.

    cd credit_risk_lending_ml
    python generate_data.py
    jupyter notebook credit_risk_analysis.ipynb

Run generate_data.py with `credit_risk_lending_ml` as the working directory
for the same reason as Part 1 -- relative-path CSV output.

### Part 3 -- ai_advisory_blockchain

An AI-augmented advisory toolkit: a portfolio-allocation agent (CAPM +
portfolio risk), a structured disclosure-signal extractor, a 3-agent bull/
bear/synthesizer debate demo, and a DCF valuation calculator -- all built
using an agentic think-act-observe pattern, entirely in MOCK_LLM mode (no
API key, no signup, no network call to any LLM provider required).

    cd ai_advisory_blockchain
    python advisory_agent.py
    python extract_disclosure.py
    python debate.py
    python dfc_calculator.py

See `ai_advisory_blockchain/README.md` for the recorded run transcripts,
the DCF sensitivity table, and confirmation of which MOCK_LLM mode was used.
See `ai_advisory_blockchain/blockchain_risk_note.md` for the written
blockchain/crypto risk appendix.

## Design Decisions Summary

**Part 1 (payments_fraud_analytics):** Synthetic transaction, merchant, and
ledger data is generated and loaded into a local SQLite database
(`paytm_payments.db`), which is queried with SQL to surface fraud-relevant
patterns (e.g. transaction concentration, merchant-level anomalies), and
summarized visually via a matplotlib-based dashboard.

**Part 2 (credit_risk_lending_ml):** Synthetic credit-applicant and
transaction-behaviour data is generated to reflect realistic borrower
profiles, then used inside a Jupyter notebook to build and evaluate a
credit-risk classification model, applying standard analyst-to-ML workflow
steps (data preparation, feature review, model fitting, evaluation).

**Part 3 (ai_advisory_blockchain):** Built strictly around an agentic
think-act-observe pattern rather than a retrieval/vector-database (RAG)
pipeline, per the assignment's design constraint. The portfolio advisory
agent uses a prescribed risk-tolerance lookup table (Think), a simulated
tool call to fetch stock data (Act), and CAPM-based expected-return plus
portfolio-variance computation with a human-in-the-loop escalation flag for
high-volatility allocations (Observe/Decide). Disclosure-signal extraction,
the 3-agent debate demo, and the DCF calculator all run in the fully
deterministic MOCK_LLM baseline mode, as required for grading, with no paid
or API-key-gated service used anywhere in this part.

## Academic Integrity

All code, analysis, and written interpretations in this repository are the
author's own work.
