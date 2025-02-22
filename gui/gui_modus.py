import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class GUIModusFenster(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("GUI-Modus Einstellungen")
        self.geometry("400x200")
        self.resizable(False, False)
        self.config_file = "config.json"
        self.load_config()
        self.create_widgets()
        
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8-sig") as f:
                    self.config_data = json.load(f)
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden der Konfiguration: {e}")
                self.config_data = {}
        else:
            self.config_data = {"gui_mode": "alt"}
            
    def save_config_file(self):
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config_data, f, indent=4)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern der Konfiguration: {e}")
    
    def create_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Wähle den GUI-Modus:").grid(row=0, column=0, sticky="w", pady=10)
        
        self.gui_mode_var = tk.StringVar(value=self.config_data.get("gui_mode", "alt"))
        
        rb_alt = ttk.Radiobutton(frame, text="Alt (Tkinter-Multifenster)", variable=self.gui_mode_var, value="alt")
        rb_neu = ttk.Radiobutton(frame, text="Neu (PyQt-Einfenster)", variable=self.gui_mode_var, value="neu")
        rb_alt.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        rb_neu.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        
        btn_save = ttk.Button(frame, text="Speichern", command=self.save_settings)
        btn_save.grid(row=3, column=0, pady=20)
    
    def save_settings(self):
        self.config_data["gui_mode"] = self.gui_mode_var.get()
        self.save_config_file()
        messagebox.showinfo("Einstellungen", "GUI-Modus Einstellungen gespeichert.\nBitte starte die Anwendung neu, um die Änderung zu übernehmen.")
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = GUIModusFenster(root)
    app.mainloop()

