import os

import psycopg2
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

    # def exec_script_file(self, script_file_name: str) -> None:
    #     script_file = open('{0}\scripts\{1}'.format(os.path.dirname(__file__), script_file_name), 'r')
    #     with self.get_cursor() as cur:
    #         cur.execute(script_file.read())
    #         self.conn.commit()

    def get_cursor(self):
        return self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)



