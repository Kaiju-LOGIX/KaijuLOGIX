import tkinter as tk
from tkinter import ttk, messagebox
import csv
from repository import ErsatzteileRepository

class ErsatzteileFenster(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Ersatzteilverwaltung")
        self.geometry("1400x800")
        self.state("zoomed")
        self.repo = ErsatzteileRepository()
        self.felder = [
            "Hersteller", "Typ", "Bauform", "Spannung", 
            "Bestellnummer", "Lagerplatz", "Beschreibung", "Zusatz1", "Zusatz2", "Zusatz3"
        ]
        self.entries = {}
        self.create_widgets()
        self.load_dropdown_filters()
        self.load_data()

    def create_widgets(self):
        # Linker Bereich: Formular zur Erfassung
        left_frame = ttk.LabelFrame(self, text="Neues Ersatzteil erfassen", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        for i, feld in enumerate(self.felder):
            lbl = ttk.Label(left_frame, text=feld + ":")
            lbl.grid(row=i, column=0, sticky=tk.W, padx=5, pady=3)
            entry = ttk.Entry(left_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=3)
            self.entries[feld] = entry
        btn_save = ttk.Button(left_frame, text="Ersatzteil speichern", command=self.save_ersatzteil)
        btn_save.grid(row=len(self.felder), column=0, columnspan=2, pady=10)
        
        # Rechter Bereich: Filter und TreeView
        right_frame = ttk.Frame(self)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Dropdown-Bereich für Hersteller und Typ (Schnellsuche)
        dropdown_frame = ttk.LabelFrame(right_frame, text="Schnellsuche", padding=10)
        dropdown_frame.pack(fill=tk.X, pady=(0,10))
        ttk.Label(dropdown_frame, text="Hersteller:").grid(row=0, column=0, padx=5, pady=5)
        self.hersteller_cb = ttk.Combobox(dropdown_frame, state="readonly")
        self.hersteller_cb.grid(row=0, column=1, padx=5, pady=5)
        self.hersteller_cb.bind("<<ComboboxSelected>>", self.on_hersteller_selected)
        ttk.Label(dropdown_frame, text="Typ:").grid(row=0, column=2, padx=5, pady=5)
        self.typ_cb = ttk.Combobox(dropdown_frame, state="readonly")
        self.typ_cb.grid(row=0, column=3, padx=5, pady=5)
        self.typ_cb.bind("<<ComboboxSelected>>", self.on_typ_selected)
        
        # Filterbereich für eine freie Suche
        filter_frame = ttk.LabelFrame(right_frame, text="Ersatzteile filtern", padding=10)
        filter_frame.pack(fill=tk.X, pady=(0,10))
        ttk.Label(filter_frame, text="Suche:").grid(row=0, column=0, padx=5, pady=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=30)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        # TreeView zur Anzeige der Ersatzteile
        self.tree = ttk.Treeview(right_frame, 
                                 columns=("id", "hersteller", "typ", "bauform", "spannung", "bestellnummer", "lagerplatz", "beschreibung"),
                                 show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("hersteller", text="Hersteller")
        self.tree.heading("typ", text="Typ")
        self.tree.heading("bauform", text="Bauform")
        self.tree.heading("spannung", text="Spannung")
        self.tree.heading("bestellnummer", text="Bestellnummer")
        self.tree.heading("lagerplatz", text="Lagerplatz")
        self.tree.heading("beschreibung", text="Beschreibung")
        self.tree.column("id", width=50)
        self.tree.column("hersteller", width=100)
        self.tree.column("typ", width=100)
        self.tree.column("bauform", width=100)
        self.tree.column("spannung", width=80)
        self.tree.column("bestellnummer", width=100)
        self.tree.column("lagerplatz", width=100)
        self.tree.column("beschreibung", width=200)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def load_dropdown_filters(self):
        # Hersteller aus der DB laden
        hersteller_list = self.repo.get_all_hersteller()
        self.hersteller_cb['values'] = [""] + hersteller_list
        self.hersteller_cb.current(0)
        # Typ-Dropdown zunächst leeren
        self.typ_cb['values'] = [""]
        self.typ_cb.current(0)

    def on_hersteller_selected(self, event=None):
        selected_hersteller = self.hersteller_cb.get().strip()
        if selected_hersteller:
            typ_list = self.repo.get_types_by_hersteller(selected_hersteller)
            self.typ_cb['values'] = [""] + typ_list
            self.typ_cb.current(0)
        else:
            self.typ_cb['values'] = [""]
            self.typ_cb.current(0)
        self.load_data()

    def on_typ_selected(self, event=None):
        self.load_data()

    def on_search(self, event=None):
        self.load_data()

    def save_ersatzteil(self):
        data = []
        for feld in self.felder:
            data.append(self.entries[feld].get().strip())
        try:
            self.repo.insert_ersatzteil(tuple(data))
            messagebox.showinfo("Erfolg", "Ersatzteil wurde gespeichert.")
            self.clear_form()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {e}")

    def load_data(self, search_query=""):
        # Alle Ersatzteile mit optionaler Freisuche laden
        records = self.repo.get_all_ersatzteile(search_query)
        hersteller_filter = self.hersteller_cb.get().strip()
        typ_filter = self.typ_cb.get().strip()
        filtered = []
        for rec in records:
            # rec: (id, hersteller, typ, bauform, spannung, bestellnummer, lagerplatz, beschreibung, ...)
            match = True
            if hersteller_filter and rec[1] != hersteller_filter:
                match = False
            if typ_filter and rec[2] != typ_filter:
                match = False
            if match:
                filtered.append(rec)
        for item in self.tree.get_children():
            self.tree.delete(item)
        for rec in filtered:
            self.tree.insert("", tk.END, values=rec[:8])

    def clear_form(self):
        for feld in self.felder:
            self.entries[feld].delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ef = ErsatzteileFenster(root)
    ef.mainloop()
