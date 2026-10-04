import customtkinter as ctk
from tkinter import messagebox
from app.data.column_matcher import guess_column_mapping
from app.data.importer import process_imported_data

class ColumnMappingWindow(ctk.CTkToplevel):
    def __init__(self, master, headers, filepath, df):
        super().__init__(master)
        self.title("Confirm Column Mapping")
        self.geometry("500x550")
        self.filepath = filepath
        self.df = df
        
        self.grid_columnconfigure(0, weight=1)
        
        # Add empty option to headers
        self.options = ["-- Leave Blank --"] + headers
        
        # Guess initial mapping
        self.guessed_mapping = guess_column_mapping(headers)
        
        self.title_label = ctk.CTkLabel(self, text="Match Excel Columns", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10))
        
        self.desc_label = ctk.CTkLabel(self, text="Please confirm the columns from your Excel file.")
        self.desc_label.grid(row=1, column=0, pady=(0, 20))
        
        self.mapping_vars = {}
        
        # Create dropdowns for each required field
        fields = ["Code", "Name", "Size", "Unit Price"]
        for i, field in enumerate(fields):
            frame = ctk.CTkFrame(self, fg_color="transparent")
            frame.grid(row=i+2, column=0, padx=40, pady=10, sticky="ew")
            frame.grid_columnconfigure(1, weight=1)
            
            lbl = ctk.CTkLabel(frame, text=field + ":", width=100, anchor="w")
            lbl.grid(row=0, column=0, padx=(0, 10))
            
            var = ctk.StringVar(value=self.guessed_mapping[field] if self.guessed_mapping[field] else "-- Leave Blank --")
            self.mapping_vars[field] = var
            
            dropdown = ctk.CTkOptionMenu(frame, variable=var, values=self.options)
            dropdown.grid(row=0, column=1, sticky="ew")
            
        self.import_btn = ctk.CTkButton(self, text="Confirm & Import", command=self.on_import)
        self.import_btn.grid(row=len(fields)+2, column=0, pady=20)
        
    def on_import(self):
        final_mapping = {field: var.get() for field, var in self.mapping_vars.items()}
        
        # Validate that essential fields are not blank
        if final_mapping["Name"] == "-- Leave Blank --" and final_mapping["Code"] == "-- Leave Blank --":
            messagebox.showerror("Error", "Either Code or Name column must be mapped.")
            return
        if final_mapping["Unit Price"] == "-- Leave Blank --":
            messagebox.showerror("Error", "Unit Price column is required.")
            return
            
        # Convert "-- Leave Blank --" to None
        for k, v in final_mapping.items():
            if v == "-- Leave Blank --":
                final_mapping[k] = None
                
        process_imported_data(self.df, final_mapping, self.filepath)
        
        messagebox.showinfo("Success", "Data imported successfully (simulation).")
        self.destroy()
