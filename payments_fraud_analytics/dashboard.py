import pandas as pd
import matplotlib.pyplot as plt

# --- Load data ---
ledger = pd.read_csv("ledger.csv", parse_dates=["transaction_time"])
gateway = pd.read_csv("gateway_export.csv", parse_dates=["transaction_time"])
merchants = pd.read_csv("merchants.csv")

# ============================================================
# HEADLINE LAYER: scorecards
# ============================================================

# Total GMV: sum of amount_inr for captured (successful) transactions
total_gmv = ledger[ledger["status"] == "captured"]["amount_inr"].sum()

# Overall success rate: % of transactions with status == captured
success_rate = (ledger["status"] == "captured").mean() * 100

# match_rate: transactions present in BOTH files with identical amount AND identical status
merged_check = pd.merge(
    ledger, gateway,
    on="transaction_id",
    suffixes=("_ledger", "_gateway"),
    how="inner"
)
matched = merged_check[
    (merged_check["amount_inr_ledger"] == merged_check["amount_inr_gateway"]) &
    (merged_check["status_ledger"] == merged_check["status_gateway"])
]
match_rate = (len(matched) / len(ledger)) * 100

# chargeback_ratio (headline): count-based, platform-wide
chargeback_ratio = (ledger["status"] == "chargeback").mean() * 100

print("=" * 50)
print("HEADLINE SCORECARDS")
print("=" * 50)
print(f"Total GMV: INR {total_gmv:,.0f}")
print(f"Success Rate: {success_rate:.2f}%")
print(f"Reconciliation Match Rate: {match_rate:.2f}%")
print(f"Chargeback Ratio: {chargeback_ratio:.2f}%")



# ============================================================
# TRENDS LAYER: daily GMV and daily chargeback count
# ============================================================

ledger["txn_date"] = ledger["transaction_time"].dt.date

daily_gmv = ledger[ledger["status"] == "captured"].groupby("txn_date")["amount_inr"].sum()
daily_chargebacks = ledger[ledger["status"] == "chargeback"].groupby("txn_date").size()

fig, ax1 = plt.subplots(figsize=(12, 5))

ax1.plot(daily_gmv.index, daily_gmv.values, color="tab:blue", label="Daily GMV (INR)")
ax1.set_xlabel("Date")
ax1.set_ylabel("Daily GMV (INR)", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")

ax2 = ax1.twinx()
ax2.plot(daily_chargebacks.index, daily_chargebacks.values, color="tab:red", label="Daily Chargebacks")
ax2.set_ylabel("Daily Chargeback Count", color="tab:red")
ax2.tick_params(axis="y", labelcolor="tab:red")

plt.title("Daily GMV and Chargeback Trend (30-Day Window)")
fig.tight_layout()
plt.savefig("dashboard_trends.png", dpi=150)
plt.close()
print("Saved: dashboard_trends.png")



# ============================================================
# BREAKDOWN LAYER: GMV by payment_method and by category
# ============================================================

captured = ledger[ledger["status"] == "captured"]

gmv_by_method = captured.groupby("payment_method")["amount_inr"].sum().sort_values(ascending=False)

# Join category in from merchants (like your Excel VLOOKUP did)
captured_with_category = captured.merge(merchants[["merchant_id", "category"]], on="merchant_id", how="left")
gmv_by_category = captured_with_category.groupby("category")["amount_inr"].sum().sort_values(ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].bar(gmv_by_method.index, gmv_by_method.values, color="steelblue")
axes[0].set_title("GMV by Payment Method")
axes[0].set_ylabel("GMV (INR)")
axes[0].tick_params(axis="x", rotation=30)

axes[1].bar(gmv_by_category.index, gmv_by_category.values, color="seagreen")
axes[1].set_title("GMV by Merchant Category")
axes[1].set_ylabel("GMV (INR)")
axes[1].tick_params(axis="x", rotation=45)

fig.tight_layout()
plt.savefig("dashboard_breakdown.png", dpi=150)
plt.close()
print("Saved: dashboard_breakdown.png")



# ============================================================
# DETAILS LAYER: top 10 merchants table with high-risk flag
# ============================================================

merchant_stats = ledger.groupby("merchant_id").agg(
    txn_count=("transaction_id", "count"),
    chargeback_count=("status", lambda x: (x == "chargeback").sum())
).reset_index()

merchant_stats["chargeback_ratio_pct"] = (
    merchant_stats["chargeback_count"] / merchant_stats["txn_count"] * 100
)
merchant_stats["high_risk_flag"] = merchant_stats["chargeback_ratio_pct"].apply(
    lambda x: "⚠ HIGH RISK" if x > 1 else ""
)

# Join merchant_name in
merchant_stats = merchant_stats.merge(merchants[["merchant_id", "merchant_name"]], on="merchant_id", how="left")

top10 = merchant_stats.sort_values("txn_count", ascending=False).head(10)
top10 = top10[["merchant_id", "merchant_name", "txn_count", "chargeback_count", "chargeback_ratio_pct", "high_risk_flag"]]
top10["chargeback_ratio_pct"] = top10["chargeback_ratio_pct"].round(2)

fig, ax = plt.subplots(figsize=(12, 4))
ax.axis("off")
tbl = ax.table(
    cellText=top10.values,
    colLabels=top10.columns,
    cellLoc="center",
    loc="center"
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(9)
tbl.scale(1, 1.5)
plt.title("Top 10 Merchants by Transaction Count (High-Risk Flag: chargeback_ratio > 1%)", pad=20)
plt.savefig("dashboard_details.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: dashboard_details.png")