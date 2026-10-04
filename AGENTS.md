# AI Agent Instructions for RS Scientific Price Lookup App

This project is a Windows desktop application built with Python.

## Core Directives
- **No PDF Parsing**: We are only parsing Excel (.xls, .xlsx) files. 
- **Simple Math**: Price is simply `unit price * quantity`. No tiered pricing, no discount, no GST calculation.
- **Visual Style**: Glassmorphism using `customtkinter`. Ensure a premium, modern feel.
- **Offline First**: All data is cached locally in an SQLite database.
- **Don't hardcode columns**: Excel import requires dynamic column matching for code, name, brand, pack size, and unit price.

## Project Structure
- `app/main.py`: Entry point for the application.
- `app/ui/`: Contains UI components (`customtkinter`).
- `app/data/`: Data loading (`pandas`), processing, and database (`sqlite3`) interactions.
- `app/pricing.py`: Logic for price calculation.

## Tech Stack
- Python 3.10+
- `customtkinter`
- `pandas`
- `openpyxl`
- `sqlite3`

## Execution
Run `python -m app.main` from the repository root.

## Guidelines
- UI aesthetics matter greatly here. Focus on frosted glass effects, subtle shadows, and a clean sans-serif font.
- Wait for a sample file from the user before finalizing the Excel import logic.
- Keep the database schema as defined in `.docs/DESIGN.md`.
