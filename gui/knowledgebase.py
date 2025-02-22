import tkinter as tk
from tkinter import ttk, messagebox
import os
import webbrowser
import json

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

class KnowledgebaseFenster(tk.Toplevel):
    def __init__(self, master=None, pdf_folder=None):
        super().__init__(master)
        self.title("Knowledgebase (PDF)")
        self.geometry("600x400")
        config = load_config()
        self.pdf_folder = pdf_folder or config.get("knowledgebase_path", "knowledgebase")
        self.create_widgets()
        self.load_pdf_list()

    def create_widgets(self):
        search_frame = ttk.Frame(self, padding=10)
        search_frame.pack(fill=tk.X)
        ttk.Label(search_frame, text="Suche:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.entry_search = ttk.Entry(search_frame, textvariable=self.search_var)
        self.entry_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry_search.bind("<KeyRelease>", lambda event: self.filter_pdf_list())
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.listbox.bind("<Double-Button-1>", lambda event: self.open_selected_pdf())
        btn_frame = ttk.Frame(self, padding=10)
        btn_frame.pack(fill=tk.X)
        btn_open = ttk.Button(btn_frame, text="PDF öffnen", command=self.open_selected_pdf)
        btn_open.pack(side=tk.LEFT)
        btn_refresh = ttk.Button(btn_frame, text="Aktualisieren", command=self.load_pdf_list)
        btn_refresh.pack(side=tk.LEFT, padx=5)

    def load_pdf_list(self):
        self.listbox.delete(0, tk.END)
        if not os.path.exists(self.pdf_folder):
            messagebox.showerror("Fehler", f"Ordner '{self.pdf_folder}' nicht gefunden.")
            return
        self.pdf_files = sorted([f for f in os.listdir(self.pdf_folder) if f.lower().endswith(".pdf")])
        for pdf in self.pdf_files:
            self.listbox.insert(tk.END, pdf)

    def filter_pdf_list(self):
        query = self.search_var.get().lower()
        self.listbox.delete(0, tk.END)
        for pdf in self.pdf_files:
            if query in pdf.lower():
                self.listbox.insert(tk.END, pdf)

    def open_selected_pdf(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Hinweis", "Bitte wählen Sie eine PDF-Datei aus.")
            return
        pdf_file = self.listbox.get(selected[0])
        pdf_path = os.path.join(self.pdf_folder, pdf_file)
        try:
            if os.name == 'nt':
                os.startfile(pdf_path)
            else:
                webbrowser.open(pdf_path)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Öffnen der PDF: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    kb = KnowledgebaseFenster(root)
    kb.mainloop()

