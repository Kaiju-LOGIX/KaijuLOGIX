import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkcalendar import DateEntry

class PannenFenster(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Pannenverwaltung")
        self.geometry("1400x800")
        self.state("zoomed")
        self.felder = [
            "Datum", "Schicht", "Name", "Abteilung", 
            "Anlage", "Anlagenteil", "Baugruppe", "Beschreibung", "Maßnahme",
            "Fehlerkategorie", "Fehlerursache", "Ausfallzeit (Min)",
            "Priorität", "Melder"
        ]
        self.db_columns = [
            "datum", "schicht", "name", "abteilung", 
            "anlage", "anlagenteil", "baugruppe", "beschreibung", "massnahme",
            "fehlerkategorie", "fehlerursache", "ausfallzeit",
            "prioritaet", "melder"
        ]
        self.fehlerkategorien = ["Elektrik", "Mechanik", "Bedienfehler", "Sensorik", "Software/Steuerung", "Hydraulik/Pneumatik"]
        self.fehlerursachen = ["Verschleiß", "Materialfehler", "Bedienfehler", "Wartungsdefizit", "Externe Ursache"]
        self.prioritaeten = ["1", "2", "3", "4", "5"]
        self.widget_dict = {}
        self.create_widgets()
        self.load_dropdown_data()  # Methode zum Initialbefüllen der Dropdowns aufrufen
        self.load_data()

    def create_widgets(self):
        info_label = ttk.Label(
            self,
            text="Pannenverwaltung: Erfassung und Analyse von Störungen\nLinks: Neue Panne erfassen, rechts: Filter und Anzeige.",
            anchor="center"
        )
        info_label.pack(fill=tk.X, padx=10, pady=(10,5))
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        form_frame = ttk.LabelFrame(main_frame, text="Neue Panne erfassen", padding=10)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        row_idx = 0
        for feld in self.felder:
            lbl = ttk.Label(form_frame, text=feld + ":")
            lbl.grid(row=row_idx, column=0, sticky=tk.W, padx=5, pady=3)
            if feld == "Abteilung":
                cb = ttk.Combobox(form_frame, state="readonly")
                cb.grid(row=row_idx, column=1, padx=5, pady=3, sticky=tk.W)
                cb.bind("<<ComboboxSelected>>", lambda e: self.update_anlagen())
                self.widget_dict[feld] = cb
            elif feld == "Anlage":
                cb = ttk.Combobox(form_frame, state="readonly")
                cb.grid(row=row_idx, column=1, padx=5, pady=3, sticky=tk.W)
                cb.bind("<<ComboboxSelected>>", lambda e: self.update_anlagenteile())
                self.widget_dict[feld] = cb
            elif feld == "Anlagenteil":
                cb = ttk.Combobox(form_frame, state="readonly")
                cb.grid(row=row_idx, column=1, padx=5, pady=3, sticky=tk.W)
                self.widget_dict[feld] = cb
            elif feld == "Fehlerkategorie":
                cb = ttk.Combobox(form_frame, values=self.fehlerkategorien, state="readonly")
                cb.grid(row=row_idx, column=1, padx=5, pady=3, sticky=tk.W)
                cb.current(0)
                self.widget_dict[feld] = cb
            elif feld == "Fehlerursache":
                cb = ttk.Combobox(form_frame, values=self.fehlerursachen, state="readonly")
                cb.grid(row=row_idx, column=1, padx=5, pady=3, sticky=tk.W)
                cb.current(0)
                self.widget_dict[feld] = cb
            elif feld == "Priorität":
                cb = ttk.Combobox(form_frame, values=self.prioritaeten, state="readonly")
                cb.grid(row=row_idx, column=1, padx=5, pady=3, sticky=tk.W)
                cb.current(0)
                self.widget_dict[feld] = cb
            elif feld == "Maßnahme":
                txt = tk.Text(form_frame, width=30, height=3)
                txt.grid(row=row_idx, column=1, padx=5, pady=3, sticky=tk.W)
                self.widget_dict[feld] = txt
            else:
                entry = ttk.Entry(form_frame, width=30)
                entry.grid(row=row_idx, column=1, padx=5, pady=3, sticky=tk.W)
                self.widget_dict[feld] = entry
            row_idx += 1
        btn_save = ttk.Button(form_frame, text="Panne speichern", command=self.save_panne)
        btn_save.grid(row=row_idx, column=0, columnspan=2, pady=10)
        
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        filter_frame = ttk.LabelFrame(right_frame, text="Pannen anzeigen (Filter)", padding=10)
        filter_frame.pack(fill=tk.X, pady=(0,10))
        ttk.Label(filter_frame, text="Abteilung:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.filter_abt = ttk.Combobox(filter_frame, state="readonly")
        self.filter_abt.grid(row=0, column=1, padx=5, pady=3, sticky=tk.W)
        self.filter_abt.bind("<<ComboboxSelected>>", lambda e: self.update_filter_anlagen())
        ttk.Label(filter_frame, text="Anlage:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=3)
        self.filter_anlage = ttk.Combobox(filter_frame, state="readonly")
        self.filter_anlage.grid(row=0, column=3, padx=5, pady=3, sticky=tk.W)
        self.filter_anlage.bind("<<ComboboxSelected>>", lambda e: self.update_filter_anlagenteile())
        ttk.Label(filter_frame, text="Anlagenteil:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=3)
        self.filter_anlagenteil = ttk.Combobox(filter_frame, state="readonly")
        self.filter_anlagenteil.grid(row=0, column=5, padx=5, pady=3, sticky=tk.W)
        ttk.Label(filter_frame, text="Startdatum:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.start_date = DateEntry(filter_frame, date_pattern='yyyy-mm-dd', width=12)
        self.start_date.grid(row=1, column=1, padx=5, pady=3, sticky=tk.W)
        ttk.Label(filter_frame, text="Enddatum:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=3)
        self.end_date = DateEntry(filter_frame, date_pattern='yyyy-mm-dd', width=12)
        self.end_date.grid(row=1, column=3, padx=5, pady=3, sticky=tk.W)
        btn_filter = ttk.Button(filter_frame, text="Anzeigen", command=self.filter_pannen)
        btn_filter.grid(row=1, column=5, padx=5, pady=3)
        search_frame = ttk.Frame(right_frame)
        search_frame.pack(fill=tk.X, pady=(0,5))
        ttk.Label(search_frame, text="Suche:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", self.on_search)
        self.tree_frame = ttk.Frame(right_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        self.spalten = self.db_columns
        self.tree = ttk.Treeview(self.tree_frame, columns=self.spalten, show="headings")
        for feld, col in zip(self.felder, self.db_columns):
            self.tree.heading(col, text=feld)
            self.tree.column(col, width=120, anchor="center")
        vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew", columnspan=2)
        self.tree_frame.rowconfigure(0, weight=1)
        self.tree_frame.columnconfigure(0, weight=1)

    def load_dropdown_data(self):
        # Dropdowns für das Erfassungsformular befüllen
        abt_list = self.get_abteilungen_from_db()
        if "Abteilung" in self.widget_dict:
            self.widget_dict["Abteilung"]['values'] = abt_list
            if abt_list:
                self.widget_dict["Abteilung"].current(0)
                self.update_anlagen()
        # Dropdowns im Filterbereich befüllen
        self.load_filter_dropdowns()

    def load_filter_dropdowns(self):
        abt_list = self.get_abteilungen_from_db()
        self.filter_abt['values'] = [""] + abt_list
        self.filter_abt.current(0)
        self.update_filter_anlagen()
    
    def get_abteilungen_from_db(self):
        conn = sqlite3.connect("instandhaltung.db")
        c = conn.cursor()
        c.execute("SELECT name FROM abteilungen ORDER BY name")
        rows = c.fetchall()
        conn.close()
        return [r[0] for r in rows]
    
    def update_anlagen(self):
        abt_cb = self.widget_dict.get("Abteilung")
        if not abt_cb:
            return
        selected_abt = abt_cb.get()
        conn = sqlite3.connect("instandhaltung.db")
        c = conn.cursor()
        c.execute("SELECT abteilung_id FROM abteilungen WHERE name = ?", (selected_abt,))
        abt_row = c.fetchone()
        abt_id = abt_row[0] if abt_row else None
        anl_names = []
        if abt_id is not None:
            c.execute("SELECT name FROM anlagen WHERE abteilung_id = ?", (abt_id,))
            rows = c.fetchall()
            anl_names = [r[0] for r in rows]
        conn.close()
        if "Anlage" in self.widget_dict:
            anl_cb = self.widget_dict["Anlage"]
            anl_cb['values'] = anl_names
            if anl_names:
                anl_cb.current(0)
                self.update_anlagenteile()
            else:
                anl_cb.set("")
                if "Anlagenteil" in self.widget_dict:
                    self.widget_dict["Anlagenteil"]['values'] = []
                    self.widget_dict["Anlagenteil"].set("")
    
    def update_anlagenteile(self):
        anl_cb = self.widget_dict.get("Anlage")
        if not anl_cb:
            return
        selected_anl = anl_cb.get()
        conn = sqlite3.connect("instandhaltung.db")
        c = conn.cursor()
        c.execute("SELECT anlage_id FROM anlagen WHERE name = ?", (selected_anl,))
        row_anlage = c.fetchone()
        if row_anlage:
            anlage_id = row_anlage[0]
            c.execute("SELECT name FROM anlagenteile WHERE anlage_id = ?", (anlage_id,))
            rows = c.fetchall()
            teil_names = [r[0] for r in rows]
        else:
            teil_names = []
        conn.close()
        if "Anlagenteil" in self.widget_dict:
            teil_cb = self.widget_dict["Anlagenteil"]
            teil_cb['values'] = teil_names
            if teil_names:
                teil_cb.current(0)
            else:
                teil_cb.set("")
    
    def update_filter_anlagen(self):
        selected_abt = self.filter_abt.get()
        conn = sqlite3.connect("instandhaltung.db")
        c = conn.cursor()
        anl_names = []
        if selected_abt:
            c.execute("SELECT abteilung_id FROM abteilungen WHERE name = ?", (selected_abt,))
            abt_row = c.fetchone()
            if abt_row:
                abt_id = abt_row[0]
                c.execute("SELECT name FROM anlagen WHERE abteilung_id = ?", (abt_id,))
                rows = c.fetchall()
                anl_names = [r[0] for r in rows]
        conn.close()
        self.filter_anlage['values'] = [""] + anl_names
        self.filter_anlage.current(0)
        self.update_filter_anlagenteile()
    
    def update_filter_anlagenteile(self):
        selected_anl = self.filter_anlage.get()
        conn = sqlite3.connect("instandhaltung.db")
        c = conn.cursor()
        teil_names = []
        if selected_anl:
            c.execute("SELECT anlage_id FROM anlagen WHERE name = ?", (selected_anl,))
            row_anlage = c.fetchone()
            if row_anlage:
                anlage_id = row_anlage[0]
                c.execute("SELECT name FROM anlagenteile WHERE anlage_id = ?", (anlage_id,))
                rows = c.fetchall()
                teil_names = [r[0] for r in rows]
        conn.close()
        self.filter_anlagenteil['values'] = [""] + teil_names
        self.filter_anlagenteil.current(0)
    
    def filter_pannen(self):
        conditions = []
        params = []
        abt = self.filter_abt.get().strip()
        if abt:
            conditions.append("abteilung = ?")
            params.append(abt)
        anl = self.filter_anlage.get().strip()
        if anl:
            conditions.append("anlage = ?")
            params.append(anl)
        teil = self.filter_anlagenteil.get().strip()
        if teil:
            conditions.append("anlagenteil = ?")
            params.append(teil)
        start_date = self.start_date.get_date().strftime("%Y-%m-%d")
        end_date = self.end_date.get_date().strftime("%Y-%m-%d")
        if start_date and end_date:
            conditions.append("datum BETWEEN ? AND ?")
            params.extend([start_date, end_date])
        sql = "SELECT " + ", ".join(self.db_columns) + " FROM pannen"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        conn = sqlite3.connect("instandhaltung.db")
        c = conn.cursor()
        c.execute(sql, tuple(params))
        rows = c.fetchall()
        conn.close()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in rows:
            self.tree.insert("", tk.END, values=row)
    
    def save_panne(self):
        daten = []
        for feld, col in zip(self.felder, self.db_columns):
            widget = self.widget_dict[feld]
            if feld == "Maßnahme":
                val = widget.get("1.0", tk.END).strip()
            else:
                val = widget.get().strip()
            daten.append(val)
        try:
            conn = sqlite3.connect("instandhaltung.db")
            c = conn.cursor()
            c.execute(f"""
                INSERT INTO pannen
                ({", ".join(self.db_columns)})
                VALUES ({", ".join(["?"]*len(self.db_columns))})
            """, tuple(daten))
            conn.commit()
            conn.close()
            messagebox.showinfo("Erfolg", "Panne wurde gespeichert.")
            self.clear_input_fields()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {e}")
    
    def load_data(self, search_query=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = sqlite3.connect("instandhaltung.db")
        c = conn.cursor()
        if search_query:
            sql = f"""
                SELECT {", ".join(self.db_columns)}
                FROM pannen
                WHERE name LIKE ? OR beschreibung LIKE ? OR fehlerkategorie LIKE ?
                OR fehlerursache LIKE ? OR massnahme LIKE ? OR melder LIKE ?
            """
            like_str = f"%{search_query}%"
            c.execute(sql, (like_str,)*6)
        else:
            sql = f"SELECT {', '.join(self.db_columns)} FROM pannen"
            c.execute(sql)
        rows = c.fetchall()
        conn.close()
        for row in rows:
            self.tree.insert("", tk.END, values=row)
    
    def on_search(self, event=None):
        query = self.search_var.get().strip()
        self.load_data(search_query=query if query else None)
    
    def clear_input_fields(self):
        for feld in self.felder:
            widget = self.widget_dict[feld]
            if feld == "Maßnahme":
                widget.delete("1.0", tk.END)
            else:
                widget.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    pf = PannenFenster(root)
    pf.mainloop()
