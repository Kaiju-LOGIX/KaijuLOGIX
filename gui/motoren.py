import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from repository import MotorenRepository

class MotorenFenster(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Motorenverwaltung")
        self.geometry("1400x800")
        self.state("zoomed")
        self.repo = MotorenRepository()
        self.felder = [
            "Motornummer", "im SW", "G", "BS", "Firma", "NEU", "Typ", "Seriennummer",
            "Leistung", "Spannung", "N1_min", "N2_min", "Strom", "Cosinus Phi", "Lagerort", "Bemerkung"
        ]
        self.entries = {}
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Linker Bereich: Formular
        left_frame = ttk.LabelFrame(self, text="Neuen Motor erfassen", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        for i, feld in enumerate(self.felder):
            lbl = ttk.Label(left_frame, text=feld + ":")
            lbl.grid(row=i, column=0, sticky=tk.W, padx=5, pady=3)
            entry = ttk.Entry(left_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=3)
            self.entries[feld] = entry
        btn_save = ttk.Button(left_frame, text="Motor speichern", command=self.save_motor)
        btn_save.grid(row=len(self.felder), column=0, columnspan=2, pady=10)

        # Rechter Bereich: Filter und TreeView
        right_frame = ttk.Frame(self)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        filter_frame = ttk.LabelFrame(right_frame, text="Motoren filtern", padding=10)
        filter_frame.pack(fill=tk.X, pady=(0,10))
        ttk.Label(filter_frame, text="Suche:").grid(row=0, column=0, padx=5, pady=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=30)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_entry.bind("<KeyRelease>", self.on_search)
        btn_export = ttk.Button(filter_frame, text="Exportieren", command=self.export_data)
        btn_export.grid(row=0, column=2, padx=5, pady=5)
        
        self.tree = ttk.Treeview(right_frame, columns=("id", "motornummer", "Firma", "Typ", "Seriennummer", "Leistung", "Spannung", "Bemerkung"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("motornummer", text="Motornummer")
        self.tree.heading("Firma", text="Firma")
        self.tree.heading("Typ", text="Typ")
        self.tree.heading("Seriennummer", text="Seriennummer")
        self.tree.heading("Leistung", text="Leistung")
        self.tree.heading("Spannung", text="Spannung")
        self.tree.heading("Bemerkung", text="Bemerkung")
        self.tree.column("id", width=50)
        self.tree.column("motornummer", width=100)
        self.tree.column("Firma", width=100)
        self.tree.column("Typ", width=100)
        self.tree.column("Seriennummer", width=100)
        self.tree.column("Leistung", width=80)
        self.tree.column("Spannung", width=80)
        self.tree.column("Bemerkung", width=200)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def save_motor(self):
        data = []
        for feld in self.felder:
            data.append(self.entries[feld].get().strip())
        try:
            self.repo.insert_motor(tuple(data))
            messagebox.showinfo("Erfolg", "Motor wurde gespeichert.")
            self.clear_form()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {e}")

    def load_data(self, search_query=""):
        for item in self.tree.get_children():
            self.tree.delete(item)
        records = self.repo.get_all_motoren(search_query)
        for rec in records:
            # Wir zeigen hier beispielhaft ausgewählte Spalten an:
            # ID, Motornummer, Firma (Index 5), Typ (Index 7), Seriennummer (Index 8), Leistung (Index 9), Spannung (Index 10), Bemerkung (Index 16)
            self.tree.insert("", tk.END, values=(rec[0], rec[1], rec[5], rec[7], rec[8], rec[9], rec[10], rec[16]))
    
    def on_search(self, event=None):
        query = self.search_var.get().strip()
        self.load_data(query)
    
    def export_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Dateien", "*.csv")])
        if not file_path:
            return
        data = []
        for child in self.tree.get_children():
            data.append(self.tree.item(child)['values'])
        try:
            with open(file_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Motornummer", "Firma", "Typ", "Seriennummer", "Leistung", "Spannung", "Bemerkung"])
                writer.writerows(data)
            messagebox.showinfo("Export", f"Daten wurden erfolgreich exportiert nach:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Export fehlgeschlagen: {e}")
    
    def clear_form(self):
        for feld in self.felder:
            self.entries[feld].delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    mf = MotorenFenster(root)
    mf.mainloop()
