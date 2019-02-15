from psycopg2.extras import RealDictCursor
from .init_db import db_con


class Model:
    def __init__(self, table_name):
        self.conn = db_con()
        self.table_name = table_name

    def fetch(self, query, mode='all'):
        cursor = self.cursor()
        cursor.execute(query)
        return cursor.fetchall() if mode == 'all' else cursor.fetchone()

    def insert(self, columns, values):
        if len(columns) != len(values):
            #input doesnt match
            self.cursor().execute("INSERT INTO {} ({}) VALUES({})"
                                  .format(
                                      self.table_name,
                                      ",".join(columns),
                                      #add quotes to string values
                                      ",".join(['{}'.format(value) if isinstance(value, str) else value for value in values])
                                    )
                                )
        self.conn.commit()


    def select_query(self, columns=None, criteria=None):
        join_type = ", ".join(columns) if columns else '*'
        query = 'SELECT {} FROM {}'.format(join_type, self.table_name)
        if criteria:
            query = "{} WHERE {}".format(query, criteria)

        return query

    def select_all(self, columns=None, criteria=None):
        return self.fetch(self.select_query(columns, criteria))

    def select_one(self, columns=None, criteria=None):
        return self.fetch(self.select_query(columns, criteria), mode='one')

    def cursor(self):
        return self.conn.cursor(cursor_factory=RealDictCursor)


    def __del__(self):
        self.conn.close()
