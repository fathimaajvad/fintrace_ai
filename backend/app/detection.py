import networkx as nx
from app.scoring import calculate_scores

def analyze_transactions(df):

    # -------- 1. Required Column Validation --------
    required_columns = [
        "transaction_id",
        "sender_id",
        "receiver_id",
        "amount",
        "timestamp"
    ]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # -------- 2. Graph Construction --------
    G = nx.DiGraph()

    for _, row in df.iterrows():
        G.add_edge(
            row["sender_id"],
            row["receiver_id"],
            amount=row["amount"],
            timestamp=row["timestamp"]
        )

    # -------- 3. Detection & Scoring --------
    suspicious_accounts, fraud_rings = calculate_scores(G, df)

    # -------- 4. Structured Result --------
    result = {
        "suspicious_accounts": suspicious_accounts,
        "fraud_rings": fraud_rings,
        "summary": {
            "total_accounts_analyzed": len(G.nodes),
            "suspicious_accounts_flagged": len(suspicious_accounts),
            "fraud_rings_detected": len(fraud_rings),
            "processing_time_seconds": 0
        }
    }

    return result
