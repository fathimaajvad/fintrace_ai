import networkx as nx
import pandas as pd
from collections import defaultdict

def calculate_scores(G, df):

    account_scores = defaultdict(lambda: {
        "score": 0,
        "patterns": set(),
        "ring_id": None
    })

    fraud_rings = []
    ring_counter = 1

    # -------- 1. Cycle Detection (Length 3–5) --------
    cycles = list(nx.simple_cycles(G))

    for cycle in cycles:
        if 3 <= len(cycle) <= 5:
            ring_id = f"RING_{ring_counter:03d}"
            ring_counter += 1

            for node in cycle:
                account_scores[node]["score"] += 40
                account_scores[node]["patterns"].add(f"cycle_length_{len(cycle)}")
                account_scores[node]["ring_id"] = ring_id

            fraud_rings.append({
                "ring_id": ring_id,
                "member_accounts": cycle,
                "pattern_type": "cycle",
                "risk_score": 90.0
            })

    # -------- 2. Fan-in / Fan-out Detection --------
    for node in G.nodes:
        in_deg = G.in_degree(node)
        out_deg = G.out_degree(node)

        if in_deg >= 10:
            account_scores[node]["score"] += 25
            account_scores[node]["patterns"].add("fan_in")

        if out_deg >= 10:
            account_scores[node]["score"] += 25
            account_scores[node]["patterns"].add("fan_out")

    # -------- 3. High Velocity Detection (72h Window) --------
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    for account in G.nodes:
        transactions = df[
            (df["sender_id"] == account) |
            (df["receiver_id"] == account)
        ].sort_values("timestamp")

        if len(transactions) >= 5:
            time_diff = (
                transactions["timestamp"].max() -
                transactions["timestamp"].min()
            ).total_seconds() / 3600

            if time_diff <= 72:
                account_scores[account]["score"] += 15
                account_scores[account]["patterns"].add("high_velocity")

    # -------- 4. Shell Chain Detection (Protected for Performance) --------
    if len(G.nodes) < 300:
        for source in G.nodes:
            for target in G.nodes:
                if source != target:
                    try:
                        path = nx.shortest_path(G, source, target)

                        if len(path) >= 4:  # 3+ hops
                            intermediate_nodes = path[1:-1]

                            for node in intermediate_nodes:
                                if G.degree(node) <= 3:
                                    if "shell_chain" not in account_scores[node]["patterns"]:
                                        account_scores[node]["score"] += 20
                                        account_scores[node]["patterns"].add("shell_chain")

                    except nx.NetworkXNoPath:
                        continue

    # -------- 5. False Positive Mitigation --------
    for account in account_scores:
        total_transactions = len(df[
            (df["sender_id"] == account) |
            (df["receiver_id"] == account)
        ])

        if total_transactions > 200:
            account_scores[account]["score"] -= 20

        if account_scores[account]["score"] < 0:
            account_scores[account]["score"] = 0

    # -------- 6. Build Suspicious Accounts List --------
    suspicious_accounts = []

    for account, data in account_scores.items():
        score = min(data["score"], 100)

        if score > 0:
            suspicious_accounts.append({
                "account_id": account,
                "suspicion_score": float(score),
                "detected_patterns": list(data["patterns"]),
                "ring_id": data["ring_id"] if data["ring_id"] else "NONE"
            })

    suspicious_accounts.sort(
        key=lambda x: x["suspicion_score"],
        reverse=True
    )

    return suspicious_accounts, fraud_rings
