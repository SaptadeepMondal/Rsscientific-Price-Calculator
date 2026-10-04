# System Architecture

## Overview
The application is a standalone desktop application developed in Python. It heavily leverages `customtkinter` for its UI to provide a modern, glassmorphism aesthetic. It relies on `pandas` for handling Excel data imports and `sqlite3` for offline storage of the price list.

## Directory Structure
```
rsscientific-price-lookup/
├── app/
│   ├── main.py                # application entry point; initializes root window
│   ├── ui/
│   │   ├── search_view.py     # handles search input, autocomplete, and results table
│   │   ├── receipt_view.py    # manages the running quote/receipt, totals, and remove actions
│   │   ├── manage_lists_view.py # panel to view imported files and remove them
│   │   ├── column_mapping_view.py # UI to handle dynamic column matching from excel
│   │   └── theme.py           # core visual styles, colors, and fonts (glassmorphism rules)
│   ├── data/
│   │   ├── importer.py        # reads excel file, parses rows, formats data
│   │   ├── column_matcher.py  # heuristics to identify header roles and split brands
│   │   └── db.py              # sqlite connection, table creation, and queries
│   └── pricing.py             # core logic for price x quantity, POR edge case
├── assets/
│   └── icon.ico               # app icon for packaging
├── requirements.txt           # dependencies
└── README.md
```

## Data Flow
1. **Data Loading:** User selects an `.xls`/`.xlsx` file -> `importer.py` reads headers -> `column_matcher.py` guesses headers and offers a confirmation UI (`column_mapping_view.py`) -> confirmed data is written to the SQLite cache via `db.py`.
2. **Search:** User types in `search_view.py` -> `db.py` executes an indexed query on `search_text` -> results return to `search_view.py`.
3. **Pricing:** User clicks a result and inputs quantity -> `pricing.py` calculates price -> item is passed to `receipt_view.py` to join the running total.
