import pandas as pd
import matplotlib.pyplot as plt

# Create sample raw dataset
data = {
    "Customer_ID": [
        "C001", "C002", "C003", "C004", "C005",
        "C006", "C007", "C008", "C009", "C010",
        "C010"
    ],
    "Name": [
        "Arun", "Priya", "Kavin", "Divya", "Rahul",
        "Meena", "Vijay", "Anu", "Suresh", "Karthik",
        "Karthik"
    ],
    "Age": [
        25, 30, None, 28, 35,
        42, 29, None, 31, 27, 27
    ],
    "City": [
        "Chennai", "chennai", "Madurai", "Chennai", "Trichy",
        "Madurai", "chennai", "Trichy", None, "Chennai",
        "Chennai"
    ],
    "Purchase_Amount": [
        1200, 1500, 1800, None, 2200,
        2500, 1750, 2000, 1600, 1900, 1900
    ]
}

df = pd.DataFrame(data)

print("RAW DATA")
print(df)

# Save raw data
df.to_csv("raw_customer_data.csv", index=False)

# -------------------------
# DATA CLEANING
# -------------------------

# Remove duplicate records
duplicates_removed = df.duplicated().sum()
df = df.drop_duplicates()

# Handle missing Age using median
age_missing = df["Age"].isna().sum()
df["Age"] = df["Age"].fillna(df["Age"].median())

# Handle missing Purchase Amount using median
purchase_missing = df["Purchase_Amount"].isna().sum()
df["Purchase_Amount"] = df["Purchase_Amount"].fillna(
    df["Purchase_Amount"].median()
)

# Handle missing City
city_missing = df["City"].isna().sum()
df["City"] = df["City"].fillna("Unknown")

# Standardize city names
df["City"] = df["City"].str.strip().str.title()

# Convert columns to correct data types
df["Age"] = df["Age"].astype(int)
df["Purchase_Amount"] = df["Purchase_Amount"].astype(float)

# -------------------------
# REPORT GENERATION
# -------------------------

total_records = len(df)
total_purchase = df["Purchase_Amount"].sum()
average_purchase = df["Purchase_Amount"].mean()

report = pd.DataFrame({
    "Metric": [
        "Original Records",
        "Final Records",
        "Duplicates Removed",
        "Missing Age Values Handled",
        "Missing Purchase Values Handled",
        "Missing City Values Handled",
        "Total Purchase Amount",
        "Average Purchase Amount"
    ],
    "Value": [
        11,
        total_records,
        duplicates_removed,
        age_missing,
        purchase_missing,
        city_missing,
        round(total_purchase, 2),
        round(average_purchase, 2)
    ]
})

# Save cleaned data
df.to_csv("cleaned_customer_data.csv", index=False)

# Save automated Excel report
with pd.ExcelWriter("automated_data_cleaning_report.xlsx",
                    engine="openpyxl") as writer:

    df.to_excel(writer, sheet_name="Cleaned Data", index=False)
    report.to_excel(writer, sheet_name="Summary Report", index=False)

# -------------------------
# VISUAL SUMMARY
# -------------------------

city_sales = df.groupby("City")["Purchase_Amount"].sum()

plt.figure(figsize=(8, 5))
city_sales.plot(kind="bar")

plt.title("Purchase Amount by City")
plt.xlabel("City")
plt.ylabel("Total Purchase Amount")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("purchase_summary.png")
plt.close()

print("\nDATA CLEANING COMPLETED")
print("-----------------------")
print("Duplicates removed:", duplicates_removed)
print("Missing Age values handled:", age_missing)
print("Missing Purchase values handled:", purchase_missing)
print("Missing City values handled:", city_missing)

print("\nAUTOMATED REPORT GENERATED")
print("cleaned_customer_data.csv")
print("automated_data_cleaning_report.xlsx")
print("purchase_summary.png")