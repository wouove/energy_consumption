from unittest import TestCase
import pandas as pd
from measurement_storage import MeasurementStorer, CsvSaver


class TestCaching(TestCase):
    def setUp(self) -> None:
        self.timestamp = '2020-01-01 08:00:00'
        self.measurements_df = pd.DataFrame([[1, 2, 3, 4]], columns=['consumption_low', 'consumption_high',
                                                                       'production_low', 'production_high'])

    def test__add_timestamp_to_measurements(self):
        df_test = self.measurements_df.copy()
        df_test.insert(0, "Timestamp", self.timestamp)
        returned_df = MeasurementStorer._add_timestamp_to_measurements(self.measurements_df, self.timestamp)
        pd.testing.assert_frame_equal(self.measurements_df, returned_df)

    def test__combine_data(self):
        previous_measurements_df = pd.DataFrame([[5, 6, 7, 8]], columns=['consumption_low', 'consumption_high',
                                                                     'production_low', 'production_high'])
        combined_df = previous_measurements_df.append(self.measurements_df, ignore_index=True)
        returned_df = CsvSaver._combine_data(previous_measurements_df, self.measurements_df)
        pd.testing.assert_frame_equal(combined_df, returned_df)