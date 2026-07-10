import pandas as pd

# =====================================================
# Load combined datasets
# =====================================================

sold = pd.read_csv(
    '/Users/morganstevenson/Desktop/IDX/week2/res_sold.csv',
    parse_dates=["CloseDate"]
)

listings = pd.read_csv(
    '/Users/morganstevenson/Desktop/IDX/week2/res_listing.csv',
    parse_dates=["ListingContractDate"]
)

# =====================================================
# Step 1 - Fetch mortgage rate data from FRED
# =====================================================
import ssl
import certifi

ssl_context = ssl.create_default_context(cafile=certifi.where())

import urllib.request

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"

with urllib.request.urlopen(url, context=ssl_context) as response:
    mortgage = pd.read_csv(response, parse_dates=["observation_date"])


mortgage.columns = ["date", "rate_30yr_fixed"]

# Ensure mortgage rate is numeric
mortgage["rate_30yr_fixed"] = pd.to_numeric(
    mortgage["rate_30yr_fixed"],
    errors="coerce"
)

# =====================================================
# Step 2 - Convert weekly data to monthly averages
# =====================================================

mortgage["year_month"] = mortgage["date"].dt.to_period("M")

mortgage_monthly = (
    mortgage.groupby("year_month", as_index=False)
    ["rate_30yr_fixed"]
    .mean()
)

# =====================================================
# Step 3 - Create matching year_month keys
# =====================================================

sold["year_month"] = sold["CloseDate"].dt.to_period("M")

listings["year_month"] = (
    listings["ListingContractDate"]
    .dt.to_period("M")
)

# =====================================================
# Step 4 - Merge mortgage rates
# =====================================================

sold_with_rates = sold.merge(
    mortgage_monthly,
    on="year_month",
    how="left"
)

listings_with_rates = listings.merge(
    mortgage_monthly,
    on="year_month",
    how="left"
)

# =====================================================
# Step 5 - Validate merge
# =====================================================

sold_missing = sold_with_rates["rate_30yr_fixed"].isna().sum()
listing_missing = listings_with_rates["rate_30yr_fixed"].isna().sum()

print(f"Missing mortgage rates in sold dataset: {sold_missing}")
print(f"Missing mortgage rates in listings dataset: {listing_missing}")

if sold_missing == 0:
    print("✓ Sold dataset merged successfully.")

if listing_missing == 0:
    print("✓ Listings dataset merged successfully.")

# =====================================================
# Preview
# =====================================================

print("\nSold Preview:")
print(
    sold_with_rates[
        [
            "CloseDate",
            "year_month",
            "ClosePrice",
            "rate_30yr_fixed",
        ]
    ].head()
)

print("\nListings Preview:")
print(
    listings_with_rates[
        [
            "ListingContractDate",
            "year_month",
            "ListPrice",
            "rate_30yr_fixed",
        ]
    ].head()
)

# =====================================================
# Save enriched datasets
# =====================================================

import os

script_dir = os.path.dirname(os.path.abspath(__file__))

sold_with_rates.to_csv(
    os.path.join(script_dir, "combined_sold_with_mortgage_rates.csv"),
    index=False
)

listings_with_rates.to_csv(
    os.path.join(script_dir, "combined_listings_with_mortgage_rates.csv"),
    index=False
)
print("\nEnriched datasets saved successfully.")