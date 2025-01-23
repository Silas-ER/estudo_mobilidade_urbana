from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import root_mean_squared_error, r2_score, mean_absolute_error
from sklearn.cluster import KMeans

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

class MachineLearning:
    def __init__(self, df):
        self.df = df

    def correlation_data(self):
        numeric_cols = self.df.select_dtypes(include=['float64', 'int64'])
        numeric_cols = numeric_cols.drop(['Linha'],axis=1)
        
        correlation = numeric_cols.corr()
        
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(correlation, annot=True, ax=ax)
        ax.set_title('Mapa de Calor de Correlação dos dados')

        return fig

    def clustering(self):
        #Pré Processamento
        scaler = StandardScaler()
        data_normalized = scaler.fit_transform(self.df[['Inteira', 'Vale_Transporte', 'Integracao', 'Qtd_Viagens', 'Estudante']])
        
        wcss = []
        for i in range(1, 11):
            kmeans = KMeans(n_clusters=i, random_state=0)
            kmeans.fit(data_normalized)
            wcss.append(kmeans.inertia_)

        fig, ax = plt.subplots()
        ax.plot(range(1, 11), wcss)
        ax.set_title('Método do Cotovelo')
        ax.set_xlabel('Número de Clusters')
        ax.set_ylabel('WCSS')
        
        return fig
    
    def kmeans_clustering(self, var1, var2):
        scaler = StandardScaler()
        data_normalized = scaler.fit_transform(self.df[['Inteira', 'Vale_Transporte', 'Integracao', 'Qtd_Viagens', 'Estudante']])
        
        var_indices = {
        'Inteira': 0,
        'Vale_Transporte': 1,
        'Integracao': 2,
        'Qtd_Viagens': 3,
        'Estudante': 4
        }

        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(data_normalized)
        self.df['Cluster'] = clusters

        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = sns.scatterplot(
            x=data_normalized[:, var_indices[var1]],  
            y=data_normalized[:, var_indices[var2]],  
            hue=clusters,             
            palette='viridis',        
            s=100,                    
            ax=ax
        )
        
        ax.set_title('Clusterização com K-Means (k=3)', fontsize=15)
        ax.set_xlabel(f'{var1} (Normalizado)', fontsize=12)
        ax.set_ylabel(f'{var2} (Normalizado)', fontsize=12)
        plt.legend(title='Cluster')

        return fig

    def group_and_train(self):
        # Agrupamento de viagens por ano com conversão de 'Ano' em inteiro
        self.df['Ano'] = self.df['Ano'].astype(int)  # Converte 'Ano' para tipo numérico
        df_grouped = self.df.groupby('Ano')['Qtd_Viagens'].sum().reset_index()

        # Definindo x como anos e y como quantidade
        x = df_grouped[['Ano']]
        y = df_grouped['Qtd_Viagens']

        # Separação dos dados
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        # Treinar modelo de regressão linear
        model = LinearRegression()
        model.fit(x_train, y_train)

        # Avaliação com métricas
        y_pred = model.predict(x_test)
        rmse = np.sqrt(root_mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)

        return model, df_grouped, rmse, r2, mae

    def forecast_and_plot(self):
        model, historico, rmse, r2, mae = self.group_and_train()

        # Previsões de próximo ano
        ano_maximo = historico['Ano'].max()
        proximo_ano = pd.DataFrame({'Ano': [ano_maximo + 1]})
        
        future_predictions = model.predict(proximo_ano)
        proximo_ano['Qtd_Viagens'] = future_predictions

        # Concatenar previsões ao histórico
        historico = pd.concat([historico, proximo_ano], ignore_index=True)

        # Plotar gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(historico['Ano'], historico['Qtd_Viagens'], label='Histórico', marker='o')
        plt.axvline(x=ano_maximo, linestyle='--', color='gray')
        plt.plot(proximo_ano['Ano'], proximo_ano['Qtd_Viagens'], label='Previsão', linestyle='--', marker='x', color='r')
        plt.title('Número de Viagens por Ano')
        plt.xlabel('Ano')
        plt.ylabel('Número de Viagens')
        
        ax = plt.gca()  # Obter o eixo atual
        ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
        plt.legend()
        plt.grid(True)
        
        return plt

    def group_and_train_by_company(self):
        self.df['Ano'] = self.df['Ano'].astype(int)
        self.df['Empresa'] = self.df['Empresa'].replace('CONCEIÇÃO', 'CONCEICAO') 

        model_dict = {}
        historico_dict = {}

        for empresa in self.df['Empresa'].unique():
            df_empresa = self.df[self.df['Empresa'] == empresa]
            df_grouped = df_empresa.groupby('Ano')['Qtd_Viagens'].sum().reset_index()
            x = df_grouped[['Ano']]
            y = df_grouped['Qtd_Viagens']

            # Verifique o número de amostras antes de dividir
            if len(df_grouped) > 1:
                x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
            else:
                x_train, y_train = x, y
                x_test, y_test = x, y
                print(f"Advertência: Apenas 1 ponto de dado disponível para a empresa {empresa}. Usando todos os dados para treinamento.")

            model = LinearRegression()
            model.fit(x_train, y_train)

            model_dict[empresa] = model
            historico_dict[empresa] = df_grouped

        return model_dict, historico_dict

    def forecast_and_plot_by_company(self):
        model_dict, historico_dict = self.group_and_train_by_company()

        plt.figure(figsize=(12, 8))

        for empresa, model in model_dict.items():
            historico = historico_dict[empresa]
            ano_maximo = historico['Ano'].max()

            # Preparar o próximo ano para previsão
            proximo_ano = pd.DataFrame({'Ano': [ano_maximo + 1]})
            future_predictions = model.predict(proximo_ano)
            proximo_ano['Qtd_Viagens'] = future_predictions

            historico = pd.concat([historico, proximo_ano], ignore_index=True)

            plt.plot(historico['Ano'], historico['Qtd_Viagens'], label=f'{empresa} (Histórico e Previsão)', marker='o')

        ax = plt.gca()
        ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))

        plt.title('Número de Viagens por Ano por Empresa')
        plt.xlabel('Ano')
        plt.ylabel('Número de Viagens')
        plt.legend()
        plt.grid(True)
        
        return plt