import pandas as pd

# Load Kaggle dataset
df = pd.read_csv("ML.csv", sep=",", engine="python")

# Rename columns to match backend schema
df_new = pd.DataFrame({
    "transaction_id": range(len(df)),
    "sender_id": df["sourceid"].astype(str),
    "receiver_id": df["destinationid"].astype(str),
    "amount": df["amountofmoney"],
    "timestamp": df["date"]
})

df_new.to_csv("converted_transactions.csv", index=False)

print("Converted dataset saved as converted_transactions.csv")

