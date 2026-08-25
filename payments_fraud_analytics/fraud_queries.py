import sqlite3
import pandas as pd

conn = sqlite3.connect("paytm_payments.db")

print("=" * 60)
print("QUERY 1: Distinct payment methods used in high-risk transactions")
print("=" * 60)

query1 = """
SELECT DISTINCT payment_method
FROM transactions
WHERE risk_score > 70
ORDER BY payment_method
LIMIT 10
"""
result1 = pd.read_sql_query(query1, conn)
print(result1)



print("\n" + "=" * 60)
print("QUERY 2: Chargeback impact summary")
print("=" * 60)

query2 = """
SELECT
    COUNT(*) AS chargeback_count,
    COUNT(DISTINCT user_id) AS unique_users_affected,
    SUM(amount_inr) AS total_chargeback_amount
FROM transactions
WHERE status = 'chargeback'
"""
result2 = pd.read_sql_query(query2, conn)
print(result2)



print("\n" + "=" * 60)
print("QUERY 3: Burner account detection (seeded target: 15 rows)")
print("=" * 60)

query3 = """
SELECT
    t.transaction_id,
    t.user_id,
    u.signup_date,
    t.transaction_time,
    t.amount_inr,
    t.status,
    julianday(t.transaction_time) - julianday(u.signup_date) AS days_since_signup
FROM transactions t
INNER JOIN users u ON t.user_id = u.user_id
WHERE t.status = 'chargeback'
    AND (julianday(t.transaction_time) - julianday(u.signup_date)) >= 0
    AND (julianday(t.transaction_time) - julianday(u.signup_date)) < 30
ORDER BY days_since_signup
"""
result3 = pd.read_sql_query(query3, conn)
print(result3)
print(f"\nTotal burner-account rows found: {len(result3)}")



print("\n" + "=" * 60)
print("QUERY 4: Velocity attack detection (seeded target: 8 clusters)")
print("=" * 60)

query4 = """
SELECT
    user_id,
    strftime('%Y-%m-%d %H:', transaction_time) ||
        printf('%02d', (CAST(strftime('%M', transaction_time) AS INTEGER) / 10) * 10) ||
        ':00' AS time_bucket,
    COUNT(*) AS txn_count_in_window
FROM transactions
GROUP BY user_id, time_bucket
HAVING COUNT(*) >= 3
ORDER BY user_id, time_bucket
"""
result4 = pd.read_sql_query(query4, conn)
print(result4)
print(f"\nTotal velocity-attack clusters found: {len(result4)}")



print("\n" + "=" * 60)
print("QUERY 5: All merchants with their chargeback counts (LEFT JOIN)")
print("=" * 60)

query5 = """
SELECT
    m.merchant_id,
    m.merchant_name,
    COUNT(t.transaction_id) AS chargeback_count
FROM merchants m
LEFT JOIN transactions t
    ON m.merchant_id = t.merchant_id AND t.status = 'chargeback'
GROUP BY m.merchant_id, m.merchant_name
ORDER BY chargeback_count DESC
LIMIT 15
"""
result5 = pd.read_sql_query(query5, conn)
print(result5)


print("\n" + "=" * 60)
print("QUERY 6: Total GMV by merchant category")
print("=" * 60)

query6 = """
SELECT
    m.category,
    COUNT(t.transaction_id) AS txn_count,
    SUM(t.amount_inr) AS total_gmv_inr
FROM transactions t
INNER JOIN merchants m ON t.merchant_id = m.merchant_id
WHERE t.status = 'captured'
GROUP BY m.category
ORDER BY total_gmv_inr DESC
"""
result6 = pd.read_sql_query(query6, conn)
print(result6)

conn.close()