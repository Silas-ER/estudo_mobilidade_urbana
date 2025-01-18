
class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    def clean_data(self):
        self.df['Empresa'] = self.df['Empresa'].replace('CONCEIÇÃO', 'CONCEICAO')
        self.df['Mes_Ano'] = self.df['Mes'] + '/' + self.df['Ano'].astype(str)
    
    def viagens_mes(self):
        return self.df.groupby('Mes_Ano')['Qtd_viagens'].sum().reset_index()