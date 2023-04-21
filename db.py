import sys, sqlite3

SQL_CREATE = "CREATE TABLE entities (entity TEXT PRIMARY KEY, count INTEGER)"

class DatabaseConnection(object):

    def __init__(self, filename):
        self.connection = sqlite3.connect(filename, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS entities (
                label TEXT,
                text TEXT,
                count INTEGER,
                PRIMARY KEY (label, text)
            )
        ''')
        self.connection.commit()

    def get_cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def create_schema(self):
        try:
            self.connection.execute(SQL_CREATE)
        except sqlite3.OperationalError:
            print("Warning: 'entities' table was already created, ignoring...")

    def get(self, entity=None):
        if entity is not None:
            cursor = self.connection.execute(f"SELECT * FROM entities WHERE entity='{entity}'")
        else:
            cursor = self.connection.execute("SELECT * FROM entities")
        return cursor.fetchall()

    def get_entity_counts(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT label, text, count FROM entities")
        rows = cursor.fetchall()
        entity_counts = []
        for row in rows:
            entity_counts.append({'label': row[0], 'text': row[1], 'count': row[2]})
        return entity_counts


if __name__ == '__main__':
    dbname = sys.argv[1] if len(sys.argv) > 1 else 'tmp'
    connection = DatabaseConnection(f'{dbname}.sqlite')
    connection.create_schema()
