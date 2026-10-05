import customtkinter as ctk
from app.data.db import search_products
from app.ui.theme import *

class SearchView(ctk.CTkFrame):
    def __init__(self, master, on_product_selected, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.on_product_selected = on_product_selected
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Search Box
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.on_search_changed)
        
        self.search_entry = ctk.CTkEntry(
            self, 
            textvariable=self.search_var, 
            placeholder_text="Search by name or code",
            placeholder_text_color=INK_MUTED,
            font=get_font("body"),
            text_color=INK,
            fg_color=PANEL_GLASS,
            border_color=PANEL_EDGE,
            border_width=1,
            corner_radius=RAD_BUTTON,
            height=40
        )
        self.search_entry.grid(row=0, column=0, pady=(0, 16), sticky="ew")
        
        # We need to simulate the focus ring glow. 
        # For simplicity, we bind FocusIn and FocusOut to change border_color to ACCENT, border_width to 2
        self.search_entry.bind("<FocusIn>", lambda e: self.search_entry.configure(border_color=ACCENT, border_width=2))
        self.search_entry.bind("<FocusOut>", lambda e: self.search_entry.configure(border_color=PANEL_EDGE, border_width=1))
        
        # Results List
        self.results_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.results_frame.grid(row=1, column=0, sticky="nsew")
        self.results_frame.grid_columnconfigure(0, weight=1)
        
        self.after_id = None
        
    def on_search_changed(self, *args):
        if self.after_id:
            self.after_cancel(self.after_id)
        self.after_id = self.after(150, self.perform_search)
        
    def perform_search(self):
        query = self.search_var.get()
        
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        if not query or len(query) < 2:
            return
            
        results = search_products(query)
        
        if not results:
            lbl = ctk.CTkLabel(self.results_frame, text=f"No products match '{query}'.", font=get_font("body"), text_color=INK_MUTED)
            lbl.grid(row=0, column=0, pady=20, sticky="w")
            return
            
        for i, prod in enumerate(results):
            # A row frame
            row_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent", corner_radius=0)
            row_frame.grid(row=i*2, column=0, sticky="ew")
            row_frame.grid_columnconfigure(0, weight=1)
            
            # Hover effects
            def on_enter(e, f=row_frame): f.configure(fg_color=PANEL_GLASS)
            def on_leave(e, f=row_frame): f.configure(fg_color="transparent")
            def on_click(e, p=prod): self.on_product_selected(p)
            
            # Bind events to frame and its children so click/hover anywhere works
            row_frame.bind("<Enter>", on_enter)
            row_frame.bind("<Leave>", on_leave)
            row_frame.bind("<Button-1>", on_click)
            
            # Inner layout for text
            info_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            info_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=12)
            info_frame.grid_columnconfigure(1, weight=1)
            
            info_frame.bind("<Enter>", on_enter)
            info_frame.bind("<Leave>", on_leave)
            info_frame.bind("<Button-1>", on_click)
            
            # Left: Name and Size
            text_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            text_frame.grid(row=0, column=0, sticky="w")
            text_frame.bind("<Enter>", on_enter)
            text_frame.bind("<Leave>", on_leave)
            text_frame.bind("<Button-1>", on_click)
            
            name_lbl = ctk.CTkLabel(text_frame, text=f"[{prod['code']}] {prod['name']}", font=get_font("body"), text_color=INK)
            name_lbl.grid(row=0, column=0, sticky="w")
            name_lbl.bind("<Enter>", on_enter)
            name_lbl.bind("<Leave>", on_leave)
            name_lbl.bind("<Button-1>", on_click)
            
            size_lbl = ctk.CTkLabel(text_frame, text=prod['size'], font=get_font("metadata"), text_color=INK_MUTED)
            size_lbl.grid(row=1, column=0, sticky="w")
            size_lbl.bind("<Enter>", on_enter)
            size_lbl.bind("<Leave>", on_leave)
            size_lbl.bind("<Button-1>", on_click)
            
            # Right: Price
            price_text = f"₹{prod['unit_price']:.2f}" if prod['unit_price'] is not None else "POR"
            price_color = INK if prod['unit_price'] is not None else CAUTION
            price_font = get_font("numeral_large") if prod['unit_price'] is not None else get_font("body")
            
            price_lbl = ctk.CTkLabel(info_frame, text=price_text, font=price_font, text_color=price_color, anchor="e")
            price_lbl.grid(row=0, column=1, sticky="e")
            price_lbl.bind("<Enter>", on_enter)
            price_lbl.bind("<Leave>", on_leave)
            price_lbl.bind("<Button-1>", on_click)
            
            # Divider
            divider = ctk.CTkFrame(self.results_frame, fg_color=PANEL_EDGE, height=1, corner_radius=0)
            divider.grid(row=i*2+1, column=0, sticky="ew")

    def clear_search(self):
        self.search_var.set("")
