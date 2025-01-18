
import pandas as pd

class DataLoader:
    def __init__(self, start_year=2018, end_year=2022):
        self.start_year = start_year
        self.end_year = end_year

    def load_data(self):
        df = {}
        # Laço para carregar os dados de 2018, 2019 e 2020 que tem as mesmas características
        for year in range(self.start_year, self.end_year+1):
            if year <= 2020: 
                df[year] = pd.read_csv(f'data/01-dados-be-{year}-analitico.csv', encoding='latin1', sep=';')
                if 'Mês' in df[year].columns:
                    df[year].rename(columns={'Mês': 'Mes'}, inplace=True)

            # Carregamento dos dados de 2021 e 2022 que tem características diferentes dos demais        
            else:
                # Ano 2021
                if year == 2021:
                    df[year] = pd.read_csv(f'data/01-dados-be-{year}-analitico.csv')
                    if 'Mês' in df[year].columns:
                        df[year].rename(columns={'Mês': 'Mes'}, inplace=True)
                # Ano 2022
                else:
                    df[year] = pd.read_csv(f'data/01-dados-be-{year}-analitico.csv', encoding='latin1', sep=',')
                    if 'Mês' in df[year].columns:
                        df[year].rename(columns={'Mês': 'Mes'}, inplace=True)
        
        for year in df:
            df[year]['Ano'] = year
        
        # Retorna os dataframes concatenados em um só
        return pd.concat(df.values(), ignore_index=True)