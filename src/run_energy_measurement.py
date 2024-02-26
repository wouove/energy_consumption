from datetime import datetime, timezone

from p1_client import P1client
from measurement_storage import MeasurementStorer
from influxdb_client import InfluxdbClient

if __name__ == '__main__':
    timestamp = datetime.now(timezone.utc)
    timestamp_string = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    p = P1client()
    measurement_df, measurement_dict = p.read_p1_connection()
    m = MeasurementStorer()
    m.save_measurement(measurement_df, timestamp_string)
    influxdb_client = InfluxdbClient(
        host="localhost",
        port=8086
    )
    influxdb_client.store_measurement(measurement_dict, timestamp)
