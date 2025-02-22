import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import shutil
import datetime

class EinstellungenFenster(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Einstellungen")
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
            self.config_data = {
                "knowledgebase_path": "",
                "backup_path": os.path.expanduser("~"),
                "optional_setting": ""
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

        ttk.Label(frame, text="Knowledgebase Pfad:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_kb = ttk.Entry(frame, width=50)
        self.entry_kb.grid(row=0, column=1, padx=5, pady=5)
        self.entry_kb.insert(0, self.config_data.get("knowledgebase_path", ""))
        btn_browse_kb = ttk.Button(frame, text="Durchsuchen", command=self.browse_kb_path)
        btn_browse_kb.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(frame, text="Backup Pfad:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_backup = ttk.Entry(frame, width=50)
        self.entry_backup.grid(row=1, column=1, padx=5, pady=5)
        self.entry_backup.insert(0, self.config_data.get("backup_path", ""))
        btn_browse_backup = ttk.Button(frame, text="Durchsuchen", command=self.browse_backup_path)
        btn_browse_backup.grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(frame, text="Optionale Einstellung:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_optional = ttk.Entry(frame, width=50)
        self.entry_optional.grid(row=2, column=1, padx=5, pady=5)
        self.entry_optional.insert(0, self.config_data.get("optional_setting", ""))

        btn_parse = ttk.Button(frame, text="PDF-Parsen starten", command=self.start_pdf_parsing)
        btn_parse.grid(row=3, column=0, columnspan=3, pady=10)

        btn_backup = ttk.Button(frame, text="Backup erstellen", command=self.create_backup)
        btn_backup.grid(row=4, column=0, columnspan=3, pady=10)

        btn_save = ttk.Button(frame, text="Einstellungen speichern", command=self.save_settings)
        btn_save.grid(row=5, column=0, columnspan=3, pady=20)
    
    def browse_kb_path(self):
        directory = filedialog.askdirectory(title="Wähle den Knowledgebase-Ordner")
        if directory:
            self.entry_kb.delete(0, tk.END)
            self.entry_kb.insert(0, directory)
    
    def browse_backup_path(self):
        directory = filedialog.askdirectory(title="Wähle den Backup-Speicherort")
        if directory:
            self.entry_backup.delete(0, tk.END)
            self.entry_backup.insert(0, directory)
    
    def start_pdf_parsing(self):
        try:
            from gui.knowledgebase import KnowledgebaseFenster
            path = self.entry_kb.get()
            if not os.path.isdir(path):
                messagebox.showerror("Fehler", "Der angegebene Knowledgebase-Pfad ist ungültig.")
                return
            # Einfaches Neuladen der PDF-Liste als Simulation des Parsens
            kb = KnowledgebaseFenster(self)
            kb.load_pdf_list()
            messagebox.showinfo("PDF-Parsen", "PDF-Parsen abgeschlossen.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim PDF-Parsen: {e}")
    
    def create_backup(self):
        backup_dir = self.entry_backup.get()
        if not os.path.isdir(backup_dir):
            messagebox.showerror("Fehler", "Der angegebene Backup-Pfad ist ungültig.")
            return
        db_file = "instandhaltung.db"
        if os.path.exists(db_file):
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"instandhaltung_backup_{timestamp}.db")
            try:
                shutil.copy(db_file, backup_file)
                messagebox.showinfo("Backup", f"Backup wurde erstellt:\n{backup_file}")
            except Exception as e:
                messagebox.showerror("Fehler", f"Backup fehlgeschlagen: {e}")
        else:
            messagebox.showerror("Fehler", "Keine Datenbankdatei gefunden.")
    
    def save_settings(self):
        self.config_data["knowledgebase_path"] = self.entry_kb.get()
        self.config_data["backup_path"] = self.entry_backup.get()
        self.config_data["optional_setting"] = self.entry_optional.get()
        self.save_config_file()
        messagebox.showinfo("Einstellungen", "Einstellungen wurden gespeichert.")
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hauptfenster")
    root.geometry("800x600")
    EinstellungenFenster(root)
    root.mainloop()

