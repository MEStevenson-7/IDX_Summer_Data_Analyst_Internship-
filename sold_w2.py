import pandas as pd

# =====================================================
# Load Data
# =====================================================

sold = pd.read_csv('/Users/morganstevenson/Desktop/IDX/res_sold.csv')

# =====================================================
# Unique Property Types
# =====================================================

print("="*60)
print("UNIQUE PROPERTY TYPES")
print("="*60)

print(sold["PropertyType"].dropna().unique())
print("\nCounts:")
print(sold["PropertyType"].value_counts(dropna=False))

# =====================================================
# Filtering Logic
# =====================================================

# Example filtering (modify as needed)
filtered = sold.copy()

# Remove rows with missing ClosePrice
filtered = filtered[filtered["ClosePrice"].notna()]

# Keep only positive prices
filtered = filtered[filtered["ClosePrice"] > 0]

# Remove impossible living areas
filtered = filtered[filtered["LivingArea"] > 0]

print("\n" + "="*60)
print("FILTERING LOGIC")
print("="*60)
print("1. Removed rows with missing ClosePrice.")
print("2. Removed properties with ClosePrice <= 0.")
print("3. Removed properties with LivingArea <= 0.")

print(f"\nOriginal observations: {len(listing)}")
print(f"Filtered observations: {len(filtered)}")

# =====================================================
# Null Count Summary
# =====================================================

print("\n" + "="*60)
print("NULL COUNT SUMMARY")
print("="*60)

null_summary = pd.DataFrame({
    "Null Count": filtered.isnull().sum(),
    "Percent Null": (filtered.isnull().mean()*100).round(2)
})

print(null_summary)

# =====================================================
# Missing Value Report (>90% Missing)
# =====================================================

print("\n" + "="*60)
print("COLUMNS WITH >90% MISSING VALUES")
print("="*60)

high_null = null_summary[null_summary["Percent Null"] > 90]

if len(high_null) == 0:
    print("No columns exceed 90% missing.")
else:
    print(high_null)

# =====================================================
# Numeric Distribution Summary
# =====================================================

summary_cols = [
    "ClosePrice",
    "LivingArea",
    "DaysOnMarket"
]

percentiles = [0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99]

print("\n" + "="*60)
print("NUMERIC DISTRIBUTION SUMMARY")
print("="*60)

for col in summary_cols:

    print(f"\n----- {col} -----")

    data = filtered[col].dropna()

    print(f"Minimum : {data.min():,.2f}")
    print(f"Maximum : {data.max():,.2f}")
    print(f"Mean    : {data.mean():,.2f}")
    print(f"Median  : {data.median():,.2f}")

    print("\nPercentiles:")
    print(data.quantile(percentiles))

# =====================================================
# Save Filtered Dataset
# =====================================================

filtered.to_csv("listing_filtered.csv", index=False)

print("\nFiltered dataset saved as 'listing_filtered.csv'.")