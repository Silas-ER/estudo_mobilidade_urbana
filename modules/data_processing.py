
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
    
    def data_formatter(self):
        self.df['Estudante'] = self.df['Estudante_BT'] + self.df['Estudante_Cartao']
        self.df['Gratuito'] = self.df['Gratuito_Cartao'] + self.df['Gratuito_BT']
        self.df['Inteira'] = self.df['Inteira_Cartao'] + self.df['Inteira_Especie']
        self.df['Integracao'] = self.df['Integracao_Plena'] + self.df['Integracao_Complementar']

        self.df = self.df.drop(columns=
            ['Estudante_BT', 'Estudante_Cartao', 'Gratuito_Cartao', 
             'Gratuito_BT', 'Inteira_Cartao', 'Inteira_Especie', 
             'Integracao_Plena', 'Integracao_Complementar'], inplace=True)
        