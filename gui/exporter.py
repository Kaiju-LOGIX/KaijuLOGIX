import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import os
import shutil
import datetime

class ExportFenster(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Daten exportieren")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="Export-Typ wählen:").pack(anchor="w")
        self.export_type = tk.StringVar(self, value="Excel")
        ttk.Radiobutton(frame, text="Excel Export", variable=self.export_type, value="Excel").pack(anchor="w")
        ttk.Radiobutton(frame, text="SQL Export", variable=self.export_type, value="SQL").pack(anchor="w")
        ttk.Label(frame, text="Export-Verzeichnis:").pack(anchor="w", pady=(10,0))
        self.dir_entry = ttk.Entry(frame, width=40)
        self.dir_entry.pack(anchor="w")
        btn_browse = ttk.Button(frame, text="Verzeichnis auswählen", command=self.browse_directory)
        btn_browse.pack(anchor="w", pady=5)
        btn_export = ttk.Button(frame, text="Exportieren", command=self.export_data)
        btn_export.pack(pady=10)

    def browse_directory(self):
        directory = filedialog.askdirectory(title="Export-Verzeichnis auswählen")
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)

    def export_data(self):
        export_type = self.export_type.get()
        directory = self.dir_entry.get().strip()
        if not directory:
            messagebox.showerror("Fehler", "Bitte ein Export-Verzeichnis auswählen.")
            return
        if export_type == "Excel":
            src = "exported_data.xlsx"  # Beispiel-Dateiname
            dst = os.path.join(directory, "exported_data.xlsx")
            try:
                shutil.copy(src, dst)
                messagebox.showinfo("Export", f"Excel-Daten wurden exportiert nach:\n{dst}")
            except Exception as e:
                messagebox.showerror("Fehler", f"Excel Export fehlgeschlagen: {e}")
        elif export_type == "SQL":
            src = "instandhaltung.db"
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            dst = os.path.join(directory, f"instandhaltung_export_{timestamp}.db")
            try:
                shutil.copy(src, dst)
                messagebox.showinfo("Export", f"SQL-Datenbank exportiert nach:\n{dst}")
            except Exception as e:
                messagebox.showerror("Fehler", f"SQL Export fehlgeschlagen: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExportFenster(root)
    root.mainloop()

