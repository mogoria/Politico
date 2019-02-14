import psycopg2
import os
from werkzeug.security import generate_password_hash


def db_con(db_url=None):
    
    if not db_url:
        db_url = os.getenv('DB_URL')

    con = psycopg2.connect(db_url)
    return con

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
    CREATE TYPE officeType AS ENUM('federal', 'legislative', 'state', 'local government')
    CREATE TABLE offices(
        id SERIAL PRIMARY KEY,
        type officeType NOT NULL,
        name VARCHAR(20) NOT NULL
    )
    """

    candidates_table = """
    CREATE TABLE candidates(
        office REFERENCES offices(id),
        user REFERENCES users(id),
        PRIMARY KEY( office, user)
    )
    """

    votes_table = """
    CREATE TABLE votes(
        office REFERENCES offices(id),
        candidate REFERENCES candidates(user),
        voter REFERENCES users(id),
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

