# RS Scientific - Price Lookup App

## Purpose
A Windows desktop app for RS Scientific (a lab chemical supplier) that allows staff to load a product price list (Excel file), search for a product by name or code, enter a quantity, and get the calculated price. Users can build a running receipt/quote of multiple products with a grand total.

## Features
- **Load Price List**: Import Excel (.xls/.xlsx) files with automatic column detection (code, name, brand, pack size, unit price).
- **Search**: Fast, type-ahead search by product name or code.
- **Price Calculation**: Calculates simple `unit price × quantity`. Handles "Price on request" items.
- **Receipt/Quote Generator**: Builds a running list of priced items with a grand total.
- **Manage Data**: Loaded price lists are cached in local SQLite database for permanent offline access without needing to re-upload.

## Technology Stack
- Language: Python 3
- GUI: `customtkinter` (Glassmorphism theme)
- Data Processing: `pandas`, `openpyxl`
- Database: `sqlite3`
- Packaging: `pyinstaller`

## Setup and Running

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python -m app.main
   ```

## Packaging
To build a standalone executable for Windows:
```bash
pyinstaller --onefile --windowed --icon=assets/icon.ico app/main.py
```
