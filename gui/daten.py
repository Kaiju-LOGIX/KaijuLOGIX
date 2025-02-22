
import tkinter as tk
from tkinter import ttk, messagebox
from gui.exporter import ExportFenster

class DatenFenster(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Daten")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        btn_export = ttk.Button(frame, text="Exportieren", command=self.open_export)
        btn_export.pack(pady=10)
        btn_anpassen = ttk.Button(frame, text="Daten anpassen", command=self.open_anpassen)
        btn_anpassen.pack(pady=10)

    def open_export(self):
        ExportFenster(self)

    def open_anpassen(self):
        messagebox.showinfo("Daten anpassen", "Hier könnte ein Fenster zur Datenanpassung geöffnet werden.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatenFenster(root)
    root.mainloop()

