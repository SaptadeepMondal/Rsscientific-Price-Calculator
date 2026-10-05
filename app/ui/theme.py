import customtkinter as ctk

# Colors - Reagent Palette (Light Mode)
CANVAS = "#EEF4F2"
PANEL_GLASS = "#FAFDFC"
PANEL_EDGE = "#C9DEDA"
INK = "#162421"
INK_MUTED = "#5B6D68"
ACCENT = "#1D6F74"
ACCENT_HOVER = "#155457"
CAUTION = "#AD6A14"
REMOVE = "#A33B34"

# Radii
RAD_PANEL = 12
RAD_BUTTON = 8
RAD_SMALL = 4

# Fonts
# We will use the fallback fonts "Segoe UI" and "Consolas".
# If custom TTF loading is implemented later, these can map to Inter and IBM Plex Mono.
def get_font(role="body"):
    """
    Roles: 
    - title (18pt, semibold)
    - header (15pt, semibold)
    - body (13pt, regular)
    - metadata (11pt, regular)
    - numeral_large (15pt, medium mono)
    - numeral_body (13pt, regular mono)
    """
    if role == "title":
        return ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
    elif role == "header":
        return ctk.CTkFont(family="Segoe UI", size=15, weight="bold")
    elif role == "body":
        return ctk.CTkFont(family="Segoe UI", size=13, weight="normal")
    elif role == "metadata":
        return ctk.CTkFont(family="Segoe UI", size=11, weight="normal")
    elif role == "numeral_large":
        return ctk.CTkFont(family="Consolas", size=15, weight="bold")
    elif role == "numeral_body":
        return ctk.CTkFont(family="Consolas", size=13, weight="normal")
    return ctk.CTkFont(family="Segoe UI", size=13, weight="normal")
