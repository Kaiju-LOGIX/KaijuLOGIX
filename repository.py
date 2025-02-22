import sqlite3

class DatabaseRepository:
    def __init__(self, db_path="instandhaltung.db"):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

class PannenRepository(DatabaseRepository):
    def get_filtered_pannen(self, abteilung="", anlage="", start_date="", end_date=""):
        conditions = []
        params = []
        if abteilung:
            conditions.append("abteilung = ?")
            params.append(abteilung)
        if anlage:
            conditions.append("anlage = ?")
            params.append(anlage)
        if start_date and end_date:
            conditions.append("datum BETWEEN ? AND ?")
            params.extend([start_date, end_date])
        query = "SELECT id, abteilung, anlage, datum, beschreibung FROM pannen"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            return cursor.fetchall()

    def get_pannen_counts_by_abteilung(self):
        query = "SELECT abteilung, COUNT(*) FROM pannen GROUP BY abteilung"
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    def insert_panne(self, panne_data):
        query = """
            INSERT INTO pannen 
            (datum, schicht, name, abteilung, anlage, anlagenteil, baugruppe, beschreibung, massnahme, fehlerkategorie, fehlerursache, ausfallzeit, prioritaet, melder)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, panne_data)
            conn.commit()

    def get_abteilungen(self):
        query = "SELECT name FROM abteilungen ORDER BY name"
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [row[0] for row in cursor.fetchall()]

    def get_anlagen(self):
        query = "SELECT name FROM anlagen ORDER BY name"
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [row[0] for row in cursor.fetchall()]

class ErsatzteileRepository(DatabaseRepository):
    def get_all_ersatzteile(self, search_query=""):
        query = """
            SELECT id, hersteller, typ, bauform, spannung, bestellnummer, lagerplatz, beschreibung, zusatz1, zusatz2, zusatz3 
            FROM ersatzteile
        """
        params = ()
        if search_query:
            query += " WHERE hersteller LIKE ? OR typ LIKE ? OR beschreibung LIKE ?"
            like_str = f"%{search_query}%"
            params = (like_str, like_str, like_str)
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def insert_ersatzteil(self, data):
        query = """
            INSERT INTO ersatzteile 
            (hersteller, typ, bauform, spannung, bestellnummer, lagerplatz, beschreibung, zusatz1, zusatz2, zusatz3)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()

    def get_all_hersteller(self):
        query = "SELECT DISTINCT hersteller FROM ersatzteile ORDER BY hersteller"
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return [row[0] for row in results if row[0]]

    def get_types_by_hersteller(self, hersteller):
        query = "SELECT DISTINCT typ FROM ersatzteile WHERE hersteller = ? ORDER BY typ"
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (hersteller,))
            results = cursor.fetchall()
            return [row[0] for row in results if row[0]]

class MotorenRepository(DatabaseRepository):
    def get_all_motoren(self, search_query=""):
        query = """
            SELECT id, motornummer, im_sw, g, bs, firma, neu, typ, seriennummer,
                   leistung, spannung, n1_min, n2_min, strom, cosinus_phi, lagerort, bemerkung
            FROM motoren
        """
        params = ()
        if search_query:
            query += " WHERE motornummer LIKE ? OR firma LIKE ? OR typ LIKE ? OR bemerkung LIKE ?"
            like_str = f"%{search_query}%"
            params = (like_str, like_str, like_str, like_str)
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def insert_motor(self, data):
        query = """
            INSERT INTO motoren 
            (motornummer, im_sw, g, bs, firma, neu, typ, seriennummer,
             leistung, spannung, n1_min, n2_min, strom, cosinus_phi, lagerort, bemerkung)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
class BenutzerRepository(DatabaseRepository):
    def get_all_users(self):
        query = "SELECT id, username, role FROM benutzer ORDER BY id ASC"
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    def insert_user(self, username, password, role):
        query = "INSERT INTO benutzer (username, password, role) VALUES (?, ?, ?)"
        import bcrypt
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (username, hashed, role))
            conn.commit()

    def update_user(self, user_id, username, role):
        query = "UPDATE benutzer SET username = ?, role = ? WHERE id = ?"
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (username, role, user_id))
            conn.commit()

    def delete_user(self, user_id):
        query = "DELETE FROM benutzer WHERE id = ?"
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            conn.commit()
