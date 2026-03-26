import sqlite3

class DBServices:

    def __init__(self):
        self.cursor = None
        self.db_connection = None

    def connection(self):
        db_connection = sqlite3.connect(
            "./database/quizz.db", check_same_thread=False)
        db_connection.isolation_level = None
        db_connection.execute("PRAGMA foreign_keys = 1")
        self.cursor = db_connection.cursor()
        self.db_connection = db_connection

    def close(self):
        self.db_connection.close()

    # ── NOUVEAU : crée la table Quiz + colonne quiz_id ────────
    def create_tables(self):
        self.db_connection.execute("""
            CREATE TABLE IF NOT EXISTS Quiz (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT DEFAULT ''
            );
        """)
        # Ajoute quiz_id à Question si absente
        try:
            self.db_connection.execute(
                "ALTER TABLE Question ADD COLUMN quiz_id INTEGER REFERENCES Quiz(id) ON DELETE SET NULL;"
            )
        except Exception:
            pass  # colonne déjà existante
        self.db_connection.commit()

    def dict_factory(self, row):
        d = {}
        for idx, col in enumerate(self.cursor.description):
            d[col[0]] = row[idx]
        return d

    def executeSelectQuery(self, query):
        result = self.cursor.execute(query)
        rows = []
        for row in result.fetchall():
            rows.append(self.dict_factory(row))
        return rows

    def executeTransactionQuery(self, query):
        self.cursor.execute("begin")
        try:
            result = self.cursor.execute(query)
            self.cursor.execute("commit")
        except Exception as e:
            self.cursor.execute("rollback")
            raise e
        return result.fetchall()