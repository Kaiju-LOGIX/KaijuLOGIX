import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from repository import PannenRepository

class BerichteFenster(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Berichte")
        self.geometry("1000x700")
        self.repo = PannenRepository()
        self.create_widgets()
        self.load_filter_data()

    def create_widgets(self):
        # Filterbereich
        filter_frame = ttk.LabelFrame(self, text="Filter", padding=10)
        filter_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(filter_frame, text="Abteilung:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.abteilung_cb = ttk.Combobox(filter_frame, state="readonly")
        self.abteilung_cb.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Anlage:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.anlage_cb = ttk.Combobox(filter_frame, state="readonly")
        self.anlage_cb.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(filter_frame, text="Startdatum (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.start_date_entry = ttk.Entry(filter_frame, width=15)
        self.start_date_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Enddatum (YYYY-MM-DD):").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.end_date_entry = ttk.Entry(filter_frame, width=15)
        self.end_date_entry.grid(row=1, column=3, padx=5, pady=5)

        today = datetime.date.today()
        self.start_date_entry.insert(0, today.replace(day=1).strftime("%Y-%m-%d"))
        self.end_date_entry.insert(0, today.strftime("%Y-%m-%d"))

        btn_filter = ttk.Button(filter_frame, text="Filter anwenden", command=self.apply_filters)
        btn_filter.grid(row=2, column=0, columnspan=4, pady=10)

        # Vorschau der gefilterten Daten
        self.tree = ttk.Treeview(self, columns=("id", "abteilung", "anlage", "datum", "beschreibung"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("abteilung", text="Abteilung")
        self.tree.heading("anlage", text="Anlage")
        self.tree.heading("datum", text="Datum")
        self.tree.heading("beschreibung", text="Beschreibung")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Buttons für Export und Diagramme
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        btn_export = ttk.Button(btn_frame, text="Exportieren", command=self.export_data)
        btn_export.pack(side=tk.LEFT, padx=5)
        btn_chart = ttk.Button(btn_frame, text="Diagramme anzeigen", command=self.show_charts)
        btn_chart.pack(side=tk.LEFT, padx=5)

    def load_filter_data(self):
        abteilungen = self.repo.get_abteilungen()
        self.abteilung_cb['values'] = [""] + abteilungen
        self.abteilung_cb.current(0)
        anlagen = self.repo.get_anlagen()
        self.anlage_cb['values'] = [""] + anlagen
        self.anlage_cb.current(0)

    def apply_filters(self):
        abteilung = self.abteilung_cb.get().strip()
        anlage = self.anlage_cb.get().strip()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()

        rows = self.repo.get_filtered_pannen(abteilung, anlage, start_date, end_date)
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def export_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Dateien", "*.csv")])
        if not file_path:
            return

        data = []
        for child in self.tree.get_children():
            data.append(self.tree.item(child)['values'])

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("ID,Abteilung,Anlage,Datum,Beschreibung\n")
                for row in data:
                    line = ",".join([str(item) for item in row])
                    f.write(line + "\n")
            messagebox.showinfo("Export", f"Daten wurden erfolgreich exportiert nach:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Export fehlgeschlagen: {e}")

    def show_charts(self):
        result = self.repo.get_pannen_counts_by_abteilung()
        abteilungen = [row[0] for row in result]
        counts = [row[1] for row in result]

        if not abteilungen:
            messagebox.showinfo("Diagramme", "Keine Daten für Diagramme vorhanden.")
            return

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(abteilungen, counts, color="skyblue")
        ax.set_title("Anzahl Pannen pro Abteilung")
        ax.set_xlabel("Abteilung")
        ax.set_ylabel("Anzahl")
        plt.xticks(rotation=45, ha="right")

        chart_window = tk.Toplevel(self)
        chart_window.title("Diagramme")
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    bf = BerichteFenster(root)
    bf.mainloop()

