import sys, os, json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMenuBar, QMenu, QAction, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8-sig") as f:
                return json.load(f)
        except Exception as e:
            print("Fehler beim Laden der Konfiguration:", e)
    # Standardwerte, falls config.json nicht existiert oder nicht geladen werden kann:
    return {
        "backup_path": "C:\\KaijuLOGIX\\Backup",
        "export_path": "C:\\KaijuLOGIX\\Export",
        "knowledgebase_path": "C:\\KaijuLOGIX\\Knowledgebase",
        "gui_mode": "neu"  # hier spielt der GUI-Modus im PyQt-Beispiel keine Rolle, da wir in PyQt arbeiten
    }

def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print("Fehler beim Speichern der Konfiguration:", e)

class DirectoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Verzeichnisse Einstellungen")
        self.setModal(True)
        self.resize(500, 250)
        self.config = load_config()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Backup/Restore
        hl_backup = QHBoxLayout()
        lbl_backup = QLabel("Backup/Restore Pfad:")
        self.le_backup = QLineEdit(self.config.get("backup_path", ""))
        btn_backup = QPushButton("Durchsuchen")
        btn_backup.clicked.connect(self.browse_backup)
        hl_backup.addWidget(lbl_backup)
        hl_backup.addWidget(self.le_backup)
        hl_backup.addWidget(btn_backup)
        layout.addLayout(hl_backup)

        # Export
        hl_export = QHBoxLayout()
        lbl_export = QLabel("Export Pfad:")
        self.le_export = QLineEdit(self.config.get("export_path", ""))
        btn_export = QPushButton("Durchsuchen")
        btn_export.clicked.connect(self.browse_export)
        hl_export.addWidget(lbl_export)
        hl_export.addWidget(self.le_export)
        hl_export.addWidget(btn_export)
        layout.addLayout(hl_export)

        # Knowledgebase
        hl_kb = QHBoxLayout()
        lbl_kb = QLabel("Knowledgebase Pfad:")
        self.le_kb = QLineEdit(self.config.get("knowledgebase_path", ""))
        btn_kb = QPushButton("Durchsuchen")
        btn_kb.clicked.connect(self.browse_kb)
        hl_kb.addWidget(lbl_kb)
        hl_kb.addWidget(self.le_kb)
        hl_kb.addWidget(btn_kb)
        layout.addLayout(hl_kb)

        # Speichern-Button
        btn_save = QPushButton("Einstellungen speichern")
        btn_save.clicked.connect(self.save_settings)
        layout.addWidget(btn_save)

    def browse_backup(self):
        directory = QFileDialog.getExistingDirectory(self, "Backup/Restore Pfad auswählen")
        if directory:
            self.le_backup.setText(directory)

    def browse_export(self):
        directory = QFileDialog.getExistingDirectory(self, "Export Pfad auswählen")
        if directory:
            self.le_export.setText(directory)

    def browse_kb(self):
        directory = QFileDialog.getExistingDirectory(self, "Knowledgebase Pfad auswählen")
        if directory:
            self.le_kb.setText(directory)

    def save_settings(self):
        self.config["backup_path"] = self.le_backup.text().strip()
        self.config["export_path"] = self.le_export.text().strip()
        self.config["knowledgebase_path"] = self.le_kb.text().strip()
        save_config(self.config)
        QMessageBox.information(self, "Einstellungen", "Verzeichnis-Einstellungen wurden gespeichert.\nBitte starte die Anwendung neu.")
        self.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Picasso - PyQt Mode")
        self.resize(1000, 600)
        self.config = load_config()
        self.initUI()

    def initUI(self):
        # Menüleiste erstellen
        menubar = self.menuBar()

        # Menü "Picasso"
        picasso_menu = menubar.addMenu("Picasso")
        act_beenden = QAction("Beenden", self)
        act_beenden.triggered.connect(self.close)
        picasso_menu.addAction(act_beenden)

        # Menü "Einstellungen"
        einstellungen_menu = menubar.addMenu("Einstellungen")
        act_verzeichnisse = QAction("Verzeichnisse", self)
        act_verzeichnisse.triggered.connect(self.open_verzeichnisse)
        einstellungen_menu.addAction(act_verzeichnisse)
        act_benutzer = QAction("Benutzer", self)
        act_benutzer.triggered.connect(lambda: QMessageBox.information(self, "Benutzer", "Benutzerverwaltung (Platzhalter)"))
        einstellungen_menu.addAction(act_benutzer)
        act_gui_modus = QAction("GUI-Modus", self)
        act_gui_modus.triggered.connect(lambda: QMessageBox.information(self, "GUI-Modus", "GUI-Modus wechseln (Platzhalter)"))
        einstellungen_menu.addAction(act_gui_modus)

        # Menü "INFO"
        info_menu = menubar.addMenu("INFO")
        act_readme = QAction("Readme", self)
        act_readme.triggered.connect(self.open_readme)
        info_menu.addAction(act_readme)
        act_about = QAction("Über", self)
        act_about.triggered.connect(self.open_about)
        info_menu.addAction(act_about)
        act_lizens = QAction("Lizens", self)
        act_lizens.triggered.connect(self.open_lizens)
        info_menu.addAction(act_lizens)
        act_kontakt = QAction("Kontakt", self)
        act_kontakt.triggered.connect(self.open_kontakt)
        info_menu.addAction(act_kontakt)

        # Zentraler Inhalt
        central = QWidget(self)
        self.setCentralWidget(central)
        vlayout = QVBoxLayout(central)
        label = QLabel("Willkommen im PyQt Ein-Fenster-Modus", self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24pt;")
        vlayout.addWidget(label)

    def open_verzeichnisse(self):
        dlg = DirectoryDialog(self)
        dlg.exec_()

    def open_readme(self):
        try:
            with open("readme.txt", "r", encoding="utf-8-sig") as f:
                content = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Readme konnte nicht geladen werden: {e}")
            return
        QMessageBox.information(self, "Readme", content)

    def open_about(self):
        about_text = "Picasso Instandhaltungstool\nVersion 1.0\nEntwickler: Dein Name\n© DigitalKaiju 2025"
        QMessageBox.information(self, "Über", about_text)

    def open_lizens(self):
        try:
            with open("lizens.txt", "r", encoding="utf-8-sig") as f:
                content = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Lizens konnte nicht geladen werden: {e}")
            return
        QMessageBox.information(self, "Lizens", content)

    def open_kontakt(self):
        kontakt_text = "Kontakt:\nEmail: support@kaijulogix.de\nTelefon: 01234-567890"
        QMessageBox.information(self, "Kontakt", kontakt_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

