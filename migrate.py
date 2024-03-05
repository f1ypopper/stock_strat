#migrate data from csv file to db
import psycopg2
import psycopg2.extras
import csv

def create_init_tables(cursor):
    return cursor.execute(
        """
            DROP TABLE IF EXISTS instrument CASCADE;
            CREATE TABLE instrument(
                 id SERIAL PRIMARY KEY,
                 name VARCHAR(100)
            );
            DROP TABLE IF EXISTS tick;
            CREATE TABLE tick(
                 id SERIAL PRIMARY KEY,
                 timestamp TIMESTAMP,
                 close DECIMAL,
                 high DECIMAL,
                 low DECIMAL,
                 open DECIMAL,
                 volume INTEGER,
                 instrument_id INTEGER REFERENCES instrument ON DELETE CASCADE
            );
        """)

def load_csv(filename):
    with open(filename) as file:
        tick_reader = csv.DictReader(file, delimiter=',')
        for row in tick_reader:
            yield row

def insert_rows(cursor, data, instrument):
    cursor.execute("INSERT INTO instrument VALUES (DEFAULT, %s);", (instrument,))
    psycopg2.extras.execute_batch(cursor, "INSERT INTO tick VALUES(DEFAULT, %(datetime)s, %(close)s, %(high)s, %(low)s, %(open)s, %(volume)s, 1)", data)

conn = psycopg2.connect(host="localhost", database="testload", user="fish", password="test")
conn.autocommit = True

with conn.cursor() as cursor:
    create_init_tables(cursor)
    data = load_csv('data/hindalco.csv')
    insert_rows(cursor, data, "HINDALCO")