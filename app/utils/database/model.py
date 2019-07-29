from psycopg2.extras import RealDictCursor
from psycopg2.sql import Identifier, Placeholder, SQL
from . import init_db


class Model:
    conn = init_db.db_con()

    def __init__(self):
        if self.conn_closed():
            Model.conn = init_db.db_con()

    @classmethod
    def fetch(cls, query, mode='all', arglist=None):
        cursor = cls.cursor()
        if arglist:
            cursor.execute(query, arglist)
        else:
            cursor.execute(query)
        result = cursor.fetchall() if mode == 'all' else cursor.fetchone()
        cursor.close()
        return result

    @classmethod
    def insert(cls, table_name, columns, values):
        if len(columns) != len(values):
            # input doesnt match
            raise Exception("Columns and Values don't match")

        cur = cls.conn.cursor()
        query = SQL("INSERT INTO {} ({}) VALUES({})").format(
                        Identifier(table_name),
                        SQL(', ').join(map(Identifier, columns)),
                        SQL(', ').join(Placeholder() * len(columns))
                        )
        cur.execute(query, values)
        cur.close()
        cls.conn.commit()

    @classmethod
    def select_query(cls, table_name, columns=None, criteria=None):
        query = QueryBuilder(table_name, columns).query()

        if criteria:
            query = QueryBuilder(table_name, columns).like(
                        criteria.get('column'))
        print(query.as_string(cls.conn))
        return query

    @classmethod
    def select_all(cls, table_name, columns=None, criteria=None):
        arglist = None
        if criteria:
            arglist = (criteria.get('value'),)
        return cls.fetch(cls.select_query(table_name, columns, criteria),
                         arglist=arglist)

    @classmethod
    def select_one(cls, table_name, columns=None, criteria=None):
        arglist = None
        if criteria:
            arglist = (criteria.get('value'),)
        print(arglist)
        return cls.fetch(cls.select_query(table_name, columns, criteria),
                         mode='one',
                         arglist=arglist)

    @classmethod
    def cursor(cls):
        return cls.conn.cursor(cursor_factory=RealDictCursor)

    @classmethod
    def close(cls):
        cls.conn.close()

    @classmethod
    def conn_closed(cls):
        return bool(cls.conn)


class QueryBuilder:
    def __init__(self, table, columns=None):
        self.table = table
        self.columns = columns

    def like(self, column):
        query = self.query() + SQL(" WHERE {} = {}").format(
                    Identifier(column),
                    Placeholder()
                )
        return query

    def query(self):
        if self.columns:
            query = SQL("SELECT {} FROM {}").format(
                    SQL(', ').join(
                        map(Identifier, self.columns)
                        ),
                    Identifier(self.table))
        else:
            query = SQL("SELECT * FROM {}").format(
                    Identifier(self.table))
        return query
