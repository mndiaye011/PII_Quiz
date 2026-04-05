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

    def create_tables(self):
        # Table Quiz
        self.db_connection.execute("""
            CREATE TABLE IF NOT EXISTS Quiz (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT DEFAULT ''
            );
        """)
        # Table User (nouveau)
        self.db_connection.execute("""
            CREATE TABLE IF NOT EXISTS User (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
        """)
        # Colonne quiz_id sur Question
        try:
            self.db_connection.execute(
                "ALTER TABLE Question ADD COLUMN quiz_id INTEGER REFERENCES Quiz(id) ON DELETE SET NULL;"
            )
        except Exception:
            pass
        # Colonne user_id sur Participant (nouveau)
        try:
            self.db_connection.execute(
                "ALTER TABLE Participant ADD COLUMN user_id INTEGER REFERENCES User(id) ON DELETE SET NULL;"
            )
        except Exception:
            pass
        # Colonne quiz_id sur Participant (nouveau - pour l'historique)
        try:
            self.db_connection.execute(
                "ALTER TABLE Participant ADD COLUMN quiz_id INTEGER REFERENCES Quiz(id) ON DELETE SET NULL;"
            )
        except Exception:
            pass
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