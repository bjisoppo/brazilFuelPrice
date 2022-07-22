import pandas as pd


class BrazilUfCodeToName:

    def __init__(self):
        """
        This class is needed to change the states postal codes (UF) to its name.
        This is important to create geographic charts where the states are referenced by the name and not the code.
        """
        # Loading the UFs csv to url_path, cleaning the data, removing unwanted spaces, change the characters
        # to uppercase and changing the columns name to match the dataframe.
        self.url_path = 'https://raw.githubusercontent.com/leogermani/estados-e-municipios-ibge/master/estados.csv'
        self.estados_uf = pd.read_csv(self.url_path, sep=',', decimal=',')
        self.estados_uf['SIGLA'] = self.estados_uf['SIGLA'].str.strip()
        self.estados_uf['NOME'] = self.estados_uf['NOME'].str.upper()

    def uf_to_name(self, original_dataframe, state_column: str, columns: list = None):
        """
        :param original_dataframe: the dataframe with original data and postal codes
        :param columns: the columns needed. If none is passed, every column will be returned
        :param state_column: the column containing the states postal codes
        :return: dataframe with state names in upper case
        """
        self.estados_uf = self.estados_uf.rename(columns={'SIGLA': state_column})

        if not columns:
            columns = original_dataframe.columns

        join_original_dataframe_on_estados_uf = pd.merge(original_dataframe, self.estados_uf, on=state_column)
        data_by_uf = join_original_dataframe_on_estados_uf[columns]
        return data_by_uf
