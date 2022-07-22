import pandas as pd
import os


class ProcessData:

    def __init__(self, columns: list, column_date: str, file_name: str, dir_name: str = None, year: bool = False,
                 month: bool = False, day: bool = False, **kwargs):
        """

        :param columns: list; list with every column that should be in the group by, except any related to the date,
        the dates columns will be added later, based on the arguments.
        :param column_date: str; date column that should be parsed
        :param file_name: str; file's filename
        :param dir_name: str; the file's directory
        :param year: bool; True if the data should be grouped by year
        :param month: bool; True if the data should be grouped by month
        :param day: bool; True if the data should be grouped by day
        :param **kwargs: parameters from pandas read_csv and to_csv methods
        """
        self.column_date = column_date
        self.file_name = file_name
        if dir_name:
            file_path = f'./{dir_name}/{self.file_name}'
        else:
            file_path = f'./{self.file_name}'
        self.fuelDataFrame = pd.read_csv(file_path, **kwargs, parse_dates=[self.column_date], dayfirst=True)

        # Breaking the date column by year, month and date based on argument
        if year:
            self.fuelDataFrame['Year'] = pd.DatetimeIndex(self.fuelDataFrame[self.column_date]).year
            columns = columns + ['Year']
        if month:
            self.fuelDataFrame['Month'] = pd.DatetimeIndex(self.fuelDataFrame[self.column_date]).month
            columns = columns + ['Month']
        if day:
            self.fuelDataFrame['day'] = pd.DatetimeIndex(self.fuelDataFrame[self.column_date]).month
            columns = columns + ['day']

        self.treatedFuelDataFrame = self.fuelDataFrame.groupby(columns).mean()

    def processed_data(self):
        return self.treatedFuelDataFrame

    def save_to_csv(self, target_dir, **kwargs):
        dir_exists = os.path.isdir(target_dir)
        if not dir_exists:
            os.mkdir(target_dir)
        path_to_new_file = f'./{target_dir}/Handled-{self.file_name}'
        self.treatedFuelDataFrame.to_csv(path_to_new_file, **kwargs)
