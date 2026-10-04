# Design Document

## Problem Statement
RS Scientific needs a desktop tool for their staff to quickly look up product prices and build running quotes/receipts for customers. The previous workflow (manually searching PDFs) was inefficient. The new requirement is to use their master Excel price lists as the source of truth, offering a fast, searchable interface over this data.

## Goals
- Provide sub-second search capabilities over thousands of products.
- Calculate simple line-item prices (quantity × unit price).
- Generate a running receipt of items and a grand total.
- Persist uploaded price lists so users don't have to upload the same file repeatedly.
- Provide a visually premium interface (glassmorphism) beyond standard, flat desktop apps.

## Non-Goals
- Complex discounting or tier-based pricing.
- Tax calculation (GST).
- Persistent state for the receipt/quotes (cleared on restart).
- Multi-user remote database sync (fully offline app).
- PDF parsing.

## Database Schema
The offline cache uses a simple SQLite schema:
```sql
CREATE TABLE products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_file TEXT,
  code TEXT,
  name TEXT,
  brand TEXT,
  pack_label TEXT,
  unit_price REAL, -- NULL for "Price on request"
  search_text TEXT, -- Lowercase concatenation of code, name, brand
  loaded_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## User Workflow
1. **Load Data**: The user opens the app and uses the "Manage Price Lists" or a generic load button to pick an `.xls` or `.xlsx` file.
2. **Column Match**: A popup suggests column headers; the user verifies or corrects them. The data imports.
3. **Search**: The user types part of a code or product name. A list of matches appears below.
4. **Price**: The user selects a match, inputs a quantity, and clicks "Add to List".
5. **Quote**: The selected item appears in the Receipt view, with price calculated. The total price is updated.
6. **Repeat**: The search box clears, ready for the next item.
