import re

def guess_column_mapping(headers):
    """
    Given a list of headers from an Excel file, try to guess which one is
    Code, Name, Size, and Unit Price.
    Returns a dict mapping expected_field -> best_guess_header
    """
    mapping = {
        "Code": None,
        "Name": None,
        "Size": None,
        "Unit Price": None
    }
    
    for h in headers:
        if not isinstance(h, str):
            continue
        h_lower = h.lower().strip()
        
        # Code
        if re.search(r'\b(code|sku|item code|product code)\b', h_lower) and not mapping["Code"]:
            mapping["Code"] = h
            
        # Name
        elif re.search(r'\b(name|product|description|item)\b', h_lower) and not mapping["Name"]:
            mapping["Name"] = h
            
        # Size (Pack Size/Quantity)
        elif re.search(r'\b(qty|quantity|size|pack|pkg|packing|capacity|unit)\b', h_lower) and not mapping["Size"]:
            mapping["Size"] = h
            
        # Unit Price
        elif re.search(r'\b(price|unit price|rate|mrp|cost)\b', h_lower) and not mapping["Unit Price"]:
            mapping["Unit Price"] = h
            
    return mapping
