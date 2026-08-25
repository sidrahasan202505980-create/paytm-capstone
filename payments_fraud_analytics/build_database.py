import sqlite3
import pandas as pd

# --- Step 1: Connect to (and create) the database file ---
conn = sqlite3.connect("paytm_payments.db")
cursor = conn.cursor()

# --- Step 2: Drop tables if they already exist (so we can re-run this script safely) ---
cursor.execute("DROP TABLE IF EXISTS transactions")
cursor.execute("DROP TABLE IF EXISTS merchants")
cursor.execute("DROP TABLE IF EXISTS users")

# --- Step 3: Create the merchants table ---
cursor.execute("""
CREATE TABLE merchants (
    merchant_id INTEGER PRIMARY KEY,
    merchant_name TEXT,
    category TEXT,
    region TEXT
)
""")

# --- Step 4: Create the users table ---
cursor.execute("""
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    signup_date TEXT
)
""")

# --- Step 5: Create the transactions table, with foreign keys ---
cursor.execute("""
CREATE TABLE transactions (
    transaction_id TEXT PRIMARY KEY,
    user_id INTEGER,
    merchant_id INTEGER,
    transaction_time TEXT,
    amount_inr INTEGER,
    payment_method TEXT,
    status TEXT,
    risk_score INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id)
)
""")

conn.commit()

# --- Step 6: Load the CSVs with pandas ---
merchants_df = pd.read_csv("merchants.csv")
users_df = pd.read_csv("users.csv")
ledger_df = pd.read_csv("ledger.csv")

# --- Step 7: Push each DataFrame into its matching SQL table ---
merchants_df.to_sql("merchants", conn, if_exists="append", index=False)
users_df.to_sql("users", conn, if_exists="append", index=False)
ledger_df.to_sql("transactions", conn, if_exists="append", index=False)

conn.commit()

# --- Step 8: Quick sanity check ---
for table in ["merchants", "users", "transactions"]:
    count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table}: {count} rows")

conn.close()
print("Database built successfully: paytm_payments.db")