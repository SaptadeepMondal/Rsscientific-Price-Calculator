import customtkinter as ctk
from tkinter import messagebox
from app.data.importer import process_imported_data
from app.ui.theme import *

class ColumnMappingWindow(ctk.CTkToplevel):
    def __init__(self, master, excel_headers, filepath, df):
        super().__init__(master)
        self.title("Map Columns")
        self.geometry("500x550")
        self.filepath = filepath
        self.df = df
        
        self.configure(fg_color=PANEL_GLASS)
        
        self.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(self, text="Verify Column Mapping", font=get_font("header"), text_color=INK)
        self.title_label.grid(row=0, column=0, pady=(24, 8), padx=24, sticky="w")
        
        self.desc_label = ctk.CTkLabel(
            self, text="We've guessed the columns below based on the file.\nPlease correct any mistakes.",
            font=get_font("body"), text_color=INK_MUTED, justify="left"
        )
        self.desc_label.grid(row=1, column=0, padx=24, sticky="w", pady=(0, 24))
        
        self.mapping_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.mapping_frame.grid(row=2, column=0, padx=24, sticky="ew")
        self.mapping_frame.grid_columnconfigure(1, weight=1)

        # Options for dropdowns (include a blank option)
        self.options = ["-- Skip --"] + excel_headers

        self.dropdown_vars = {}
        fields = [
            ("code", "Product Code", ["code", "cat", "no", "item"]),
            ("name", "Product Name", ["name", "desc", "product"]),
            ("size", "Pack Size", ["size", "pack", "qty"]),
            ("unit_price", "Unit Price", ["price", "rate", "mrp"])
        ]
        
        for i, (field_id, field_label, hints) in enumerate(fields):
            lbl = ctk.CTkLabel(self.mapping_frame, text=field_label, font=get_font("body"), text_color=INK)
            lbl.grid(row=i, column=0, sticky="w", pady=12)
            
            var = ctk.StringVar(value=self.guess_column(excel_headers, hints))
            self.dropdown_vars[field_id] = var
            
            menu = ctk.CTkOptionMenu(
                self.mapping_frame, variable=var, values=self.options, font=get_font("body"),
                dropdown_font=get_font("body"), fg_color=CANVAS, button_color=PANEL_EDGE,
                button_hover_color=PANEL_EDGE, text_color=INK, corner_radius=RAD_BUTTON
            )
            menu.grid(row=i, column=1, sticky="ew", padx=(24, 0), pady=12)
            
        # Error Label
        self.error_lbl = ctk.CTkLabel(self, text="", font=get_font("body"), text_color=REMOVE, justify="left")
        self.error_lbl.grid(row=3, column=0, padx=24, pady=12, sticky="w")
            
        self.import_btn = ctk.CTkButton(
            self, text="Confirm & Import", font=get_font("body"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color="white", corner_radius=RAD_BUTTON,
            command=self.confirm_mapping
        )
        self.import_btn.grid(row=4, column=0, pady=24)

    def guess_column(self, headers, hints):
        headers_lower = [h.lower() for h in headers]
        for hint in hints:
            for i, h in enumerate(headers_lower):
                if hint in h:
                    return headers[i]
        return "-- Skip --"

    def confirm_mapping(self):
        mapping = {}
        for field, var in self.dropdown_vars.items():
            val = var.get()
            if val != "-- Skip --":
                mapping[field] = val
                
        # Validations
        if 'unit_price' not in mapping:
            self.error_lbl.configure(text="No column looked like a price. Choose one from the dropdowns below.")
            return
            
        if 'code' not in mapping and 'name' not in mapping:
            self.error_lbl.configure(text="You must map either Product Code or Product Name.")
            return

        self.error_lbl.configure(text="")
        
        try:
            process_imported_data(self.df, mapping, self.filepath)
            messagebox.showinfo("Success", "Price list imported successfully.")
            
            # The parent App has a running loop. We just destroy this window.
            self.destroy()
        except Exception as e:
            self.error_lbl.configure(text=f"Failed to import: {str(e)}")
