#analyze the instrument's ticks and create signals
import argparse
import pandas as pd
import numpy as np
import psycopg2
import matplotlib.pyplot as plt


def create_plot(df, instrument):
    plt.figure(figsize = (20,10))
    df['close'].plot(color = 'k', label= 'Close Price') 
    df['short_ma'].plot(color = 'b',label = '50-day SMA') 
    df['long_ma'].plot(color = 'g', label = '100-day SMA')
    plt.plot(df[df['position'] == 1].index, 
        df['short_ma'][df['position'] == 1], 
        '^', markersize = 10, color = 'g', label = 'buy')
    plt.plot(df[df['position'] == -1].index, 
        df['short_ma'][df['position'] == -1], 
        'v', markersize = 10, color = 'r', label = 'sell')
    plt.legend()
    plt.grid()
    plt.title(instrument)
    plt.show()

def SMA(df, short_ma=50, long_ma=100):
    df['short_ma'] = df.close.rolling(window=short_ma, min_periods=1).mean()
    df['long_ma'] = df.close.rolling(window=long_ma, min_periods=1).mean()
    df['signal'] = np.where(df['short_ma'] > df['long_ma'], 1.0, 0.0)
    df['position'] = df['signal'].diff() 

def main(conn, instrument):
    with conn.cursor() as cursor:
        #get column names
        cursor.execute("SELECT * FROM tick LIMIT 0;")
        columns = ([desc[0] for desc in cursor.description])
        cursor.execute("SELECT * FROM tick WHERE instrument_id=(SELECT id FROM instrument WHERE name=%s) ORDER BY timestamp;", (instrument,))
        ticks = cursor.fetchall()
        df = pd.DataFrame(ticks, columns=columns)
        df.close = (pd.to_numeric(df.close))
        df.timestamp = pd.to_datetime(df.timestamp)
        SMA(df)
        create_plot(df, instrument)        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Analyzer", description="analyze instrument's ticks and create signals")
    parser.add_argument('instrument')
    parser.add_argument('-s', '--server', default='localhost')
    parser.add_argument('-d', '--db',required=True)
    parser.add_argument('-u', '--user', required=True)
    parser.add_argument('-p', '--password', required=True)
    args = parser.parse_args()
    conn = psycopg2.connect(host=args.server, database=args.db, user=args.user, password=args.password)
    main(conn, args.instrument)