import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import pandas as pd
from app.data.importer import load_excel_headers
from app.ui.column_mapping_view import ColumnMappingWindow
from app.ui.manage_lists_view import ManageListsWindow
from app.ui.search_view import SearchView
from app.ui.receipt_view import ReceiptView
from app.ui.theme import *
from app.data.db import init_db

ctk.set_appearance_mode("Light")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RS Scientific - Price Lookup")
        self.geometry("1000x700")
        
        # Window bg
        self.configure(fg_color=CANVAS)

        self.grid_columnconfigure(0, weight=2) # Left pane (Bench)
        self.grid_columnconfigure(1, weight=1) # Right pane (Tray)
        self.grid_rowconfigure(1, weight=1)

        # -------------------------------------------------------------
        # Top Control Strip
        # -------------------------------------------------------------
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=24, pady=(16, 0))
        
        # Thin divider below header
        self.header_divider = ctk.CTkFrame(self, fg_color=PANEL_EDGE, height=1, corner_radius=0)
        self.header_divider.grid(row=0, column=0, columnspan=2, sticky="sew", padx=24, pady=(0, 0))

        self.title_label = ctk.CTkLabel(self.header_frame, text="RS Scientific", font=get_font("title"), text_color=INK)
        self.title_label.pack(side="left", pady=10)

        self.load_btn = ctk.CTkButton(
            self.header_frame, text="Load Price List", font=get_font("body"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color="white",
            corner_radius=RAD_BUTTON, width=130, command=self.load_price_list
        )
        self.load_btn.pack(side="right", padx=(10, 0), pady=10)

        self.manage_btn = ctk.CTkButton(
            self.header_frame, text="Manage Price Lists", font=get_font("body"),
            fg_color="transparent", hover_color=PANEL_GLASS, text_color=INK,
            border_width=1, border_color=PANEL_EDGE,
            corner_radius=RAD_BUTTON, width=130, command=self.open_manage_lists
        )
        self.manage_btn.pack(side="right", pady=10)

        # -------------------------------------------------------------
        # Left Pane: Search
        # -------------------------------------------------------------
        self.left_pane = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.left_pane.grid(row=1, column=0, sticky="nsew", padx=(24, 12), pady=24)
        self.left_pane.grid_columnconfigure(0, weight=1)
        self.left_pane.grid_rowconfigure(2, weight=1)

        self.search_lbl = ctk.CTkLabel(self.left_pane, text="Search by name or code", font=get_font("body"), text_color=INK)
        self.search_lbl.grid(row=0, column=0, sticky="w", pady=(0, 8))

        # Search View handles the search input and results list
        self.search_view = SearchView(self.left_pane, on_product_selected=self.on_product_selected)
        self.search_view.grid(row=1, column=0, sticky="nsew", rowspan=2)

        # Selected Product Panel (Elevated)
        self.selected_prod = None
        
        # We place it at row 3
        self.item_frame = ctk.CTkFrame(self.left_pane, fg_color=PANEL_GLASS, corner_radius=RAD_PANEL, border_width=1, border_color=PANEL_EDGE)
        self.item_frame.grid(row=3, column=0, sticky="ew", pady=(16, 0))
        self.item_frame.grid_columnconfigure(1, weight=1)
        self.item_frame.grid_remove() # Hide initially
        
        self.item_name_lbl = ctk.CTkLabel(self.item_frame, text="", font=get_font("header"), text_color=INK)
        self.item_name_lbl.grid(row=0, column=0, columnspan=3, padx=16, pady=(16, 8), sticky="w")
        
        self.qty_frame = ctk.CTkFrame(self.item_frame, fg_color="transparent")
        self.qty_frame.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="w")
        
        ctk.CTkLabel(self.qty_frame, text="Qty", font=get_font("body"), text_color=INK_MUTED).pack(side="left", padx=(0, 8))
        self.qty_var = ctk.StringVar(value="1")
        self.qty_entry = ctk.CTkEntry(
            self.qty_frame, textvariable=self.qty_var, width=60, font=get_font("numeral_body"),
            fg_color=PANEL_GLASS, border_color=PANEL_EDGE, text_color=INK, corner_radius=RAD_BUTTON
        )
        self.qty_entry.pack(side="left")
        self.qty_var.trace_add("write", self.update_item_price)
        
        self.price_lbl = ctk.CTkLabel(self.item_frame, text="", font=get_font("numeral_large"), text_color=INK, anchor="e")
        self.price_lbl.grid(row=1, column=1, padx=16, pady=(0, 16), sticky="e")
        
        self.add_btn = ctk.CTkButton(
            self.item_frame, text="Add to List", font=get_font("body"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color="white",
            corner_radius=RAD_BUTTON, command=self.add_to_receipt
        )
        self.add_btn.grid(row=1, column=2, padx=16, pady=(0, 16), sticky="e")

        # -------------------------------------------------------------
        # Right Pane: Receipt Tray
        # -------------------------------------------------------------
        self.receipt_view = ReceiptView(self)
        self.receipt_view.grid(row=1, column=1, sticky="nsew", padx=(12, 24), pady=24)

    def on_product_selected(self, product):
        self.selected_prod = product
        self.qty_var.set("1")
        self.item_name_lbl.configure(text=f"{product['name']}")
        self.update_item_price()
        self.item_frame.grid() # Show the elevated panel
        
    def update_item_price(self, *args):
        if not self.selected_prod:
            return
            
        try:
            qty = int(self.qty_var.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            self.price_lbl.configure(text="Invalid qty", text_color=REMOVE, font=get_font("body"))
            self.add_btn.configure(state="disabled", fg_color=INK_MUTED)
            return
            
        price_val = self.selected_prod['unit_price']
        if price_val is not None:
            self.price_lbl.configure(text=f"₹{price_val * qty:.2f}", text_color=INK, font=get_font("numeral_large"))
        else:
            self.price_lbl.configure(text="Price on request", text_color=CAUTION, font=get_font("body"))
            
        self.add_btn.configure(state="normal", fg_color=ACCENT)

    def add_to_receipt(self):
        if not self.selected_prod:
            return
        try:
            qty = int(self.qty_var.get())
        except ValueError:
            return
            
        self.receipt_view.add_item(self.selected_prod, qty)
        self.selected_prod = None
        self.item_frame.grid_remove() # Hide again
        self.search_view.clear_search()

    def open_manage_lists(self):
        ManageListsWindow(self).grab_set()

    def load_price_list(self):
        filepath = filedialog.askopenfilename(
            title="Select Price List",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if not filepath:
            return

        try:
            headers, df = load_excel_headers(filepath)
            mapping_window = ColumnMappingWindow(self, headers, filepath, df)
            mapping_window.grab_set()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")

if __name__ == "__main__":
    init_db()
    app = App()
    app.mainloop()
