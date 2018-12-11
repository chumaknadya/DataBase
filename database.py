import os

import psycopg2
import psycopg2.extras
from config import config

class Database(object):
    def __init__(self):
        self.conn = None

    def connect(self) -> None:
        try:
            # read connection parameters
            params = config()
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**params)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close_connection(self) -> None:
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')

    def exec_sql(self, sql: str) -> None:
        script_file = open('{0}/src/sql/{1}'.format(os.path.dirname(__file__), sql), 'r')
        with self.get_cursor() as cur:
            cur.execute(script_file.read())
            self.conn.commit()

    def get_cursor(self):
        return self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

if __name__ == "__main__":
  db = Database()
  db.connect()
  db.exec_sql("drop.sql")

