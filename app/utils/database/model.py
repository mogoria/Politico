from psycopg2.extras import RealDictCursor
from . import init_db

class Model:
    conn=init_db.db_con()

    def __init__(self):
        if self.conn_closed():
            Model.conn = init_db.db_con()

    @classmethod
    def fetch(cls, query, mode='all'):
        cursor = cls.cursor()
        cursor.execute(query)
        return cursor.fetchall() if mode == 'all' else cursor.fetchone()

    @classmethod
    def insert(cls, table_name, columns, values):
        if len(columns) != len(values):
            #input doesnt match
            raise Exception("Columns and Values don't match")

        cur = cls.conn.cursor()
        cur.execute("INSERT INTO {} ({}) VALUES({})"
                                .format(
                                    table_name,
                                    ",".join(columns),
                                    #add quotes to string values
                                    ",".join(["'{}'".format(value) if isinstance(value, str) else value for value in values])
                                )
                            )
        cls.conn.commit()

    @classmethod
    def select_query(cls, table_name, columns=None, criteria=None):
        join_type = ", ".join(columns) if columns else '*'
        query = 'SELECT {} FROM {}'.format(join_type, table_name)
        if criteria:
            query = "{} WHERE {}".format(query, criteria)

        return query

    @classmethod
    def select_all(cls, table_name, columns=None, criteria=None):
        return cls.fetch(cls.select_query(table_name, columns, criteria))

    @classmethod
    def select_one(cls, table_name, columns=None, criteria=None):
        return cls.fetch(cls.select_query(table_name, columns, criteria), mode='one')

    @classmethod
    def cursor(cls):
        return cls.conn.cursor(cursor_factory=RealDictCursor)
    @classmethod
    def close(cls):
        cls.conn.close()

    @classmethod
    def conn_closed(cls):
        return bool(cls.conn)
