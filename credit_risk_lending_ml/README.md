# Part 2 — Credit Risk & Lending ML

## Task 1 — EDA & Preprocessing
- Measured default rate: 20.25% (0.2025)
- Missing credit_bureau_score %: 20.00%
- is_thin_file flag: engineered directly from raw data (credit_bureau_score.isna()), no rows dropped



## Task 2 — Train/Test Split & Preprocessing
- Split: 75/25, stratified on default, random_state=42 (300 training rows / 100 test rows)
- Thin-file flag engineered first (safe pre-split, no fitted statistic involved)
- Median used for imputation (computed from training split only): 612.0 — applied to fill missing values in both training and test splits
- Encoding: one-hot encoding for employment_type (fit independently on train and test, test columns reindexed to match train)
- Scaling: StandardScaler, fit only on training split, then applied to both training and test splits



## Task 3 & 4 — Model Training & Evaluation

Both models trained on the identical 75/25 stratified split (random_state=42).

| Metric    | Logistic Regression | Decision Tree |
|-----------|---------------------|----------------|
| Accuracy  | 0.76                | 0.67           |
| Precision | 0.39                | 0.24           |
| Recall    | 0.35                | 0.30           |
| F1 Score  | 0.37                | 0.27           |
| ROC-AUC   | 0.72                | 0.53           |

Confusion Matrix — Logistic Regression: [[69, 11], [13, 7]]
Confusion Matrix — Decision Tree: [[61, 19], [14, 6]]



## Task 5 — Risk-Based Pricing Table

Applicants bucketed into 4 quartile-based risk tiers using Logistic Regression's predicted default probability on the test set. Observed default rate increases monotonically from Tier 1 to Tier 4, confirming the model's risk ranking holds up against real outcomes.

| Risk Tier              | # Applicants | Observed Default Rate | Assigned Interest Rate |
|-------------------------|--------------|------------------------|--------------------------|
| Tier 1 (Low Risk)        | 25           | 8%                    | 14%                      |
| Tier 2 (Medium)          | 25           | 12%                   | 20%                      |
| Tier 3 (High)            | 25           | 20%                   | 28%                      |
| Tier 4 (Very High)       | 25           | 40%                   | 36%                      |



## Task 6 & 7 — Anomaly Detection

Isolation Forest trained on standardized txn_hour, is_new_device, and txn_amount_inr from txn_behaviour.csv (265 rows), with contamination rate set to 15/265 ≈ 5.66% to match the known seeded anomaly proportion. The model flagged 15 transactions as anomalous.

Ground truth (txn_id starting with "BTXNA") shows 15 true seeded anomalies. Isolation Forest recall against seeded anomalies: 11/15 = 73.33%.



## Task 8 — Bias-Awareness Note

This dataset contains no explicit gender, caste, religion, or location field, so on the surface it looks free of protected-attribute bias. However, the absence of a direct field does not guarantee fairness, because other variables can act as indirect proxies that correlate with a protected attribute even without naming it.

The clearest risk in this dataset is credit_bureau_score. A bureau score is not a neutral, purely individual measure of trustworthiness — it reflects a person's history of formal access to banking and credit products. In India, access to formal credit has historically been uneven across regions, castes, and communities, often due to factors like rural vs. urban banking infrastructure, generational wealth, or prior systemic exclusion, rather than an individual's actual creditworthiness. If the model treats a low or missing bureau score as straightforwardly "risky," it risks penalizing applicants for a historical access gap they did not create, rather than for their genuine ability to repay.

This risk becomes concrete in the is_thin_file population: 20% of applicants in this dataset have no bureau score at all. If the model, or any imputation strategy, systematically treats "no score" as equivalent to "high risk," it would disproportionately disadvantage applicants who are simply new to formal credit — exactly the population Paytm Postpad is trying to serve with alternate-data signals like UPI inflow. Denying them credit or charging them punitively high rates on this basis would not be an individual underwriting decision, but a systemic one, and could indirectly reproduce existing inequities in access to formal banking.

As a governance safeguard, I recommend a maker-checker human-in-the-loop review specifically for the is_thin_file segment: any applicant with a missing credit_bureau_score who the model recommends rejecting should be automatically routed to a human loan officer for manual review before a final decision is made, rather than being auto-declined. This ensures that the population most exposed to proxy risk is not harmed by an automated decision alone, while still allowing the model to operate normally for applicants with an established credit history.



## Task 9 — Final Model Comparison & Recommendation

| Metric    | Logistic Regression | Decision Tree |
|-----------|---------------------|----------------|
| Accuracy  | 0.76                | 0.67           |
| Precision | 0.39                | 0.24           |
| Recall    | 0.35                | 0.30           |
| F1 Score  | 0.37                | 0.27           |
| ROC-AUC   | 0.72                | 0.53           |

Isolation Forest recall on seeded fraud anomalies: 11/15 = 73.33%

**Recommendation:** 
Paytm Postpad should deploy the Logistic Regression model, not the Decision Tree. Logistic Regression outperforms the Decision Tree on every evaluation metric, most notably ROC-AUC (0.72 vs. 0.53), meaning it ranks risky vs. safe applicants far more reliably — the Decision Tree's 0.53 is barely better than random guessing. This gap likely stems from the Decision Tree overfitting: trained without a depth limit on only 300 rows, it memorized noise in the training data rather than learning generalizable patterns. While Decision Trees are often assumed to be more interpretable, an unrestricted, deeply-nested tree like this one is not actually easy to explain to a regulator or applicant, whereas Logistic Regression's per-feature coefficients offer a genuinely transparent, auditable basis for a credit decision. For these reasons — both stronger predictive performance and clearer explainability — Logistic Regression is the appropriate model to deploy for Paytm Postpad's risk-based pricing.