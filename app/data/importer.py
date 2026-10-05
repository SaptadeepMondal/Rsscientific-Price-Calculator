import pandas as pd
import os
from app.data.db import insert_products, remove_file_data

def load_excel_headers(filepath):
    """
    Reads the first few rows of the excel file to get headers.
    Returns (list_of_headers, dataframe).
    We read the whole dataframe here because we'll need it right after mapping,
    and reading a few thousand rows in pandas is very fast.
    """
    df = pd.read_excel(filepath)
    # Convert all column names to string just in case
    headers = [str(col) for col in df.columns]
    return headers, df

def process_imported_data(df, mapping, filepath):
    """
    Processes the dataframe according to the confirmed mapping.
    And pushes it into the sqlite db.
    """
    filename = os.path.basename(filepath)
    
    # First, let's remove any existing data for this file
    remove_file_data(filename)

    records_to_insert = []
    
    for _, row in df.iterrows():
        # Safely get column names from mapping
        code_col = mapping.get("code")
        name_col = mapping.get("name")
        size_col = mapping.get("size")
        price_col = mapping.get("unit_price")

        code = str(row[code_col]) if code_col and pd.notna(row[code_col]) else ""
        name = str(row[name_col]) if name_col and pd.notna(row[name_col]) else ""
        size = str(row[size_col]) if size_col and pd.notna(row[size_col]) else ""
        
        # Unit price parsing
        raw_price = row[price_col] if price_col and pd.notna(row[price_col]) else None
        
        try:
            unit_price = float(raw_price) if raw_price is not None else None
        except ValueError:
            # Could be "POR" or text
            unit_price = None

        search_text = f"{code} {name}".lower()
        
        # Only insert if code or name exists
        if code.strip() or name.strip():
            records_to_insert.append((
                filename,
                code,
                name,
                size,
                unit_price,
                search_text
            ))
            
    if records_to_insert:
        insert_products(records_to_insert)
