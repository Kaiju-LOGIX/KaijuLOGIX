import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

class VerzeichnisseFenster(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Verzeichnisse Einstellungen")
        self.geometry("600x400")
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
            # Standardwerte setzen, wenn keine config.json vorhanden ist
            self.config_data = {
                "backup_path": "C:\\KaijuLOGIX\\Backup",
                "export_path": "C:\\KaijuLOGIX\\Export",
                "knowledgebase_path": "C:\\KaijuLOGIX\\Knowledgebase"
            }

    def save_config_file(self):
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config_data, f, indent=4)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern der Konfiguration: {e}")

    def create_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)
        
        # Backup/Restore Pfad
        ttk.Label(frame, text="Backup/Restore Pfad:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_backup = ttk.Entry(frame, width=50)
        self.entry_backup.grid(row=0, column=1, padx=5, pady=5)
        self.entry_backup.insert(0, self.config_data.get("backup_path", ""))
        btn_backup = ttk.Button(frame, text="Durchsuchen", command=self.browse_backup)
        btn_backup.grid(row=0, column=2, padx=5, pady=5)
        
        # Export Pfad
        ttk.Label(frame, text="Export Pfad:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_export = ttk.Entry(frame, width=50)
        self.entry_export.grid(row=1, column=1, padx=5, pady=5)
        self.entry_export.insert(0, self.config_data.get("export_path", ""))
        btn_export = ttk.Button(frame, text="Durchsuchen", command=self.browse_export)
        btn_export.grid(row=1, column=2, padx=5, pady=5)
        
        # Knowledgebase Pfad
        ttk.Label(frame, text="Knowledgebase Pfad:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_kb = ttk.Entry(frame, width=50)
        self.entry_kb.grid(row=2, column=1, padx=5, pady=5)
        self.entry_kb.insert(0, self.config_data.get("knowledgebase_path", ""))
        btn_kb = ttk.Button(frame, text="Durchsuchen", command=self.browse_kb)
        btn_kb.grid(row=2, column=2, padx=5, pady=5)
        
        btn_save = ttk.Button(frame, text="Einstellungen speichern", command=self.save_settings)
        btn_save.grid(row=3, column=0, columnspan=3, pady=20)

    def browse_backup(self):
        directory = filedialog.askdirectory(title="Backup/Restore Pfad auswählen")
        if directory:
            self.entry_backup.delete(0, tk.END)
            self.entry_backup.insert(0, directory)

    def browse_export(self):
        directory = filedialog.askdirectory(title="Export Pfad auswählen")
        if directory:
            self.entry_export.delete(0, tk.END)
            self.entry_export.insert(0, directory)

    def browse_kb(self):
        directory = filedialog.askdirectory(title="Knowledgebase Pfad auswählen")
        if directory:
            self.entry_kb.delete(0, tk.END)
            self.entry_kb.insert(0, directory)

    def save_settings(self):
        self.config_data["backup_path"] = self.entry_backup.get().strip()
        self.config_data["export_path"] = self.entry_export.get().strip()
        self.config_data["knowledgebase_path"] = self.entry_kb.get().strip()
        self.save_config_file()
        messagebox.showinfo("Einstellungen", "Verzeichnis-Einstellungen wurden gespeichert.")
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    vf = VerzeichnisseFenster(root)
    vf.mainloop()

