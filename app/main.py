import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import pandas as pd
from app.data.importer import load_excel_headers
from app.ui.column_mapping_view import ColumnMappingWindow
from app.ui.manage_lists_view import ManageListsWindow
from app.ui.search_view import SearchView
from app.ui.receipt_view import ReceiptView

from app.data.db import init_db

# Configure standard appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RS Scientific - Price Lookup")
        self.geometry("1000x700")

        self.grid_columnconfigure(0, weight=2) # Search side
        self.grid_columnconfigure(1, weight=1) # Receipt side
        self.grid_rowconfigure(0, weight=1)

        # Left panel: Search & Actions
        self.left_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(2, weight=1)

        # Title & Buttons
        self.header_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, text="RS Scientific Price App", font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(side="left", padx=10)

        self.manage_btn = ctk.CTkButton(
            self.header_frame, text="Manage Price Lists", fg_color="gray40", hover_color="gray30", command=self.open_manage_lists, width=130
        )
        self.manage_btn.pack(side="right", padx=5)
        
        self.load_btn = ctk.CTkButton(
            self.header_frame, text="Load Price List", command=self.load_price_list, width=130
        )
        self.load_btn.pack(side="right", padx=5)

        # Single Item View / Input Quantity
        self.item_frame = ctk.CTkFrame(self.left_frame)
        self.item_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10), padx=10)
        self.item_frame.grid_columnconfigure(1, weight=1)
        
        self.selected_prod = None
        
        self.item_lbl = ctk.CTkLabel(self.item_frame, text="Select a product below", anchor="w")
        self.item_lbl.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        
        self.qty_var = ctk.StringVar(value="1")
        self.qty_entry = ctk.CTkEntry(self.item_frame, textvariable=self.qty_var, width=60)
        self.qty_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")
        self.qty_var.trace_add("write", self.update_item_price)
        
        self.price_lbl = ctk.CTkLabel(self.item_frame, text="", font=ctk.CTkFont(weight="bold"))
        self.price_lbl.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="w")
        
        self.add_btn = ctk.CTkButton(self.item_frame, text="Add to List", state="disabled", command=self.add_to_receipt)
        self.add_btn.grid(row=1, column=2, padx=10, pady=(0, 10), sticky="e")

        # Search View
        self.search_view = SearchView(self.left_frame, on_product_selected=self.on_product_selected)
        self.search_view.grid(row=2, column=0, sticky="nsew", padx=10)

        # Right panel: Receipt
        self.receipt_view = ReceiptView(self)
        self.receipt_view.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    def on_product_selected(self, product):
        self.selected_prod = product
        self.qty_var.set("1")
        self.item_lbl.configure(text=f"[{product['code']}] {product['name']}")
        self.update_item_price()
        self.add_btn.configure(state="normal")
        
    def update_item_price(self, *args):
        if not self.selected_prod:
            return
            
        try:
            qty = int(self.qty_var.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            self.price_lbl.configure(text="Invalid quantity")
            self.add_btn.configure(state="disabled")
            return
            
        price_val = self.selected_prod['unit_price']
        if price_val is not None:
            self.price_lbl.configure(text=f"${price_val * qty:.2f}")
        else:
            self.price_lbl.configure(text="Price on request (POR)")
            
        self.add_btn.configure(state="normal")

    def add_to_receipt(self):
        if not self.selected_prod:
            return
        try:
            qty = int(self.qty_var.get())
        except ValueError:
            return
            
        self.receipt_view.add_item(self.selected_prod, qty)
        self.selected_prod = None
        self.item_lbl.configure(text="Select a product below")
        self.price_lbl.configure(text="")
        self.add_btn.configure(state="disabled")
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
            # 1. Read headers
            headers, df = load_excel_headers(filepath)
            
            # 2. Show mapping window
            mapping_window = ColumnMappingWindow(self, headers, filepath, df)
            mapping_window.grab_set()  # wait for this window
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")

if __name__ == "__main__":
    init_db()
    app = App()
    app.mainloop()
