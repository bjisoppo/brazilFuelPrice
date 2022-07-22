from six.moves import urllib
import os


class DownLoadFiles:

    def __init__(self, start: int, end: 2002, directory: str = 'csvfiles'):
        """
        :param dir: directory path or name where the csv files will be stored.
        If none is passed, it will assume a default name.
        :param start: start year
        :param end: end year
        """
        self.directory = directory
        self.create_dir()
        for year in range(start, end):
            for semester in range(1, 3):
                self.download_files(year, semester)

    def download_files(self, year: int, semester: int):
        """
        This method will download the csv file from gov.br website and save to specified directory.
        """
        # Due to a connection problem, the files were not completely downloaded,
        # so a recursion is required to guarantee gov.br files will be fully downloaded.
        url = f'https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/' \
              f'arquivos/shpc/dsas/ca/ca-{year}-0{semester}.csv'
        path = f'csvfiles\ca-{year}-0{semester}.csv'
        try:
            urllib.request.urlretrieve(url, path)
        except:
            self.download_files(year, semester)

    def create_dir(self):
        """
        This method is needed to make sure the directory exists, if not, it will add one.
        """
        dirExists = os.path.isdir(self.directory)
        if not dirExists:
            os.mkdir(self.directory)
