# ---------------------------
# 4. Query Firebase
# ---------------------------
data_snapshot = ref.get()

# Convert to DataFrame
records = []
if data_snapshot:
    for key, value in data_snapshot.items():
        records.append(value)

df = pd.DataFrame(records)

# ---------------------------
# 5. Clean Data
# ---------------------------
# Remove any rows with missing or non-numeric values
df = df.dropna()
df = df[pd.to_numeric(df['x'], errors='coerce').notnull()]
df = df[pd.to_numeric(df['y'], errors='coerce').notnull()]
df = df[pd.to_numeric(df['z'], errors='coerce').notnull()]

# Save to CSV
csv_filename = 'gyroscope_data.csv'
df.to_csv(csv_filename, index=False)
print(f"Data saved to {csv_filename}")
