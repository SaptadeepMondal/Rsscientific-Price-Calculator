import customtkinter as ctk

class ReceiptView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.header_lbl = ctk.CTkLabel(self, text="Current Quote", font=ctk.CTkFont(size=16, weight="bold"))
        self.header_lbl.grid(row=0, column=0, pady=10)
        
        # Receipt List
        self.receipt_frame = ctk.CTkScrollableFrame(self)
        self.receipt_frame.grid(row=1, column=0, padx=10, sticky="nsew")
        self.receipt_frame.grid_columnconfigure(0, weight=1)
        
        # Totals area
        self.totals_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.totals_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.totals_frame.grid_columnconfigure(0, weight=1)
        
        self.total_lbl = ctk.CTkLabel(self.totals_frame, text="Total: $0.00", font=ctk.CTkFont(size=18, weight="bold"))
        self.total_lbl.grid(row=0, column=0, sticky="e")
        
        self.por_lbl = ctk.CTkLabel(self.totals_frame, text="", text_color="orange")
        self.por_lbl.grid(row=1, column=0, sticky="e")
        
        # Clear button
        self.clear_btn = ctk.CTkButton(self, text="Clear List", fg_color="#D32F2F", hover_color="#B71C1C", command=self.clear_receipt)
        self.clear_btn.grid(row=3, column=0, pady=(0, 10))
        
        self.items = []
        
    def add_item(self, product, quantity):
        price_val = product['unit_price']
        
        if price_val is not None:
            total_price = price_val * quantity
            price_text = f"${total_price:.2f}"
        else:
            total_price = None
            price_text = "POR"
            
        item = {
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
            'price_text': price_text
        }
        self.items.append(item)
        self.refresh_ui()
        
    def remove_item(self, index):
        if 0 <= index < len(self.items):
            self.items.pop(index)
            self.refresh_ui()
            
    def clear_receipt(self):
        self.items = []
        self.refresh_ui()
        
    def refresh_ui(self):
        for widget in self.receipt_frame.winfo_children():
            widget.destroy()
            
        running_total = 0.0
        por_count = 0
        
        for i, item in enumerate(self.items):
            prod = item['product']
            
            frame = ctk.CTkFrame(self.receipt_frame, fg_color="gray25", corner_radius=5)
            frame.grid(row=i, column=0, sticky="ew", pady=2)
            frame.grid_columnconfigure(0, weight=1)
            
            text = f"[{prod['code']}] {prod['name']} x {item['quantity']} = {item['price_text']}"
            lbl = ctk.CTkLabel(frame, text=text, anchor="w", justify="left")
            lbl.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            
            del_btn = ctk.CTkButton(
                frame, text="×", width=30, fg_color="#D32F2F", hover_color="#B71C1C", 
                command=lambda idx=i: self.remove_item(idx)
            )
            del_btn.grid(row=0, column=1, padx=5, pady=5)
            
            if item['total_price'] is not None:
                running_total += item['total_price']
            else:
                por_count += 1
                
        self.total_lbl.configure(text=f"Total: ${running_total:.2f}")
        
        if por_count > 0:
            self.por_lbl.configure(text=f"+ {por_count} item(s) priced on request")
        else:
            self.por_lbl.configure(text="")
