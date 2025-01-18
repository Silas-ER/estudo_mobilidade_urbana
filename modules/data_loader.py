
import pandas as pd

class DataLoader:
    def __init__(self, start_year=2018, end_year=2022):
        self.start_year = start_year
        self.end_year = end_year

    def load_data(self):
        df = {}
        for year in range(self.start_year, self.end_year+1):
            if year <= 2020: 
                df[year] = pd.read_csv(f'data/01-dados-be-{year}-analitico.csv', encoding='latin1', sep=';')
                if 'Mês' in df[year].columns:
                    df[year].rename(columns={'Mês': 'Mes'}, inplace=True)
            else:
                df[year] = pd.read_csv(f'data/01-dados-be-{year}-analitico.csv')
                df[year].rename(columns={'Mês': 'Mes'}, inplace=True)
        
        for year in df:
            df[year]['Ano'] = year
        
        return pd.concat(df.values(), ignore_index=True)