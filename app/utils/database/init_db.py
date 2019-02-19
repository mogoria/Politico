from werkzeug.security import generate_password_hash
import os
import psycopg2


def db_con(db_url=None):

    if not db_url:
        db_url = os.getenv('DB_URL')
        print(db_url)
    con = psycopg2.connect(db_url)
    return con

def db_refresh(conn=None):
    if not conn:
        #create a connection if it doresn't exist
        conn = db_con()
    cur = conn.cursor()
    queries = drop_table_queries() + table_queries()

    for query in queries:
        cur.execute(query)
        conn.commit()
    conn.close()

def table_queries():

    users_table = """
    CREATE TABLE users(
        id SERIAL PRIMARY KEY,
        firstname VARCHAR(20) NOT NULL,
        lastname VARCHAR(20) NOT NULL,
        othername VARCHAR(20) NULL,
        phoneNumber VARCHAR(10) NOT NULL,
        email VARCHAR(30) NOT NULL UNIQUE,
        passportUri VARCHAR NULL,
        password VARCHAR NOT NULL,
        isAdmin BOOLEAN DEFAULT False
    )
    """

    parties_table = """
    CREATE TABLE parties(
        id SERIAL PRIMARY KEY,
        name VARCHAR(20) NOT NULL,
        hqAddress VARCHAR(20) NOT NULL,
        logoUrl VARCHAR NULL
    )
    """

    offices_table = """
    DROP TYPE IF EXISTS officeType;
    CREATE TYPE officeType AS ENUM('federal', 'legislative', 'state', 'local government');
    CREATE TABLE offices(
        id SERIAL PRIMARY KEY NOT NULL,
        type officeType NOT NULL,
        name VARCHAR(20) NOT NULL
    )
    """

    candidates_table = """
    CREATE TABLE candidates(
        office INT REFERENCES offices(id),
        candidate INT REFERENCES users(id) UNIQUE,
        party INT REFERENCES parties(id),
        PRIMARY KEY( office, candidate)
    )
    """

    votes_table = """
    CREATE TABLE votes(
        office INT REFERENCES offices(id),
        candidate INT REFERENCES candidates(candidate),
        voter INT REFERENCES users(id),
        PRIMARY KEY(voter, office)
    )
    """
    return [users_table, parties_table, offices_table, candidates_table, votes_table]

def admin_query():
    password = generate_password_hash('not-sure')
    query = """
    INSERT INTO users(firstname, lastname, phoneNumber, email, password, isAdmin)
        VALUES('John', 'Doe', 0700222333, 'admin@localhost.com', {}, True)
    """.format(password)
    return query

def drop_table_queries():
    drop_users = """
    DROP TABLE IF EXISTS users CASCADE
    """
    drop_parties = """
    DROP TABLE IF EXISTS parties CASCADE
    """
    drop_offices = """
    DROP TABLE IF EXISTS offices CASCADE
    """
    drop_candidates = """
    DROP TABLE IF EXISTS candidates CASCADE
    """
    drop_votes = """
    DROP TABLE IF EXISTS votes
    """
    return [drop_users, drop_parties, drop_offices, drop_candidates, drop_votes]

if __name__ == '__main__':
    try:
        db_refresh()
    except Exception as e:
        print("An error occured setting up db: {}".format(e))