# Part 1 — Payments & Fraud Analytics

## Design Decisions

- **Fee-tier assumptions (HLOOKUP table):** UPI 0.3%, Wallet 0.5%, Card 1.5%, Netbanking 0.9% — illustrative MDR percentages, with Card set highest and UPI lowest to reflect typical real-world processing cost differences.
- **Classification cutoff:** A transaction is labeled "High-Value Merchant Day" when a merchant's total transaction amount for that day exceeds INR 5,000 AND the merchant's region is not "East" (exact rule as specified in the brief).
- **Chart choices:** Used matplotlib for all four dashboard layers, saved as static PNG images per the brief's requirement (no live BI tool dependency).

## Dashboard Interpretations

### Headline Layer
Our platform processed ₹290,382 in GMV with a success rate of 85.56%, which is a solid performance for a payments platform. However, the 90.49% match rate shows that roughly 10% of transactions have a discrepancy between our internal ledger and the payment gateway export — this gap is large enough to need investigation rather than being dismissed as routine noise. The chargeback ratio of 5.12% is notably elevated compared to typical healthy payments platforms (which usually stay under 1%), suggesting there may be a meaningful fraud problem worth investigating further.

### Trends Layer
Daily GMV fluctuates significantly across the month, ranging from around ₹4,000 to over ₹22,000, with no strong weekly pattern visible. Chargebacks do not appear to track GMV — the two highest GMV days (Jan 4-5 and Jan 12) actually have almost no chargebacks, while the largest chargeback spike (Jan 22-23, reaching 4 in a day) occurs during a period of comparatively lower GMV. This suggests chargeback/fraud activity is driven by factors independent of overall transaction volume, meaning a simple "watch the busy days" fraud strategy wouldn't be sufficient — fraud monitoring needs to run consistently regardless of daily GMV levels.

### Breakdown Layer
UPI generates the highest GMV by payment method, which aligns with the seed data's 55% transaction-method weighting toward UPI — more than double any other method's share. By category, Travel generates the highest GMV, even though categories were assigned randomly to merchants with no built-in weighting; this is likely explained by travel merchants processing a mix of higher-value transactions rather than a deliberate business pattern. This suggests that if Paytm wanted to prioritize payment-method infrastructure investment, UPI reliability would matter most given its outsized share of GMV.

### Details Layer
Surprisingly, 7 of the top 10 highest-volume merchants are flagged as high-risk (chargeback ratio exceeding 1%) — intuitively, one might expect busier, more established merchants to be safer rather than riskier. However, this is likely an artifact of the 1% threshold being quite sensitive for merchants with relatively low total transaction counts: since fraud (like the seeded burner-account chargebacks) is assigned randomly and independent of merchant popularity, even one or two chargebacks can push a merchant's ratio above 1% if their total transaction count is small. This suggests the 1% threshold may need to be paired with a minimum transaction-count requirement in a real deployment, so a merchant isn't unfairly flagged based on statistical noise from a small sample.

## How to Run This Part

1. `cd payments_fraud_analytics`
2. `python generate_data.py` — creates merchants.csv, users.csv, ledger.csv, gateway_export.csv
3. `python build_database.py` — builds paytm_payments.db from the CSVs
4. `python fraud_queries.py` — runs and prints all 6 SQL fraud-detection queries
5. `python reconcile.py` — runs the reconciliation function, prints discrepancy counts
6. `python dashboard.py` — generates dashboard_trends.png, dashboard_breakdown.png, dashboard_details.png
7. Open `merchant_workbook.xlsx` in Excel/Google Sheets to view the VLOOKUP/HLOOKUP/pivot table work