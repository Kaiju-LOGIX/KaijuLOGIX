import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime

class WartungenFenster(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Wartungs- & Prüfungsverwaltung")
        self.geometry("900x600")
        self.anlage_id_map = {}
        self.create_widgets()
        self.load_anlagen()
        self.load_data()

    def create_widgets(self):
        form_frame = ttk.LabelFrame(self, text="Neue Prüfung erfassen", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(form_frame, text="Anlage:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.combo_anlage = ttk.Combobox(form_frame, state="readonly")
        self.combo_anlage.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Datum (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_datum = ttk.Entry(form_frame)
        self.entry_datum.grid(row=1, column=1, padx=5, pady=5)
        aktuelles_datum = datetime.date.today().strftime("%Y-%m-%d")
        self.entry_datum.insert(0, aktuelles_datum)
        ttk.Label(form_frame, text="Prüfnotiz:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.text_pruefnotiz = tk.Text(form_frame, width=40, height=3)
        self.text_pruefnotiz.grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Wiederholung (Monate):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_wiederholung = ttk.Entry(form_frame)
        self.entry_wiederholung.grid(row=3, column=1, padx=5, pady=5)
        self.var_erledigt = tk.IntVar(self)
        ttk.Checkbutton(form_frame, text="Erledigt", variable=self.var_erledigt).grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.btn_save = ttk.Button(form_frame, text="Prüfung speichern", command=self.save_pruefung)
        self.btn_save.grid(row=5, column=0, columnspan=2, pady=10)
        self.tree = ttk.Treeview(self, columns=("id", "anlage_name", "datum", "pruefnotiz", "wiederholung", "erledigt"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("anlage_name", text="Anlage")
        self.tree.heading("datum", text="Datum")
        self.tree.heading("pruefnotiz", text="Prüfnotiz")
        self.tree.heading("wiederholung", text="Wiederholung (Monate)")
        self.tree.heading("erledigt", text="Erledigt")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_anlagen(self):
        conn = sqlite3.connect("instandhaltung.db")
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("SELECT anlage_id, name FROM anlagen ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        self.anlage_id_map = {}
        anl_names = []
        for (aid, aname) in rows:
            self.anlage_id_map[aname] = aid
            anl_names.append(aname)
        self.combo_anlage['values'] = anl_names
        if anl_names:
            self.combo_anlage.current(0)

    def save_pruefung(self):
        anlage_name = self.combo_anlage.get()
        anlage_id = self.anlage_id_map.get(anlage_name, None)
        datum = self.entry_datum.get()
        pruefnotiz = self.text_pruefnotiz.get("1.0", tk.END).strip()
        wiederholung = self.entry_wiederholung.get()
        erledigt = self.var_erledigt.get()
        try:
            conn = sqlite3.connect("instandhaltung.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO wartungen (anlage_id, datum, pruefnotiz, wiederholung, erledigt)
                VALUES (?, ?, ?, ?, ?)
            """, (anlage_id, datum, pruefnotiz, wiederholung, erledigt))
            conn.commit()
            conn.close()
            messagebox.showinfo("Speichern", "Prüfung wurde gespeichert.")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {e}")

    def load_data(self):
        try:
            conn = sqlite3.connect("instandhaltung.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    w.id,
                    IFNULL(a.name, '') as anlage_name,
                    w.datum,
                    w.pruefnotiz,
                    w.wiederholung,
                    w.erledigt
                FROM wartungen w
                LEFT JOIN anlagen a ON w.anlage_id = a.anlage_id
                ORDER BY w.id
            """)
            rows = cursor.fetchall()
            conn.close()
            for item in self.tree.get_children():
                self.tree.delete(item)
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der Daten: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    wf = WartungenFenster(root)
    wf.mainloop()

