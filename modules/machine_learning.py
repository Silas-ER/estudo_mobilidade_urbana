from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import root_mean_squared_error, r2_score, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class MachineLearning:
    def __init__(self, df):
        self.df = df

    def data_preprocessing(self):
        le = LabelEncoder()

        self.df['Mes'] = le.fit_transform(self.df['Mes'])
        self.df['Empresa'] = le.fit_transform(self.df['Empresa'])

        self.df['Mes_Ano'] = pd.to_datetime(self.df['Mes_Ano'], format='%m/%Y')

        self.df['Mes_Num'] = self.df['Mes_Ano'].dt.month
        self.df['Ano_Num'] = self.df['Mes_Ano'].dt.year
        self.df = self.df.drop('Mes_Ano', axis=1)

        if self.df['Ano'].dtype == 'object':
            self.df['Ano'] = pd.to_numeric(self.df['Ano'], errors='coerce')
            
        #Dividindo entre variaveis de grupo e de teste
        x = self.df.drop('Qtd_Viagens', axis=1)
        y = self.df['Qtd_Viagens']

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        return x_train, x_test, y_train, y_test
    
    def model_regression(self):
        x_train, x_test, y_train, y_test = self.data_preprocessing()

        # Treinamento do modelo
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(x_train, y_train)

        # Previsão e avaliação
        y_pred = model.predict(x_test)
        mse = root_mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        return mse, mae, r2
    
    def model_regression_plot(self):
        self.df['Mes_Ano'] = pd.to_datetime(self.df['Ano_Num'].astype(str) + '-' + self.df['Mes_Num'].astype(str) + '-01')
        
        plt.figure(figsize=(12, 8))
        plt.title('Evolução do Uso de Transporte Público em Natal/RN')
        plt.xlabel('')
        plt.ylabel('')

        sns.lineplot(data=self.df, x='Mes_Ano', y='Qtd_Viagens', marker='o', color='blue') 
        plt.grid(True, linestyle='--', alpha=0.7) 

        return plt

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
    
    def linear_regression(self):
        x_train, x_test, y_train, y_test = self.data_preprocessing()

        columns_to_drop = ['Mes_Num', 'Ano_Num', 'Empresa', 'Mes', 'Ano', 'Linha']

        # Drop colunas em x_train e x_test
        x_train = x_train.drop(columns=columns_to_drop, axis=1)
        x_test = x_test.drop(columns=columns_to_drop, axis=1)

        model = LinearRegression()
        model.fit(x_train, y_train)

        coefficients = pd.DataFrame(model.coef_, index= x_train.columns, columns=['Coeficiente'])

        return coefficients
    
    def linear_regression_plot(self):
        coef = self.linear_regression()
        coef = coef.sort_values(by='Coeficiente', ascending=False)
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Coeficiente', y=coef.index, data=coef, palette='viridis')
        plt.title('Impacto dos Tipos de Pagamento nas Viagens')
        plt.xlabel('Valor do Coeficiente', fontsize=12)
        plt.ylabel('Variáveis', fontsize=12)
        plt.grid(alpha=0.3, linestyle='--')
        plt.tight_layout()
        
        return plt

