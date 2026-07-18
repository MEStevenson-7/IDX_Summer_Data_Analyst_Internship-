# imports
import pandas as pd
import numpy as np

#helper functions
def valid_timeline(df, col1, col2):
    # True where the timeline is valid
    valid = df[col1] < df[col2]

    # Count invalid rows
    inval_time = (~valid).sum()

    # Keep only valid rows
    df = df[valid].copy()

    return df, inval_time

def clean_numeric_values(df):
    # Individual flags
    closeprice = df['ClosePrice'] <= 0
    livingarea = df['LivingArea'] <= 0
    days = df['DaysOnMarket'] < 0
    bedrooms = df['BedroomsTotal'] < 0
    bathrooms = df['BathroomsTotalInteger'] < 0

    # Any invalid numeric value
    invalid = closeprice | livingarea | days | bedrooms | bathrooms

    # Counts
    counts = {
        'ClosePrice <= 0': closeprice.sum(),
        'LivingArea <= 0': livingarea.sum(),
        'DaysOnMarket < 0': days.sum(),
        'BedroomsTotal < 0': bedrooms.sum(),
        'BathroomsTotalInteger < 0': bathrooms.sum(),
        'Total rows removed': invalid.sum()
    }

    # Remove invalid rows
    cleaned = df.loc[~invalid].copy()

    return cleaned, counts

def clean_coordinates(df, lat_col='Latitude', lon_col='Longitude'):
    # Individual flags
    missing = df[lat_col].isna() | df[lon_col].isna()
    zero = (df[lat_col] == 0) | (df[lon_col] == 0)
    positive_lon = df[lon_col] > 0

    # Approximate California bounding box
    out_of_state = (
        (df[lat_col] < 32.0) | (df[lat_col] > 42.1) |
        (df[lon_col] < -124.5) | (df[lon_col] > -114.0)
    )

    # Combine all flags
    invalid = missing | zero | positive_lon | out_of_state

    # Count each issue
    counts = {
        "Missing coordinates": missing.sum(),
        "Zero coordinates": zero.sum(),
        "Positive longitude": positive_lon.sum(),
        "Out of California": out_of_state.sum(),
        "Total rows removed": invalid.sum()
    }

    # Remove invalid rows
    cleaned = df.loc[~invalid].copy()

    return cleaned, counts

# Read in listings and sold files that were enriched in Week 3
listing = pd.read_csv('/Users/morganstevenson/Desktop/IDX/week2/combined_listings_with_mortgage_rates.csv')
sold = pd.read_csv('/Users/morganstevenson/Desktop/IDX/week2/combined_sold_with_mortgage_rates.csv')

#print before row counts
print(f"listings row counts before data cleaning steps: {listing.shape[0]}")
print(f"sold row counts before data cleaning steps: {sold.shape[0]}")

# Columns to be converted to date time
date_cols = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate']

# Apply pd.to_datetime across all specified columns for both listing and sold data frames
listing[date_cols] = listing[date_cols].apply(pd.to_datetime)
sold[date_cols] = sold[date_cols].apply(pd.to_datetime)


# •	Remove unnecessary or redundant columns, used .equals() to make sure columns had identical information (removed checks for readability)
keep = ['OriginalListPrice', 'ListingKey', 'CloseDate', 'ClosePrice', 'Latitude', 'Longitude',
       'UnparsedAddress', 'PropertyType', 'LivingArea', 'ListPrice',
       'DaysOnMarket', 'ListOfficeName', 'BuyerOfficeName', 'CoListOfficeName',
       'ListAgentFullName','BuyerAgentMlsId', 'BuyerAgentFirstName', 'BuyerAgentLastName',
       'FireplacesTotal', 'AssociationFeeFrequency', 'AboveGradeFinishedArea',
       'ListingKeyNumeric', 'MLSAreaMajor', 'TaxAnnualAmount',
       'CountyOrParish', 'MlsStatus', 'ElementarySchool', 'AttachedGarageYN', 'ParkingTotal',
       'BuilderName', 'PropertySubType', 'LotSizeAcres', 'SubdivisionName',
       'BuyerOfficeAOR', 'YearBuilt', 'StreetNumberNumeric', 'ListingId', 'BathroomsTotalInteger', 'City', 'TaxYear',
       'BuildingAreaTotal', 'BedroomsTotal', 'ContractStatusChangeDate', 'ElementarySchoolDistrict', 'CoBuyerAgentFirstName',
       'PurchaseContractDate', 'ListingContractDate', 'BelowGradeFinishedArea',
       'BusinessType', 'StateOrProvince', 'CoveredSpaces', 'MiddleOrJuniorSchool', 'FireplaceYN', 'Stories',
       'HighSchool', 'Levels', 'LotSizeDimensions', 'LotSizeArea', 'MainLevelBedrooms',
       'NewConstructionYN', 'GarageSpaces', 'HighSchoolDistrict', 'PostalCode', 'AssociationFee', 'LotSizeSquareFeet',
       'MiddleOrJuniorSchoolDistrict', 'ListAgentEmail',
       'BuyerAgencyCompensationType', 'BuyerAgencyCompensation', 'year_month',
       'rate_30yr_fixed']
listing = listing [keep]
sold = sold[keep]


# •	Handle missing values appropriately
# investigation of missing values with .isnull().sum() 
# getting rid of columns where more than 90% of values are null
lisitng = listing.loc[:, listing.isna().mean() < 0.9]
sold = sold.loc[:, listing.isna().mean() < 0.9]

#Getting rid of rows where more than 90% of entries are null
# Keep rows with at least 10% non-null values
listing = listing.dropna(thresh=int(0.1 * len(listing.columns)))
sold = sold.dropna(thresh=int(0.1 * len(sold.columns)))

# •	Ensure numeric fields are properly typed
# investigating dtype with .info()

listing['DaysOnMarket'] = listing['DaysOnMarket'].astype(int)
sold['DaysOnMarket'] = sold['DaysOnMarket'].astype(int)
listing['ParkingTotal'] = listing['ParkingTotal'].fillna(0).astype(int)
sold['ParkingTotal'] = sold['ParkingTotal'].fillna(0).astype(int)
listing['YearBuilt'] = listing['YearBuilt'].fillna(0).astype(int)
sold['YearBuilt'] = sold['YearBuilt'].fillna(0).astype(int)
listing['StreetNumberNumeric'] = listing['StreetNumberNumeric'].fillna(0).astype(int)
sold['StreetNumberNumeric'] = sold['StreetNumberNumeric'].fillna(0).astype(int)
listing['BathroomsTotalInteger'] = listing['BathroomsTotalInteger'].fillna(0).astype(int)
sold['BathroomsTotalInteger'] = sold['BathroomsTotalInteger'].fillna(0).astype(int)
listing['TaxYear'] = listing['TaxYear'].fillna(0).astype(int)
sold['TaxYear'] = sold['TaxYear'].fillna(0).astype(int)
listing['BedroomsTotal'] = listing['BedroomsTotal'].fillna(0).astype(int)
sold['BedroomsTotal'] = sold['BedroomsTotal'].fillna(0).astype(int)
listing['Stories'] = listing['Stories'].fillna(0).astype(int)
sold['Stories'] = sold['Stories'].fillna(0).astype(int)
listing['MainLevelBedrooms'] = listing['MainLevelBedrooms'].fillna(0).astype(int)
sold['MainLevelBedrooms'] = sold['MainLevelBedrooms'].fillna(0).astype(int)
listing['GarageSpaces'] = listing['GarageSpaces'].fillna(0).astype(int)
sold['GarageSpaces'] = sold['GarageSpaces'].fillna(0).astype(int)


#•	Remove or flag invalid numeric values: ClosePrice <= 0, LivingArea <= 0, DaysOnMarket < 0, negative Bedrooms or Bathrooms
listing, listing_numeric_counts = clean_numeric_values(listing)
sold, sold_numeric_counts = clean_numeric_values(sold)

print("Listing")
print(listing_numeric_counts)

print("\nSold")
print(sold_numeric_counts)



#Validate the logical order of date fields: ListingContractDate should precede PurchaseContractDate, which should precede CloseDate.

listing, listing_before_purchase  = valid_timeline(listing, 'ListingContractDate', 'PurchaseContractDate')
listing, purchase_before_close  = valid_timeline(listing, 'PurchaseContractDate', 'CloseDate')
sold, s_listing_before_purchase  = valid_timeline(sold, 'ListingContractDate', 'PurchaseContractDate')
sold, s_purchase_before_close  = valid_timeline(sold, 'PurchaseContractDate', 'CloseDate')

#geographic cleaning of data 
listing, geographic_flags = clean_coordinates(listing)
sold, s_geographic_flags = clean_coordinates(sold)