import pandas as pd

def reconcile_payments(ledger_df, gateway_df):
    """
    Compares ledger_df against gateway_df and returns four DataFrames:
    1. missing_in_gateway - transactions in ledger but not in gateway
    2. missing_in_ledger - transactions in gateway but not in ledger (extra)
    3. amount_mismatches - transactions present in both, but amount_inr differs
    4. status_mismatches - transactions present in both, but status differs
    """

    # --- Set operations on transaction_id ---
    ledger_ids = set(ledger_df["transaction_id"])
    gateway_ids = set(gateway_df["transaction_id"])

    missing_in_gateway_ids = ledger_ids - gateway_ids
    missing_in_ledger_ids = gateway_ids - ledger_ids

    missing_in_gateway = ledger_df[ledger_df["transaction_id"].isin(missing_in_gateway_ids)].copy()
    missing_in_ledger = gateway_df[gateway_df["transaction_id"].isin(missing_in_ledger_ids)].copy()

    # --- pd.merge for pairwise comparison of rows present in both ---
    merged = pd.merge(
        ledger_df, gateway_df,
        on="transaction_id",
        suffixes=("_ledger", "_gateway"),
        how="inner"
    )

    # --- Amount mismatches ---
    amount_mismatches = merged[
        merged["amount_inr_ledger"] != merged["amount_inr_gateway"]
    ].copy()
    amount_mismatches["amount_difference"] = (
        amount_mismatches["amount_inr_gateway"] - amount_mismatches["amount_inr_ledger"]
    )
    amount_mismatches = amount_mismatches[
        ["transaction_id", "amount_inr_ledger", "amount_inr_gateway", "amount_difference"]
    ]

    # --- Status mismatches ---
    status_mismatches = merged[
        merged["status_ledger"] != merged["status_gateway"]
    ].copy()
    status_mismatches = status_mismatches[
        ["transaction_id", "status_ledger", "status_gateway"]
    ]

    return missing_in_gateway, missing_in_ledger, amount_mismatches, status_mismatches


if __name__ == "__main__":
    ledger = pd.read_csv("ledger.csv")
    gateway = pd.read_csv("gateway_export.csv")

    missing_gw, missing_ledger, amount_mismatch, status_mismatch = reconcile_payments(ledger, gateway)

    n = len(ledger)
    print(f"Missing in gateway: {len(missing_gw)} rows (expected ~5% of {n} ≈ {int(0.05*n)})")
    print(f"Missing in ledger (extra in gateway): {len(missing_ledger)} rows (expected ~2% of {n} ≈ {int(0.02*n)})")
    print(f"Amount mismatches: {len(amount_mismatch)} rows (expected ~3% of {n} ≈ {int(0.03*n)})")
    print(f"Status mismatches: {len(status_mismatch)} rows (expected ~2% of {n} ≈ {int(0.02*n)})")