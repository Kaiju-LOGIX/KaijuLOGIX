import sqlite3
import bcrypt
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

TABLES = {
    "benutzer": """
        CREATE TABLE IF NOT EXISTS benutzer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password BLOB,
            role TEXT DEFAULT 'user'
        );
    """,
    "pannen": """
        CREATE TABLE IF NOT EXISTS pannen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            abteilung TEXT,
            datum TEXT,
            schicht TEXT,
            name TEXT,
            anlage TEXT,
            anlagenteil TEXT,
            baugruppe TEXT,
            beschreibung TEXT,
            fehlerkategorie TEXT,
            fehlerursache TEXT,
            ausfallzeit TEXT,
            prioritaet TEXT,
            massnahme TEXT,
            melder TEXT
        );
    """,
    "motoren": """
        CREATE TABLE IF NOT EXISTS motoren (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            motornummer TEXT,
            im_sw TEXT,
            g TEXT,
            bs TEXT,
            firma TEXT,
            neu TEXT,
            typ TEXT,
            seriennummer TEXT,
            leistung TEXT,
            spannung TEXT,
            n1_min TEXT,
            n2_min TEXT,
            strom TEXT,
            cosinus_phi TEXT,
            lagerort TEXT,
            bemerkung TEXT
        );
    """,
    "ersatzteile": """
        CREATE TABLE IF NOT EXISTS ersatzteile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hersteller TEXT,
            typ TEXT,
            bauform TEXT,
            spannung TEXT,
            bestellnummer TEXT,
            lagerplatz TEXT,
            beschreibung TEXT,
            zusatz1 TEXT,
            zusatz2 TEXT,
            zusatz3 TEXT,
            bestand INTEGER DEFAULT 0,
            mindestbestand INTEGER DEFAULT 0,
            lieferant TEXT,
            einzelpreis REAL,
            waehrung TEXT
        );
    """,
    "wartungen": """
        CREATE TABLE IF NOT EXISTS wartungen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            anlage_id INTEGER,
            datum TEXT,
            pruefnotiz TEXT,
            wiederholung TEXT,
            erledigt INTEGER,
            FOREIGN KEY(anlage_id) REFERENCES anlagen(anlage_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
    """,
    "abteilungen": """
        CREATE TABLE IF NOT EXISTS abteilungen (
            abteilung_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
    """,
    "anlagen": """
        CREATE TABLE IF NOT EXISTS anlagen (
            anlage_id INTEGER PRIMARY KEY AUTOINCREMENT,
            abteilung_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY(abteilung_id) REFERENCES abteilungen(abteilung_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
    """,
    "anlagenteile": """
        CREATE TABLE IF NOT EXISTS anlagenteile (
            anlagenteil_id INTEGER PRIMARY KEY AUTOINCREMENT,
            anlage_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY(anlage_id) REFERENCES anlagen(anlage_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
    """
}

def create_tables(db_path="instandhaltung.db"):
    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            for table_name, query in TABLES.items():
                cursor.execute(query)
                logging.info(f"Tabelle '{table_name}' erstellt oder aktualisiert.")
            
            # Standardnutzer: admin und user
            def insert_user(username, password, role):
                cursor.execute("SELECT COUNT(*) FROM benutzer WHERE username = ?", (username,))
                if cursor.fetchone()[0] == 0:
                    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
                    cursor.execute("INSERT INTO benutzer (username, password, role) VALUES (?, ?, ?)",
                                   (username, hashed, role))
                    logging.info(f"Benutzer '{username}' eingefügt.")
                else:
                    logging.info(f"Benutzer '{username}' existiert bereits.")
            
            insert_user("admin", "admin", "admin")
            insert_user("user", "user", "user")
            
            conn.commit()
            logging.info("Datenbanksetup abgeschlossen.")
    except Exception as e:
        logging.error(f"Fehler beim Erstellen der Tabellen: {e}")

if __name__ == "__main__":
    create_tables()

