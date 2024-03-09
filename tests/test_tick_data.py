import unittest
import csv
import datetime

class TestTickData(unittest.TestCase):
    def test_values(self):
        with open('data/hindalco.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                #Test datetime
                self.assertTrue(datetime.datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S'), datetime)

                # Test close, high, low, open
                for field in ['close', 'high', 'low', 'open']:
                    self.assertIsInstance(float(row[field]), float)

                # Test volume
                self.assertIsInstance(int(row['volume']), int)

                # Test instrument
                self.assertIsInstance(row['instrument'], str)

if __name__ == '__main__':
    unittest.main()