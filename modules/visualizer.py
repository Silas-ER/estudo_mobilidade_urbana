
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

class DataVisualizer:
    def __init__(self, df):
        self.df = df
    
    def plot_heatmap(self):
        plt.figure(figsize=(10, 7.5))

        numeric_cols = self.df.select_dtypes(include=['float64', 'int64']) # Selecionar colunas numéricas
        cols_to_drop = ['Ano', 'Mes', 'Linha'] 
        existing_cols = [col for col in cols_to_drop if col in numeric_cols.columns] # Remover apenas as colunas que estão presentes no DataFrame
        numeric_cols = numeric_cols.drop(columns=existing_cols)

        # Criando matriz de correlação
        matriz_correlacao = numeric_cols.corr()
        sns.heatmap(matriz_correlacao, annot=True, cmap="coolwarm", fmt='.2f')
        plt.title("Heatmap de Correlação", fontsize=18)
        return plt.gcf()
    
    def plot_boxplot(self):
        # Filtrar somente as variáveis selecionadas
        variaveis_relevantes = ['Qtd_Viagens', 'Vale_Transporte', 'Inteira_Especie',
                                'Integracao_Plena', 'Gratuito_BT', 'Estudante_Cartao']
        df_filtrado = self.df[variaveis_relevantes]

        plt.figure(figsize=(16, 8))
        df_filtrado.boxplot(vert=False, patch_artist=True, widths=0.7)
        plt.title('Distribuição das Variáveis Relevantes (Boxplot)', fontsize=16)
        plt.xlabel('Valores', fontsize=14)
        plt.ylabel('Variáveis', fontsize=14)
        plt.grid(axis='x', linestyle='--', alpha=0.7)

        max_value = df_filtrado.max().max()
        tick_values = range(0, int(max_value) + 33200, 33200)
        plt.xticks(tick_values, fontsize=12)
        plt.yticks(fontsize=10)
        plt.tight_layout()

        return plt.gcf()
    
    # Função para plotar gráfico de linhas com base na quantidade de viagens por mês
    def plot_line_chart(self):

        self.df['Mes_Ano'] = pd.to_datetime(self.df['Mes_Ano'])
        df_temp = self.df.groupby('Mes_Ano')['Qtd_Viagens'].sum().reset_index()
        
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=df_temp, x='Mes_Ano', y='Qtd_Viagens')
        plt.title('Evolução do Uso de Transporte Público em Natal/RN')
        plt.xlabel('Tempo (mes/ano)')
        plt.ylabel('Quantidade de Viagens')
        sns.lineplot(data=df_temp, x='Mes_Ano', y='Qtd_Viagens', marker='o', color='blue') # Adicionando marcadores
        plt.grid(True, linestyle='--', alpha=0.7) # Adicionando grid
        #plt.xticks(rotation=90)
        
        return plt

    # Função que vai prever a tendencia de uso de transporte público para os próximos 3 anos com base nos anteriores
    def plot_tendencias_de_viagem(self):
        pass

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