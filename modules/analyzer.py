
class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    def clean_data(self):
        # Padronizar a empresa CONCEIÇÃO
        self.df['Empresa'] = self.df['Empresa'].replace('CONCEIÇÃO', 'CONCEICAO') 
        # Criar coluna Mes_Ano
        self.df['Mes'] = self.df['Mes'].astype(str)
        self.df['Ano'] = self.df['Ano'].astype(str)
        self.df['Empresa'] = self.df['Empresa'].astype(str)
        self.df['Mes_Ano'] = self.df['Mes'] + '/' + self.df['Ano']
    
    def viagens_mes(self):
        # Retorna a quantidade de viagens por mes/ano
        return self.df.groupby('Mes_Ano')['Qtd_viagens'].sum().reset_index()