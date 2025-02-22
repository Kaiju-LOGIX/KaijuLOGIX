import json
import os
import sys

def load_config():
    config_file = "config.json"
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    return {"gui_mode": "alt"}  # Standard: alt

config = load_config()
mode = config.get("gui_mode", "alt")

if mode == "neu":
    # Starte den PyQt-Modus
    from PyQt5.QtWidgets import QApplication
    # Hier kannst du deinen PyQt-Hauptfenster-Code einbinden – z.B. aus main_pyqt.py
    from gui.main_pyqt import MainWindow  # Beispiel: MainWindow aus einer UI-gestützten Datei
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
elif mode == "alt":
    # Starte den alten Tkinter-Modus
    import tkinter as tk
    from gui.main_menu_tk import MainMenu
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
else:
    print("Unbekannter GUI-Modus in config.json:", mode)
