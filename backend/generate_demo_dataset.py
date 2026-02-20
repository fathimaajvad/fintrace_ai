import pandas as pd
from datetime import datetime, timedelta

rows = []
transaction_id = 0
now = datetime.now()

# -----------------------
# 1. Cycle Pattern (A → B → C → A)
# -----------------------
cycle_accounts = ["CYCLE_A", "CYCLE_B", "CYCLE_C"]

rows.append([transaction_id, "CYCLE_A", "CYCLE_B", 500, now]); transaction_id += 1
rows.append([transaction_id, "CYCLE_B", "CYCLE_C", 600, now]); transaction_id += 1
rows.append([transaction_id, "CYCLE_C", "CYCLE_A", 700, now]); transaction_id += 1

# -----------------------
# 2. Fan-in Pattern (10 senders → AGGREGATOR)
# -----------------------
for i in range(10):
    rows.append([
        transaction_id,
        f"SENDER_{i}",
        "AGGREGATOR",
        100 + i,
        now - timedelta(hours=i)
    ])
    transaction_id += 1

# -----------------------
# 3. Fan-out Pattern (DISPERSER → 10 receivers)
# -----------------------
for i in range(10):
    rows.append([
        transaction_id,
        "DISPERSER",
        f"RECEIVER_{i}",
        200 + i,
        now - timedelta(hours=i)
    ])
    transaction_id += 1

# -----------------------
# 4. Shell Chain (LAYER1 → LAYER2 → LAYER3 → LAYER4)
# -----------------------
rows.append([transaction_id, "LAYER1", "LAYER2", 1000, now]); transaction_id += 1
rows.append([transaction_id, "LAYER2", "LAYER3", 1000, now]); transaction_id += 1
rows.append([transaction_id, "LAYER3", "LAYER4", 1000, now]); transaction_id += 1

# -----------------------
# 5. High Velocity (5 fast transactions within 72 hours)
# -----------------------
for i in range(5):
    rows.append([
        transaction_id,
        "FAST_NODE",
        f"FAST_TARGET_{i}",
        300,
        now - timedelta(hours=i)
    ])
    transaction_id += 1

df = pd.DataFrame(rows, columns=[
    "transaction_id",
    "sender_id",
    "receiver_id",
    "amount",
    "timestamp"
])

df.to_csv("demo_dataset.csv", index=False)

print("Demo dataset created: demo_dataset.csv")