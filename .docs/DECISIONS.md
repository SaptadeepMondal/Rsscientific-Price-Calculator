# Decision Record

# Decision 001 — Move from PDF parsing to Excel

## Status
Accepted

## Date
2026-10-05

## Context
Initial iterations (v1-v3) assumed the price list was delivered exclusively via PDF from suppliers, requiring complex, error-prone text extraction. The customer has now clarified that an Excel (`.xls`, `.xlsx`) version of the master product/price list is available.

## Decision
Abandon all PDF parsing approaches. Build the app around reading the Excel files natively.

## Rationale
Excel files provide structured tabular data natively. Parsing this data is magnitudes more reliable, faster, and simpler to implement than OCR or layout-based PDF extraction.

## Consequences
- Requires `pandas` and `openpyxl` dependencies.
- Greatly simplifies the ingestion pipeline.
- Vastly improves import speed and accuracy.

---

# Decision 002 — Use CustomTkinter for GUI

## Status
Accepted

## Date
2026-10-05

## Context
The customer requested a "glassmorphism" aesthetic: frosted-glass panels over gradient backgrounds. Native Python GUI tools (like plain `tkinter` or `PyQt`) do not support true OS-level background blur natively across platforms.

## Decision
Use `customtkinter` to simulate the look via translucent panels, soft rounded corners, and gradient backgrounds.

## Alternatives Considered
- **Web-based UI (pywebview + HTML/CSS)**: Would provide native CSS blur, but adds significant packaging complexity and overhead.

## Rationale
`customtkinter` strikes a good balance between achieving a modern, aesthetic look (dark mode, rounded shapes, solid custom colors) while keeping the Python build simple as a standalone executable.

## Consequences
- We will have to "simulate" glassmorphism (translucency + light borders) rather than use real backdrop filters, but it will be much easier to bundle into a single `.exe`.
