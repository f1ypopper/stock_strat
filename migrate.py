#migrate instrument data from csv file to db
import psycopg2
import psycopg2.extras
import csv
import argparse

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

def main(conn, csv_path):
 with conn.cursor() as cursor:
    create_init_tables(cursor)
    data = load_csv(csv_path)
    insert_rows(cursor, data, data[0]['instrument'])   

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Analyzer", description="analyze instrument's ticks and create signals")
    parser.add_argument('csv', help='path to csv file')
    parser.add_argument('-s', '--server', default='localhost')
    parser.add_argument('-d', '--db',required=True)
    parser.add_argument('-u', '--user', required=True)
    parser.add_argument('-p', '--password', required=True)
    args = parser.parse_args()
    conn = psycopg2.connect(host=args.server, database=args.db, user=args.user, password=args.password)
    conn.autocommit = True
    main(conn, args.csv)

