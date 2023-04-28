import sqlite3


class DatabaseConnection(object):

    def __init__(self, filename):
        self.connection = sqlite3.connect(filename, check_same_thread=False)

        self.SQL_CREATE_DOC = """
        CREATE TABLE documents (filename TEXT PRIMARY KEY, 
                                fulltext TEXT, 
                                summary TEXT,
                                nermarkup TEXT);
        """
        self.SQL_CREATE_ENTS = """
        CREATE TABLE IF NOT EXISTS entities (
            filename TEXT,
            entity TEXT,
            label TEXT,
            FOREIGN KEY(filename) REFERENCES documents(filename)
        );
        """
        self.SQL_SELECT_ALL_DOCS = "SELECT * FROM documents"
        self.SQL_SELECT_DOC_BY_ID = "SELECT * FROM documents WHERE filename=?"
        self.SQL_INSERT_DOC = "INSERT INTO documents (filename, fulltext, summary, nermarkup) VALUES (?, ?, ?, ?)"
        self.SQL_INSERT_ENTITY = "INSERT INTO entities (filename, entity, label) VALUES (?, ?, ?)"
        self.SQL_SELECT_ENTITIES_BY_DOC = "SELECT * FROM entities WHERE filename=?"
        self.SQL_SELECT_ALL_ENTS = "SELECT * FROM entities"

    def create_schema(self):
        try:
            self.connection.execute(self.SQL_CREATE_DOC)
            self.connection.execute(self.SQL_CREATE_ENTS)
            self.connection.commit()
        except sqlite3.OperationalError:
            print("Warning: the table was already created, ignoring...")

    def get_all_documents(self):
        cursor = self.connection.execute(self.SQL_SELECT_ALL_DOCS)
        return cursor.fetchall()

    def get_document_by_id(self, filename):
        cursor = self.connection.execute(self.SQL_SELECT_DOC_BY_ID, (filename,))
        return cursor.fetchone()

    def get_entities_by_doc(self, filename):
        cursor = self.connection.execute(self.SQL_SELECT_ENTITIES_BY_DOC, (filename,))
        return cursor.fetchall()
    
    def get_all_entities(self):
        cursor = self.connection.execute(self.SQL_SELECT_ALL_ENTS)
        return cursor.fetchall()
    
    def add_document(self, filename, fulltext, summary, nermarkup):
        try:
            self.connection.execute(self.SQL_INSERT_DOC, (filename, fulltext, summary, nermarkup))
            self.connection.commit()
        except sqlite3.IntegrityError:
            print(f"Warning: the document {filename} already exists in the table, ignoring...")
    
    def add_entity(self, filename, entity, label):
        cursor = self.connection.execute(
            "SELECT * FROM entities WHERE filename=? AND entity=? AND label=?", (filename, entity, label))
        result = cursor.fetchone()
        if result:
            # Entity already exists with this filename, don't add it again
            return
        self.connection.execute(self.SQL_INSERT_ENTITY, (filename, entity, label))
        self.connection.commit()


def create_db(db_name=None):
    dbname = db_name if db_name else 'tmp'
    connection = DatabaseConnection(f'{dbname}.sqlite')
    connection.create_schema()
    return connection


if __name__ == '__main__':
    create_db()
