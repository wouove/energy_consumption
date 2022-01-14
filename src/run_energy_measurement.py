from datetime import datetime
import logging
import time

# from p1_client import P1client
# from measurement_storage import MeasurementStorer

if __name__ == '__main__':
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # p = P1client()
        # measurement_df = p.read_p1_connection()
        # m = MeasurementStorer()
        # m.save_measurement(measurement_df, timestamp)

        # import pandas as pd
        path = '/storage/test_20211210.txt'

        with open(path, 'w') as f:
            logging.info(f"Writes to log at {timestamp}")
            f.write(f"Test at {timestamp} \n")
        time.sleep(60)
