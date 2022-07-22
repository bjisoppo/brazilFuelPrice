import os
import pandas as pd
from fuelPriceByStateAndDate import ProcessData
from DownLoadFiles import DownLoadFiles
from BrazilUfCodeToName import BrazilUfCodeToName

# Initial parameters that will be passed to ProcessData method.
columns = ['Estado - Sigla', 'Produto']
column_date = 'Data da Coleta'
dirName = 'csvfiles'
newDirName = 'handled_csv_files'

# Firstly, we are going to download the files from the site.
DownLoadFiles(2004, 2022, dirName)

# It is not interesting to load all the files into the memory, therefore the files will be processed individually first.
for file in os.listdir(f'./{dirName}'):
    fuel_dataframe = ProcessData(columns, column_date, file_name=file, dir_name=dirName,
                                 year=True, month=True, encoding='latin-1', sep=';', decimal=',')
    processed_fuel_dataframe = fuel_dataframe.save_to_csv(newDirName, encoding='latin-1', sep=';', decimal=',')

csv_list = []  # processed dataframes will be appended to this list
for file in os.listdir(f'./{newDirName}'):
    print(f'./{newDirName}/{file}')
    csv_list.append(pd.read_csv(f'./{newDirName}/{file}', encoding='latin-1', sep=';', decimal=','))
csv_merged = pd.concat(csv_list, ignore_index=True)
csv_merged.to_csv('fuel_price_by_state_year_and_month.csv', index=False, encoding='latin-1', sep=';', decimal=',')

# Changing the state postal code to state name.
fuel_price_by_state_and_date = BrazilUfCodeToName().uf_to_name(csv_merged,
            columns=['Year', 'Month', 'NOME', 'Produto', 'Valor de Venda'],
            state_column='Estado - Sigla')
