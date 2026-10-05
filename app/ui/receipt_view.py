import customtkinter as ctk
from app.ui.theme import *

class ReceiptView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=PANEL_GLASS, border_color=PANEL_EDGE, border_width=1, corner_radius=RAD_PANEL, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.header_lbl = ctk.CTkLabel(self, text="Current Quote", font=get_font("header"), text_color=INK)
        self.header_lbl.grid(row=0, column=0, padx=24, pady=24, sticky="w")
        
        # Receipt List
        self.receipt_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.receipt_frame.grid(row=1, column=0, padx=12, sticky="nsew")
        self.receipt_frame.grid_columnconfigure(0, weight=1)
        
        # Totals area
        self.totals_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.totals_frame.grid(row=2, column=0, padx=24, pady=24, sticky="ew")
        self.totals_frame.grid_columnconfigure(0, weight=1)
        
        self.total_lbl = ctk.CTkLabel(self.totals_frame, text="Total: ₹0.00", font=get_font("numeral_large"), text_color=INK)
        self.total_lbl.grid(row=0, column=0, sticky="e")
        
        self.por_lbl = ctk.CTkLabel(self.totals_frame, text="", font=get_font("metadata"), text_color=CAUTION)
        self.por_lbl.grid(row=1, column=0, sticky="e")
        
        # Actions
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.grid(row=3, column=0, padx=24, pady=(0, 24), sticky="ew")
        self.actions_frame.grid_columnconfigure(0, weight=1)
        
        self.copy_btn = ctk.CTkButton(
            self.actions_frame, text="Copy Quote", font=get_font("body"),
            fg_color="transparent", hover_color=CANVAS, border_width=1, border_color=PANEL_EDGE, text_color=INK,
            corner_radius=RAD_BUTTON, command=self.copy_quote
        )
        self.copy_btn.pack(side="left")
        
        self.clear_btn = ctk.CTkButton(
            self.actions_frame, text="Clear", font=get_font("body"),
            fg_color="transparent", hover_color=CANVAS, text_color=REMOVE, border_width=1, border_color=PANEL_EDGE,
            corner_radius=RAD_BUTTON, width=80, command=self.clear_receipt
        )
        self.clear_btn.pack(side="right")
        
        self.items = []
        self.refresh_ui()
        
    def add_item(self, product, quantity):
        price_val = product['unit_price']
        
        if price_val is not None:
            total_price = price_val * quantity
            price_text = f"₹{total_price:.2f}"
            price_color = INK
            price_font = get_font("numeral_body")
        else:
            total_price = None
            price_text = "POR"
            price_color = CAUTION
            price_font = get_font("body")
            
        item = {
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
            'price_text': price_text,
            'price_color': price_color,
            'price_font': price_font
        }
        
        # Insert at the top (index 0)
        self.items.insert(0, item)
        self.refresh_ui()
        
    def remove_item(self, index):
        if 0 <= index < len(self.items):
            self.items.pop(index)
            self.refresh_ui()
            
    def clear_receipt(self):
        self.items = []
        self.refresh_ui()
        
    def copy_quote(self):
        # Build text string
        lines = ["RS Scientific - Quote\n"]
        for item in self.items:
            prod = item['product']
            lines.append(f"[{prod['code']}] {prod['name']} x {item['quantity']} = {item['price_text']}")
            
        lines.append(f"\n{self.total_lbl.cget('text')}")
        if self.por_lbl.cget('text'):
            lines.append(self.por_lbl.cget('text'))
            
        text = "\n".join(lines)
        self.clipboard_clear()
        self.clipboard_append(text)
        
    def refresh_ui(self):
        for widget in self.receipt_frame.winfo_children():
            widget.destroy()
            
        if not self.items:
            empty_lbl = ctk.CTkLabel(self.receipt_frame, text="Your quote is empty. Add a product\nfrom the search results.", font=get_font("body"), text_color=INK_MUTED, justify="center")
            empty_lbl.grid(row=0, column=0, pady=40)
            self.total_lbl.configure(text="Total: ₹0.00")
            self.por_lbl.configure(text="")
            self.copy_btn.configure(state="disabled")
            self.clear_btn.configure(state="disabled")
            return
            
        self.copy_btn.configure(state="normal")
        self.clear_btn.configure(state="normal")
            
        running_total = 0.0
        por_count = 0
        
        for i, item in enumerate(self.items):
            prod = item['product']
            
            # Receipt chip
            frame = ctk.CTkFrame(self.receipt_frame, fg_color=CANVAS, corner_radius=RAD_BUTTON)
            frame.grid(row=i, column=0, sticky="ew", pady=4, padx=12)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(1, weight=0, minsize=80)
            frame.grid_columnconfigure(2, weight=0, minsize=40)
            
            # Label
            text = f"[{prod['code']}] {prod['name']} × {item['quantity']}"
            lbl = ctk.CTkLabel(frame, text=text, font=get_font("body"), text_color=INK, anchor="w", justify="left", wraplength=200)
            lbl.grid(row=0, column=0, padx=12, pady=12, sticky="w")
            
            # Price
            price_lbl = ctk.CTkLabel(frame, text=item['price_text'], font=item['price_font'], text_color=item['price_color'])
            price_lbl.grid(row=0, column=1, padx=(12, 4), pady=12, sticky="e")
            
            # Delete button (×)
            del_btn = ctk.CTkButton(
                frame, text="×", font=get_font("body"), width=24, height=24, corner_radius=12,
                fg_color="transparent", text_color=INK_MUTED, hover_color=REMOVE,
                command=lambda idx=i: self.remove_item(idx)
            )
            # Hover effect for text color change
            del_btn.bind("<Enter>", lambda e, b=del_btn: b.configure(text_color="white"))
            del_btn.bind("<Leave>", lambda e, b=del_btn: b.configure(text_color=INK_MUTED))
            
            del_btn.grid(row=0, column=2, padx=(0, 8), pady=12, sticky="e")
            
            if item['total_price'] is not None:
                running_total += item['total_price']
            else:
                por_count += 1
                
        self.total_lbl.configure(text=f"Total: ₹{running_total:.2f}")
        
        if por_count > 0:
            self.por_lbl.configure(text=f"+ {por_count} item(s) priced on request")
        else:
            self.por_lbl.configure(text="")
