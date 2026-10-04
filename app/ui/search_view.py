import customtkinter as ctk
from app.data.db import search_products

class SearchView(ctk.CTkFrame):
    def __init__(self, master, on_product_selected, **kwargs):
        super().__init__(master, **kwargs)
        self.on_product_selected = on_product_selected
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Search Box
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.on_search_changed)
        
        self.search_entry = ctk.CTkEntry(
            self, 
            textvariable=self.search_var, 
            placeholder_text="Search by product code or name...",
            font=ctk.CTkFont(size=14)
        )
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Results List
        self.results_frame = ctk.CTkScrollableFrame(self)
        self.results_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.results_frame.grid_columnconfigure(0, weight=1)
        
        self.after_id = None
        
    def on_search_changed(self, *args):
        # Debounce the search input
        if self.after_id:
            self.after_cancel(self.after_id)
        self.after_id = self.after(150, self.perform_search)
        
    def perform_search(self):
        query = self.search_var.get()
        
        # Clear existing
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        if not query or len(query) < 2:
            return
            
        results = search_products(query)
        
        if not results:
            ctk.CTkLabel(self.results_frame, text="No matching products found.", text_color="gray").grid(row=0, column=0, pady=10)
            return
            
        for i, prod in enumerate(results):
            btn = ctk.CTkButton(
                self.results_frame,
                text=f"[{prod['code']}] {prod['name']} ({prod['size']})",
                anchor="w",
                fg_color="transparent",
                text_color=("black", "white"),
                hover_color="gray30",
                command=lambda p=prod: self.on_product_selected(p)
            )
            btn.grid(row=i, column=0, sticky="ew", pady=2)
            
    def clear_search(self):
        self.search_var.set("")
