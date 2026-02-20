import pandas as pd
import random
from datetime import datetime, timedelta

rows = []
tx_id = 0
now = datetime.now()

def add_tx(s, r, amt, time):
    global tx_id
    rows.append([tx_id, s, r, amt, time])
    tx_id += 1

# 1. GENERATE 10 DIFFERENT CYCLES (RING_001 to RING_010)
# This will trigger your calculate_scores cycle detection (Length 3-5)
for r in range(10):
    size = random.randint(3, 5)
    cycle_nodes = [f"RING_{r}_NODE_{i}" for i in range(size)]
    for i in range(size):
        add_tx(cycle_nodes[i], cycle_nodes[(i + 1) % size], random.randint(500, 2000), now)

# 2. GENERATE MASSIVE FAN-IN (Mule Aggregation)
# Triggers in_deg >= 10 logic
aggregator_nodes = ["BIG_BOSS_IN_1", "BIG_BOSS_IN_2"]
for boss in aggregator_nodes:
    for i in range(25):
        add_tx(f"MULE_SENDER_{i}_{boss}", boss, random.randint(100, 500), now - timedelta(minutes=i*10))

# 3. GENERATE MASSIVE FAN-OUT (Layering/Dispersal)
# Triggers out_deg >= 10 logic
disperser_nodes = ["LAUNDRY_OUT_1", "LAUNDRY_OUT_2"]
for boss in disperser_nodes:
    for i in range(25):
        add_tx(boss, f"MULE_RECV_{i}_{boss}", random.randint(100, 500), now - timedelta(minutes=i*10))

# 4. GENERATE 5 DEEP SHELL CHAINS (Chain length 5)
# Triggers your shortest_path >= 4 logic (Money Laundering Layers)
for c in range(5):
    for i in range(5):
        add_tx(f"CHAIN_{c}_STEP_{i}", f"CHAIN_{c}_STEP_{i+1}", 5000, now - timedelta(hours=i))

# 5. GENERATE HIGH VELOCITY NODES
# Triggers the len(transactions) >= 5 within 72h window
for h in range(10):
    v_node = f"VELOCITY_NODE_{h}"
    for i in range(8):
        add_tx(v_node, f"TARGET_{i}_{h}", 200, now - timedelta(hours=i*2))

# 6. GENERATE "NOISY" NORMAL TRANSACTIONS (False Positive Mitigation test)
# Adding a "Normal" node with 200+ transactions to test your mitigation score (-20)
for i in range(210):
    add_tx("BIG_BANK_OFFICIAL", f"RECIPIENT_{i}", 50, now - timedelta(minutes=i))

# Create DataFrame
df = pd.DataFrame(rows, columns=["transaction_id", "sender_id", "receiver_id", "amount", "timestamp"])
df.to_csv("fintrace_stress_test.csv", index=False)

print(f"Stress test dataset created with {len(df)} transactions.")