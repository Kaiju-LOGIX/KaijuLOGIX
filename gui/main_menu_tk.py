import tkinter as tk
from tkinter import ttk, messagebox

class MainMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Picasso")
        self.master.geometry("1000x600")
        self.create_menubar()
        self.create_widgets()

    def create_menubar(self):
        # Zuerst wird das menubar-Objekt erstellt:
        menubar = tk.Menu(self.master)
        
        # Menü "Picasso" mit "Beenden"
        picasso_menu = tk.Menu(menubar, tearoff=0)
        picasso_menu.add_command(label="Beenden", command=self.master.quit)
        menubar.add_cascade(label="Picasso", menu=picasso_menu)
        
        # Menü "Einstellungen" mit "Verzeichnisse", "Benutzer" und "GUI-Modus"
        einstellungen_menu = tk.Menu(menubar, tearoff=0)
        einstellungen_menu.add_command(label="Verzeichnisse", command=self.open_verzeichnisse)
        einstellungen_menu.add_command(label="Benutzer", command=self.open_benutzer)
        einstellungen_menu.add_command(label="GUI-Modus", command=self.open_gui_modus)
        menubar.add_cascade(label="Einstellungen", menu=einstellungen_menu)
        
        # Menü "INFO" mit "Readme", "Über", "Lizens" und "Kontakt"
        info_menu = tk.Menu(menubar, tearoff=0)
        info_menu.add_command(label="Readme", command=self.open_readme)
        info_menu.add_command(label="Über", command=self.open_about)
        info_menu.add_command(label="Lizens", command=self.open_lizens)
        info_menu.add_command(label="Kontakt", command=self.open_kontakt)
        menubar.add_cascade(label="INFO", menu=info_menu)
        
        self.master.config(menu=menubar)

    def create_widgets(self):
        header = ttk.Label(self.master, text="Willkommen bei Picasso", font=("Arial", 24))
        header.pack(pady=20)
        # Navigation über Buttons
        btn_frame = ttk.Frame(self.master)
        btn_frame.pack(pady=10)
        btn_pannen = ttk.Button(btn_frame, text="Pannenverwaltung", command=self.open_pannen)
        btn_wartungen = ttk.Button(btn_frame, text="Wartungen/Prüfungen", command=self.open_wartungen)
        btn_ersatzteile = ttk.Button(btn_frame, text="Ersatzteilverwaltung", command=self.open_ersatzteile)
        btn_motoren = ttk.Button(btn_frame, text="Motorenverwaltung", command=self.open_motoren)
        btn_knowledgebase = ttk.Button(btn_frame, text="Knowledgebase", command=self.open_knowledgebase)
        btn_pannen.grid(row=0, column=0, padx=10)
        btn_wartungen.grid(row=0, column=1, padx=10)
        btn_ersatzteile.grid(row=0, column=2, padx=10)
        btn_motoren.grid(row=0, column=3, padx=10)
        btn_knowledgebase.grid(row=0, column=4, padx=10)

    def open_pannen(self):
        from gui.pannenverwaltung import PannenFenster
        PannenFenster(self.master)

    def open_wartungen(self):
        from gui.wartungen import WartungenFenster
        WartungenFenster(self.master)

    def open_ersatzteile(self):
        from gui.ersatzteile import ErsatzteileFenster
        ErsatzteileFenster(self.master)

    def open_motoren(self):
        from gui.motoren import MotorenFenster
        MotorenFenster(self.master)

    def open_knowledgebase(self):
        from gui.knowledgebase import KnowledgebaseFenster
        KnowledgebaseFenster(self.master)

    def open_verzeichnisse(self):
        from gui.verzeichnisse import VerzeichnisseFenster
        VerzeichnisseFenster(self.master)

    def open_benutzer(self):
        from gui.benutzerverwaltung import BenutzerVerwaltungFenster
        BenutzerVerwaltungFenster(self.master)

    def open_gui_modus(self):
        from gui.gui_modus import GUIModusFenster
        GUIModusFenster(self.master)

    def open_readme(self):
        try:
            with open("readme.txt", "r", encoding="utf-8-sig") as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Fehler", f"Readme konnte nicht geladen werden: {e}")
            return
        self.show_text_window("Readme", content)

    def open_about(self):
        about_text = "Picasso Instandhaltungstool\nVersion 1.0\nEntwickler: Dein Name\n© DigitalKaiju 2025"
        self.show_text_window("Über", about_text)

    def open_lizens(self):
        try:
            with open("lizens.txt", "r", encoding="utf-8-sig") as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Fehler", f"Lizens konnte nicht geladen werden: {e}")
            return
        self.show_text_window("Lizens", content)

    def open_kontakt(self):
        kontakt_text = "Kontakt:\nEmail: support@kaijulogix.de\nTelefon: 01234-567890"
        self.show_text_window("Kontakt", kontakt_text)

    def show_text_window(self, title, text):
        window = tk.Toplevel(self.master)
        window.title(title)
        text_area = tk.Text(window, wrap=tk.WORD)
        text_area.insert("1.0", text)
        text_area.config(state=tk.DISABLED)
        text_area.pack(fill=tk.BOTH, expand=True)
        btn_close = ttk.Button(window, text="Schließen", command=window.destroy)
        btn_close.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
