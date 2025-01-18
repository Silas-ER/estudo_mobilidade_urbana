
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

class DataVisualizer:
    def __init__(self, df):
        self.df = df
    
    def plot_heatmap(self):
        plt.figure(figsize=(10, 7.5))
        
        numeric_cols = self.df.select_dtypes(include=['float64', 'int64'])
        numeric_cols = numeric_cols.drop(columns=['Ano', 'Mes', 'Linha'])
        matriz_correlacao = numeric_cols.corr()
        
        heatmap = sns.heatmap(matriz_correlacao, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title("Heatmap de Correlação", fontsize=18)

        return plt.gcf()
    
    def plot_boxplot(self):
        plt.figure(figsize=(4, 2))
        boxplot = sns.boxplot(data=self.df, x='Qtd_Viagens')
        plt.title("Distribuição de Qtd_Viagens", fontsize=12)
        plt.xlabel("Quantidade de Viagens", fontsize=8)
        plt.ylabel("Densidade", fontsize=8)

        return plt.gcf()
    
    def plot_line_chart(self):

        self.df['Mes_Ano'] = pd.to_datetime(self.df['Mes_Ano'])
        df_temp = self.df.groupby('Mes_Ano')['Qtd_Viagens'].sum().reset_index()
        
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=df_temp, x='Mes_Ano', y='Qtd_Viagens')
        plt.title('Evolução do Uso de Transporte Público em Natal/RN')
        plt.xlabel('Tempo (mes/ano)')
        plt.ylabel('Quantidade de Viagens')
        #plt.xticks(rotation=90)
        
        return plt

    def plot_bilhetagem_comparativa(self):
        # Somar as colunas de tipos de bilhetagem
        bilhetagem_cols = [
            'Gratuito_Cartao', 'Gratuito_BT', 'Estudante_Cartao', 'Estudante_BT',
            'Vale_Transporte', 'Inteira_Cartao', 'Inteira_Especie', 'Tarifa_Social'
        ]

        df_bilhetagem = self.df[bilhetagem_cols].sum().reset_index()
        df_bilhetagem.columns = ['Tipo_Bilhetagem', 'Total_Viagens']
        
        # Ordenar os dados para visualização
        df_bilhetagem = df_bilhetagem.sort_values(by='Total_Viagens', ascending=False)
        
        # Plotar gráfico de barras
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(data=df_bilhetagem, x='Total_Viagens', y='Tipo_Bilhetagem', palette='viridis')
        plt.title('Comparação dos Tipos de Bilhetagem')
        plt.xlabel('Total de Viagens')
        plt.ylabel('Tipo de Bilhetagem')
        
        # Formatador para mostrar valores reais no eixo X
        formatter = ticker.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', '.'))
        ax.xaxis.set_major_locator(ticker.MultipleLocator(12000000))  
        ax.xaxis.set_major_formatter(formatter)

        # Renderizar o gráfico no Streamlit
        return plt
    
    def plot_top_linhas(self):
        top_linhas = self.df.groupby('Linha')['Qtd_Viagens'].sum().reset_index()
        top_linhas = top_linhas.sort_values(by='Qtd_Viagens', ascending=False).head(10)

        plt.figure(figsize=(10, 6))
        sns.barplot(data=top_linhas, x='Linha', y='Qtd_Viagens', palette='viridis')
        plt.title('Top 10 Linhas com Maior Volume de Viagens')
        plt.xlabel('Total de Viagens')
        plt.ylabel('Linhas')

        return plt

    def plot_top_empresas(self):
        top_empresas = self.df.groupby('Empresa')['Qtd_Viagens'].sum().reset_index()
        top_empresas = top_empresas.sort_values(by='Qtd_Viagens', ascending=False).head(10)

        plt.figure(figsize=(10, 6))
        ax = sns.barplot(data=top_empresas, x='Qtd_Viagens', y='Empresa', palette='viridis')
        plt.title('Top 10 Empresas com Maior Volume de Viagens')
        plt.xlabel('Total de Viagens')
        plt.ylabel('Empresas')

        # Formatador para mostrar valores reais no eixo X
        formatter = ticker.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', '.'))
        ax.xaxis.set_major_locator(ticker.MultipleLocator(500000))  
        ax.xaxis.set_major_formatter(formatter)

        return plt