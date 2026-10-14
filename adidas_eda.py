"""
Adidas US Sales - data cleaning and exploratory data analysis (EDA).

Usage:
    python adidas_eda.py Adidas_US_Sales_Datasets.xlsx

Reads the raw workbook, cleans it, prints the EDA tables used in the README
and saves them as CSV files in ./eda_tables/ (no charts are produced).
Requires: pandas, numpy, openpyxl
"""
import sys
from pathlib import Path

import pandas as pd

SRC = sys.argv[1] if len(sys.argv) > 1 else "Adidas_US_Sales_Datasets.xlsx"
OUT = Path("eda_tables")
OUT.mkdir(exist_ok=True)
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 30)


# ---------------------------------------------------------------- 1. LOAD + CLEAN
raw = pd.read_excel(SRC, header=4, usecols="B:N")  # title block sits above row 5
print(f"Raw rows: {len(raw):,}")

for col in ["Retailer", "Region", "State", "City", "Product", "Sales Method"]:
    raw[col] = raw[col].astype(str).str.strip()
raw["Retailer ID"] = raw["Retailer ID"].astype(str)  # identifier, not a number
raw["Invoice Date"] = pd.to_datetime(raw["Invoice Date"])

print("Missing values:", int(raw.isna().sum().sum()))
print("Exact duplicate rows:", int(raw.duplicated().sum()))

zero_units = raw["Units Sold"] <= 0
print("Rows with zero units (removed):", int(zero_units.sum()))
df = raw[~zero_units].drop_duplicates().reset_index(drop=True)

# Total Sales vs Price x Units check
df["Calc Sales"] = df["Price per Unit"] * df["Units Sold"]
df["Scale Flag"] = (df["Total Sales"] - df["Calc Sales"]).abs() > 1
print("Rows where Total Sales != Price x Units (exactly 10x):", int(df["Scale Flag"].sum()))
print("Rows where Profit != Sales x Margin:",
      int(((df["Total Sales"] * df["Operating Margin"] - df["Operating Profit"]).abs() > 0.01).sum()))

# Assumption: Units Sold is understated 10x in flagged rows
df["Units Adjusted"] = (df["Total Sales"] / df["Price per Unit"]).round()

df["Year"] = df["Invoice Date"].dt.year
df["Month"] = df["Invoice Date"].dt.month
df["Quarter"] = "Q" + df["Invoice Date"].dt.quarter.astype(str)
df["Weekday"] = df["Invoice Date"].dt.day_name()
print(f"Clean rows: {len(df):,}\n")


# ---------------------------------------------------------------- 2. HELPERS
def summarise(by):
    t = df.groupby(by).agg(
        Sales=("Total Sales", "sum"),
        Profit=("Operating Profit", "sum"),
        Units=("Units Adjusted", "sum"),
        Transactions=("Total Sales", "size"),
    )
    t["Margin %"] = t["Profit"] / t["Sales"] * 100
    t["Sales Share %"] = t["Sales"] / t["Sales"].sum() * 100
    t["Profit Share %"] = t["Profit"] / t["Profit"].sum() * 100
    t["Avg Sale per Txn"] = t["Sales"] / t["Transactions"]
    return t.sort_values("Sales", ascending=False).round(2)


def show(title, table, name):
    print(f"=== {title} ===")
    print(table.to_string(), "\n")
    table.to_csv(OUT / f"{name}.csv")


# ---------------------------------------------------------------- 3. EDA
show("Descriptive statistics",
     df[["Price per Unit", "Units Adjusted", "Total Sales",
         "Operating Profit", "Operating Margin"]].describe().round(2), "describe")
print("Skewness:\n", df[["Price per Unit", "Units Adjusted", "Total Sales",
                         "Operating Profit", "Operating Margin"]].skew().round(2), "\n")
show("Correlation matrix",
     df[["Price per Unit", "Units Adjusted", "Total Sales",
         "Operating Profit", "Operating Margin"]].corr().round(2), "correlation")

for dim in ["Retailer", "Region", "Product", "Sales Method", "Year", "Quarter", "Weekday"]:
    show(f"By {dim}", summarise(dim), f"by_{dim.lower().replace(' ', '_')}")

states = summarise("State")
show("By State", states, "by_state")
print("States needed for 80% of sales:",
      int((states["Sales"].cumsum() / states["Sales"].sum() < 0.8).sum() + 1), "of", len(states), "\n")

# City names repeat across states (e.g. Portland, Charleston) -> key on State + City
show("Top 10 State + City", summarise(["State", "City"]).head(10), "top_cities")

monthly = df.groupby(["Year", "Month"]).agg(
    Sales=("Total Sales", "sum"), Profit=("Operating Profit", "sum"),
    Transactions=("Total Sales", "size"))
monthly["Margin %"] = monthly["Profit"] / monthly["Sales"] * 100
show("Monthly trend", monthly.round(1), "monthly_trend")

# Cross-tabs
def margin_pivot(index, columns):
    p = df.pivot_table(index=index, columns=columns,
                       values=["Operating Profit", "Total Sales"], aggfunc="sum")
    return (p["Operating Profit"] / p["Total Sales"] * 100).round(1)

show("Retailer x Sales Method - Sales",
     df.pivot_table(index="Retailer", columns="Sales Method", values="Total Sales", aggfunc="sum").round(0),
     "retailer_x_method_sales")
show("Retailer x Sales Method - Margin %", margin_pivot("Retailer", "Sales Method"),
     "retailer_x_method_margin")
show("Region x Sales Method - Sales",
     df.pivot_table(index="Region", columns="Sales Method", values="Total Sales", aggfunc="sum").round(0),
     "region_x_method_sales")
show("Region x Product - Margin %", margin_pivot("Region", "Product"), "region_x_product_margin")
show("Product x Sales Method - Margin %", margin_pivot("Product", "Sales Method"),
     "product_x_method_margin")
show("Retailer x Year - Transactions",
     df.pivot_table(index="Retailer", columns="Year", values="Total Sales", aggfunc="size"),
     "retailer_x_year_txns")

# Outliers (IQR rule) - retained, they are genuine bulk/in-store transactions
print("=== IQR outlier counts ===")
for col in ["Total Sales", "Operating Profit", "Operating Margin", "Price per Unit"]:
    q1, q3 = df[col].quantile([0.25, 0.75])
    iqr = q3 - q1
    n = int(((df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)).sum())
    print(f"{col}: {n}")

# Sensitivity: what if Total Sales is the wrong field (use Price x Units)?
print("\n=== Sensitivity: sales recomputed as Price x Units ===")
alt = df.groupby("Sales Method")[["Total Sales", "Calc Sales"]].sum()
alt["Rank (original)"] = alt["Total Sales"].rank(ascending=False)
alt["Rank (recomputed)"] = alt["Calc Sales"].rank(ascending=False)
print(alt.round(0).to_string())
print("Total (original):", f"{df['Total Sales'].sum():,.0f}",
      "| Total (recomputed):", f"{df['Calc Sales'].sum():,.0f}")
