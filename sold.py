import pandas as pd
import numpy as np

from pathlib import Path

def import_concat_save(file_prefix, output_name):

    dfs = []
    base_dir = Path("/Users/morganstevenson/Desktop/IDX")

    for year in [2024, 2025]:
        months = range(1, 13)

        for month in months:
            stem = f"{file_prefix}{year}{month:02d}"

            filled_file = base_dir / f"{stem}_filled.csv"
            regular_file = base_dir / f"{stem}.csv"

            if filled_file.exists():
                file_path = filled_file
            elif regular_file.exists():
                file_path = regular_file
            else:
                print(f"Missing: {stem}")
                continue

            print(f"Reading {file_path.name}")
            dfs.append(pd.read_csv(file_path))

    # Jan-Jun 2026
    for month in range(1, 7):
        stem = f"{file_prefix}2026{month:02d}"

        filled_file = base_dir / f"{stem}_filled.csv"
        regular_file = base_dir / f"{stem}.csv"

        if filled_file.exists():
            file_path = filled_file
        elif regular_file.exists():
            file_path = regular_file
        else:
             print(f"Missing: {stem}")
             continue

        print(f"Reading {file_path.name}")
        dfs.append(pd.read_csv(file_path))

    df = pd.concat(dfs, ignore_index=True)

    output_path = base_dir / output_name
    df.to_csv(output_path, index=False)

    print(f"Saved {len(df):,} rows to {output_path}")

    return df


all_sold = pd.read_csv('/Users/morganstevenson/Desktop/IDX/CRMLSold_2024_2026Jun.csv')

all_sold.shape

res_sold = all_sold[all_sold['PropertyType'] == 'Residential']

res_sold.shape