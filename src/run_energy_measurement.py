from datetime import datetime

from p1_client import P1client
from measurement_storage import MeasurementStorer

if __name__ == '__main__':
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%m:%s")
    p = P1client()
    measurement_df = p.read_p1_connection()
    m = MeasurementStorer()
    m.save_measurement(measurement_df, timestamp)