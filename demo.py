#!/usr/bin/env python3
import sqlite3
import pandas as pd
import os
import random
from datetime import datetime, timedelta

DB_FILE = "factory_demo.db"
CONFIG_FILE = "konfiguration_demo.xlsx"

def create_tables():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Tabelle für Fabriken
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS factories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')

    # Tabelle für Abteilungen (departments) – jede Abteilung gehört zu einer Fabrik
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            factory_id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (factory_id) REFERENCES factories(id)
        )
    ''')

    # Tabelle für Anlagen – jede Anlage gehört zu einer Abteilung
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department_id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        )
    ''')

    # Tabelle für Anlagenteile – jedes Teil gehört zu einer Anlage
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plant_parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_id INTEGER,
            part_name TEXT,
            description TEXT,
            FOREIGN KEY (plant_id) REFERENCES plants(id)
        )
    ''')

    # Tabelle für Pannen/Unfälle – hier wird auch der Schichttyp (Früh, Mittag, Nacht) festgehalten
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_part_id INTEGER,
            incident_date TEXT,
            shift TEXT,
            cause TEXT,
            description TEXT,
            FOREIGN KEY (plant_part_id) REFERENCES plant_parts(id)
        )
    ''')

    # Zusätzliche Tabellen für Motoren, Ersatzteile, Wartungen und Mitarbeiter (für humorvolle Demonstrationen)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS engines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            serial_number TEXT,
            model TEXT,
            description TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spare_parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            engine_id INTEGER,
            part_name TEXT,
            description TEXT,
            FOREIGN KEY (engine_id) REFERENCES engines(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maintenance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            engine_id INTEGER,
            maintenance_date TEXT,
            description TEXT,
            FOREIGN KEY (engine_id) REFERENCES engines(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            description TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("Tabellen erfolgreich erstellt!")

def create_config_excel():
    # Falls die Konfigurationsdatei noch nicht existiert, wird sie hier erzeugt.
    if not os.path.exists(CONFIG_FILE):
        # Abteilungen
        departments_df = pd.DataFrame({
            "name": ["Kaffee & Co", "Keks- und Backstube", "Schmunzeltechnik"],
            "description": [
                "Zuständig für den koffeinhaltigen Betrieb.",
                "Hier werden Keksomat und Backwaren produziert.",
                "Innovative Technik mit einem Augenzwinkern."
            ]
        })

        # Anlagen – mit Zuordnung zur Abteilung über den Namen der Abteilung
        plants_df = pd.DataFrame({
            "department": ["Kaffee & Co", "Kaffee & Co",
                           "Keks- und Backstube", "Keks- und Backstube", "Keks- und Backstube",
                           "Schmunzeltechnik", "Schmunzeltechnik"],
            "name": ["Bohnenzauber", "Espresso-Express",
                     "Keksfabrik", "Teigtraum", "Ofenzauber",
                     "Lachlabor", "Witzwerkstatt"],
            "description": [
                "Erzeugt magischen Kaffeegenuss.",
                "Schnellster Espresso-Service in der Galaxie.",
                "Hier rollen die Kekse vom Band.",
                "Wo Teigträume Wirklichkeit werden.",
                "Magische Wärme für perfekte Backkunst.",
                "Testlabor für humorvolle Innovationen.",
                "Hier werden die besten Gags geschmiedet."
            ]
        })

        # Anlagenteile – mit Zuordnung zur Anlage über den Anlagennamen
        plant_parts_data = [
            # Für Bohnenzauber
            {"plant": "Bohnenzauber", "part_name": "Kaffeemaschine", "description": "Bereitet perfekten Kaffee zu, wenn sie nicht streikt."},
            {"plant": "Bohnenzauber", "part_name": "Mahlwerk", "description": "Mahlt die Bohnen mit Präzision und einem Hauch Magie."},
            {"plant": "Bohnenzauber", "part_name": "Dampfboiler", "description": "Versorgt die Anlage mit Dampf – manchmal zu humorvoll."},
            # Für Espresso-Express
            {"plant": "Espresso-Express", "part_name": "Espressomaschine", "description": "Brüht Espresso so schnell, dass man kaum blinzelt."},
            {"plant": "Espresso-Express", "part_name": "Wasserpumpe", "description": "Sorgt für den nötigen Wasserschub."},
            {"plant": "Espresso-Express", "part_name": "Kaffeezähler", "description": "Zählt die Tassen, damit niemand zu wenig Kaffee bekommt."},
            # Für Keksfabrik
            {"plant": "Keksfabrik", "part_name": "Keksomat", "description": "Automatischer Keksproduzent, anfällig für klebrige Situationen."},
            {"plant": "Keksfabrik", "part_name": "Backofen", "description": "Hält die Kekse warm, wenn die Maschine versagt."},
            {"plant": "Keksfabrik", "part_name": "Teigmischer", "description": "Vermischt Zutaten mit viel Liebe (und Überraschungen)."},
            # Für Teigtraum
            {"plant": "Teigtraum", "part_name": "Keksomat", "description": "Erzeugt Kekse in hoher Geschwindigkeit – wenn er mal funktioniert."},
            {"plant": "Teigtraum", "part_name": "FlourMatic", "description": "Automatisiert das Mehl-Zuführen mit einem Hauch von Poesie."},
            {"plant": "Teigtraum", "part_name": "OfenX", "description": "Hält den Teig in Schach – meistens."},
            # Für Ofenzauber
            {"plant": "Ofenzauber", "part_name": "Backofen", "description": "Der Ofen, der immer warmherzig ist."},
            {"plant": "Ofenzauber", "part_name": "Keksautomat", "description": "Gibt Kekse aus, aber nur, wenn er in Stimmung ist."},
            # Für Lachlabor
            {"plant": "Lachlabor", "part_name": "Spaßgenerator", "description": "Erzeugt Lacher in regelmäßigen Abständen."},
            {"plant": "Lachlabor", "part_name": "Witzchip", "description": "Klein, aber oho – der Witzchip."},
            {"plant": "Lachlabor", "part_name": "Humorhub", "description": "Das Herzstück des Lachens."},
            # Für Witzwerkstatt
            {"plant": "Witzwerkstatt", "part_name": "Lachmaschine", "description": "Lacht, wenn es sein soll, und manchmal auch von selbst."},
            {"plant": "Witzwerkstatt", "part_name": "Gag-Modul", "description": "Ausgestattet mit den besten Gags der Branche."},
            {"plant": "Witzwerkstatt", "part_name": "Schmunzelheizung", "description": "Hält die Stimmung warm, selbst bei Kälte."},
        ]
        plant_parts_df = pd.DataFrame(plant_parts_data)

        # Schreibe die Daten in eine Excel-Datei mit mehreren Sheets
        with pd.ExcelWriter(CONFIG_FILE) as writer:
            departments_df.to_excel(writer, sheet_name="departments", index=False)
            plants_df.to_excel(writer, sheet_name="plants", index=False)
            plant_parts_df.to_excel(writer, sheet_name="plant_parts", index=False)

        print(f"Konfigurationsdatei '{CONFIG_FILE}' wurde erstellt.")
    else:
        print(f"Konfigurationsdatei '{CONFIG_FILE}' existiert bereits.")

def import_config_data():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Lese die Excel-Datei
    xls = pd.ExcelFile(CONFIG_FILE)

    # Füge eine Basis-Fabrik ein
    cursor.execute(
        "INSERT INTO factories (name, description) VALUES (?, ?)",
        ("Fabrik Fantasia", "Eine fantastische Fabrik, in der Humor und Technik aufeinandertreffen.")
    )
    factory_id = cursor.lastrowid

    # Importiere Abteilungen
    df_departments = pd.read_excel(xls, "departments")
    department_mapping = {}  # Mapping von Abteilungsname zu ID
    for _, row in df_departments.iterrows():
        cursor.execute(
            "INSERT INTO departments (factory_id, name, description) VALUES (?, ?, ?)",
            (factory_id, row["name"], row["description"])
        )
        department_mapping[row["name"]] = cursor.lastrowid

    # Importiere Anlagen
    df_plants = pd.read_excel(xls, "plants")
    plant_mapping = {}  # Mapping von Anlagenname zu ID
    for _, row in df_plants.iterrows():
        dep_id = department_mapping.get(row["department"])
        if dep_id:
            cursor.execute(
                "INSERT INTO plants (department_id, name, description) VALUES (?, ?, ?)",
                (dep_id, row["name"], row["description"])
            )
            plant_mapping[row["name"]] = cursor.lastrowid

    # Importiere Anlagenteile
    df_parts = pd.read_excel(xls, "plant_parts")
    for _, row in df_parts.iterrows():
        plant_id = plant_mapping.get(row["plant"])
        if plant_id:
            cursor.execute(
                "INSERT INTO plant_parts (plant_id, part_name, description) VALUES (?, ?, ?)",
                (plant_id, row["part_name"], row["description"])
            )

    conn.commit()
    conn.close()
    print("Konfigurationsdaten aus Excel erfolgreich importiert!")

def init_other_reference_data():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Mitarbeiter
    employees = [
        ("Ford Prefect", "Außerirdischer Berater", "Bringt galaktischen Humor in den Betrieb."),
        ("Arthur Dent", "Techniker", "Trotzt Pannen mit einem Handtuch und Gelassenheit."),
        ("Zaphod Beeblebrox", "Geschäftsführer", "Führt die Fabrik mit doppeltem Kopf und unkonventionellen Ideen."),
    ]
    cursor.executemany(
        "INSERT INTO employees (name, role, description) VALUES (?, ?, ?)",
        employees
    )

    # Motoren
    engines = [
        ("ENG-001", "Turbo-Lachmotor", "Antreibt nicht nur, sondern sorgt auch für unerwartete Lacher."),
        ("ENG-002", "Super-Schmunzel 3000", "Bekannt für charmante Geräusche beim Anlaufen.")
    ]
    cursor.executemany(
        "INSERT INTO engines (serial_number, model, description) VALUES (?, ?, ?)",
        engines
    )

    # Ersatzteile für Motoren
    spare_parts = [
        (1, "Glücksrad", "Ein Rad, das angeblich Pannen abwehrt."),
        (1, "Lachschelle", "Wird eingesetzt, wenn der Motor zu ernst wird."),
        (2, "Witzzylinder", "Ersetzt defekte Zylinder und sorgt für extra Humor.")
    ]
    cursor.executemany(
        "INSERT INTO spare_parts (engine_id, part_name, description) VALUES (?, ?, ?)",
        spare_parts
    )

    # Wartungen
    maintenance = [
        (1, "2023-02-20", "Regelmäßige Wartung mit Ölwechsel und Lachtests."),
        (2, "2023-07-15", "Wartung und Nachjustierung der Schmunzelfunktionen.")
    ]
    cursor.executemany(
        "INSERT INTO maintenance (engine_id, maintenance_date, description) VALUES (?, ?, ?)",
        maintenance
    )

    conn.commit()
    conn.close()
    print("Weitere Referenzdaten (Mitarbeiter, Motoren, Ersatzteile, Wartungen) wurden initialisiert!")

def generate_incidents():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Hole alle Anlagenteile (ID und Name)
    cursor.execute("SELECT id, part_name FROM plant_parts")
    plant_parts = cursor.fetchall()  # Liste von (id, part_name)
    if not plant_parts:
        print("Keine Anlagenteile gefunden, um Pannen zu generieren.")
        conn.close()
        return

    # Erstelle eine gewichtete Liste zur Auswahl von Anlagenteilen.
    weighted_parts = []
    for part in plant_parts:
        part_id, part_name = part
        weight = 2
        if "kaffeemaschine" in part_name.lower():
            weight = 5  # Kaffeemaschine häufiger
        elif "keksomat" in part_name.lower():
            weight = 1  # Keksomat seltener
        weighted_parts.extend([part_id] * weight)

    # Schichtplan:
    # Montag bis Freitag: Früh, Mittag, Nacht
    # Samstag: nur Früh (ab Mittag frei)
    # Sonntag: frei
    shifts = {
        0: ["Früh", "Mittag", "Nacht"],
        1: ["Früh", "Mittag", "Nacht"],
        2: ["Früh", "Mittag", "Nacht"],
        3: ["Früh", "Mittag", "Nacht"],
        4: ["Früh", "Mittag", "Nacht"],
        5: ["Früh"],
        6: []
    }

    # Erzeuge Pannen-Daten für jeden Tag im Jahr 2023
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    current_date = start_date

    incidents_inserted = 0

    while current_date <= end_date:
        weekday = current_date.weekday()  # Montag=0, Sonntag=6
        active_shifts = shifts.get(weekday, [])
        for shift in active_shifts:
            # Pro Schicht 3 bis 5 Einträge
            num_incidents = random.randint(3, 5)
            for _ in range(num_incidents):
                plant_part_id = random.choice(weighted_parts)
                # Hole den Teilnamen für individuelle Ursachenbeschreibung
                cursor.execute("SELECT part_name FROM plant_parts WHERE id = ?", (plant_part_id,))
                part_name = cursor.fetchone()[0].lower()
                if "kaffeemaschine" in part_name:
                    cause = "Kaffeemaschine kaputt"
                    description = "Die Kaffeemaschine produzierte zu wenig Kaffee – Notfall am Morgen!"
                elif "keksomat" in part_name:
                    cause = "Keksomat defekt"
                    description = "Der Keksomat blieb länger aus – die Kekse mussten warten."
                else:
                    cause = "Allgemeiner Defekt"
                    description = "Ein unerwarteter Fehler störte den Betrieb."
                incident_date = current_date.strftime("%Y-%m-%d")
                cursor.execute(
                    "INSERT INTO incidents (plant_part_id, incident_date, shift, cause, description) VALUES (?, ?, ?, ?, ?)",
                    (plant_part_id, incident_date, shift, cause, description)
                )
                incidents_inserted += 1
        current_date += timedelta(days=1)

    conn.commit()
    conn.close()
    print(f"Demodaten für Pannen wurden erfolgreich generiert ({incidents_inserted} Einträge)!")

def main():
    create_tables()
    create_config_excel()
    import_config_data()
    init_other_reference_data()
    generate_incidents()
    print("Alle Daten wurden erfolgreich befüllt!")

if __name__ == "__main__":
    main()

