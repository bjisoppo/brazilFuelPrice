import os
import pandas as pd
from fuelPriceByStateAndDate import ProcessData
from DownLoadFiles import DownLoadFiles
from BrazilUfCodeToName import BrazilUfCodeToName

# Initial parameters that will be passed to ProcessData class.
columns = ['Estado - Sigla', 'Produto']  # columns that should be grouped by
column_date = 'Data da Coleta'  # column containing the dates to be parsed
dirName = 'csvfiles'  # directory name the csv files will be stored

# Firstly, we are going to download the files from the site.
# True if you need to download the raw data, False if you don't.
# Notice it can take a while to download every file and it will take considerable space on hard drive
download_files_flag = False
if download_files_flag:
    DownLoadFiles(2004, 2022, dirName)

# It is not interesting to load all the files into the memory, therefore the files will be processed individually first
# and appended to csv_fuel_price_list, after that the csv_list will be merged into csv_fuel_price_dataframe
csv_fuel_price_list = []  # processed dataframes will be appended to this list
for file in os.listdir(f'./{dirName}'):
    fuel_dataframe = ProcessData(columns, column_date,
                                 file_name=file,
                                 dir_name=dirName,
                                 year=True,
                                 month=True,
                                 encoding='latin-1',
                                 sep=';',
                                 decimal=',')
    processed_data = fuel_dataframe.processedFuelDataFrame
    csv_fuel_price_list.append(processed_data)
csv_fuel_price_dataframe = pd.concat(csv_fuel_price_list, ignore_index=True)

# Changing the state postal code to state name.
print(csv_fuel_price_dataframe)
fuel_price_by_state_and_date = BrazilUfCodeToName().uf_to_name(csv_fuel_price_dataframe,
            columns=['Year', 'Month', 'NOME', 'Produto', 'Valor de Venda'],
            state_column='Estado - Sigla')

fuel_price_by_state_and_date.to_csv('fuel_price_by_state_year_and_month.csv',
                                    index=False,
                                    encoding='UTF-8',
                                    sep=';',
                                    decimal=',')