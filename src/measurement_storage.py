import pandas as pd


class MeasurementStorer:
    def __init__(self):
        self.saver = CsvSaver()

    def save_measurement(self, df, timestamp):
        df_with_timestamp = self._add_timestamp_to_measurements(df, timestamp)
        self.saver.store_measurement(df_with_timestamp)

    @staticmethod
    def _add_timestamp_to_measurements(df, timestamp):
        return df.insert(0, "Timestamp", [timestamp], True)


class CsvSaver:
    def __init__(self):
        self.filepath = '/home/pi/python-projects'
        self.file = 'energy_measurement_data.csv'

    def store_measurement(self, df):
        previous_data_df = self._open_file()
        combined_df = previous_data_df.append(df, ignore_index=True)
        combined_df.to_csv(f'{self.filepath}/{self.file}', sep=';', index=False)

    def _open_file(self):
        df = pd.read_csv(f'{self.filepath}/{self.file}', sep=';')
        return df
