import pandas as pd


class MeasurementStorer:
    def __init__(self):
        self.saver = CsvSaver()

    def save_measurement(self, df, timestamp):
        df_with_timestamp = self._add_timestamp_to_measurements(df, timestamp)
        self.saver.store_measurement(df_with_timestamp)

    @staticmethod
    def _add_timestamp_to_measurements(df, timestamp):
        df.insert(0, "timestamp", timestamp)
        return df


class CsvSaver:
    def __init__(self):
        self.filepath = '/home/pi/python-projects/energy_consumption/src/'
        self.file = 'energy_measurement_data_house_2.csv'

    def store_measurement(self, df):
        previous_data_df = self._open_file()
        combined_df = self._combine_data(previous_data_df, df)
        combined_df.to_csv(f'{self.filepath}/{self.file}', sep=';', index=False)

    def _open_file(self):
        df = pd.read_csv(f'{self.filepath}/{self.file}', sep=';')
        return df

    @staticmethod
    def _combine_data(df1, df2):
        combined_df = df1.append(df2, ignore_index=True)
        return combined_df
