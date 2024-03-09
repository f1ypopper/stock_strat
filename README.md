# Stock Analyzer

Analyze instrument ticks using Simple Moving Crossover Strategy to generate buy and sell signals

## Usage

**migrate.py**: Migrate csv data to Postgres DB

```
python3 migrate.py <instrument> -s <addresss> -d <db> -u <user> -p <password>
```

**analyze.py**: Analyze the instrument's ticks and plot signals
```
python3 analyze.py <path_to_csv> -s <addresss> -d <db> -u <user> -p <password>
```

## Testing
Test CSV data file for valid data types:
```
python3 -m unittest
```
## Results/Performance:
![Hindalco SMA crossover](images/hindalco_sma.png "SMA Crossover strategy using 50-day and 100-day moving averages")
SMA Crossover strategy using 50-day and 100-day moving averages