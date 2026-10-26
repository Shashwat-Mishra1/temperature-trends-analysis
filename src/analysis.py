import os
import pandas as pd
import matplotlib.pyplot as plt

# Define project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "temperature_data.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Create output directory automatically
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_FILE)

# Clean column names
df.columns = df.columns.str.strip()

# Check required columns
required_columns = ["State", "City", "Temperature", "Date", "Time", "Year", "Month"]

missing_columns = [column for column in required_columns if column not in df.columns]

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

# Convert temperature to numeric values
df["Temperature"] = pd.to_numeric(df["Temperature"], errors="coerce")
df = df.dropna(subset=["Temperature"])

if df.empty:
    raise ValueError("The dataset contains no valid temperature values.")

# Display dataset information
print("=" * 50)
print("TEMPERATURE TRENDS ANALYSIS")
print("=" * 50)

print("\nDataset dimensions:")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\nBasic temperature statistics:")
print(df["Temperature"].describe())

# Average temperature by state
print("\nAverage temperature by state:")
state_average = df.groupby("State")["Temperature"].mean().sort_values(ascending=False)
print(state_average.round(2))

# Highest temperature record
print("\nHighest temperature record:")
print(df.loc[df["Temperature"].idxmax()])

# Lowest temperature record
print("\nLowest temperature record:")
print(df.loc[df["Temperature"].idxmin()])

# Average temperature by month
month_order = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

df["Month"] = df["Month"].astype(str).str.strip().str.capitalize()

df["Month"] = pd.Categorical(
    df["Month"],
    categories=month_order,
    ordered=True
)

monthly_average = df.groupby("Month", observed=False)["Temperature"].mean()
monthly_average = monthly_average.dropna()

print("\nAverage temperature by month:")
print(monthly_average.round(2))

# Generate monthly temperature trend chart
if not monthly_average.empty:
    plt.figure(figsize=(12, 6))
    monthly_average.plot(kind="line", marker="o")

    plt.title("Average Temperature Trend by Month")
    plt.xlabel("Month")
    plt.ylabel("Average Temperature")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    chart_path = os.path.join(OUTPUT_DIR, "temperature_trend.png")
    plt.savefig(chart_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\nChart saved successfully: {chart_path}")
else:
    print("\nNo valid monthly data was available to generate a chart.")

print("\nAnalysis completed successfully.")
