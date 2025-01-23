from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import root_mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans

import pandas as pd
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
        
        return mse
    
    def model_regression_plot(self):
        x_train, x_test, y_train, y_test = self.data_preprocessing()

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
        #numeric_cols = numeric_cols.drop(['Mes', 'Linha', 'Ano', 'Empresa'],axis=1)
        correlation = numeric_cols.corr()
        plt.figure(figsize=(10, 8))
        heatmap = sns.heatmap(correlation, annot=True)
        
        return plt

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

    def data_segmentation(self):
        x = self.df

        # Colunas a serem removidas
        columns_to_drop = ['Mes_Num', 'Ano_Num', 'Empresa', 'Mes', 'Ano', 'Linha']
        x = x.drop(columns=columns_to_drop, axis=1)

        # Normalização
        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(x)

        # KMeans para clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        kmeans.fit(x_scaled)

        self.df['Cluster'] = kmeans.labels_

        # Seleção de colunas relevantes para o pairplot
        selected_columns = ['Estudante', 'Gratuito', 'Inteira', 'Integracao', 'Qtd_Viagens', 'Cluster']
        pairplot = sns.pairplot(self.df[selected_columns], hue='Cluster')

        return pairplot
        """
        def plot_clusters_2D(df, x_col, y_col, cluster_column='Cluster'):
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=df, x=x_col, y=y_col, hue=cluster_column, palette='viridis', s=100)
            plt.title(f'Clusters com {x_col} e {y_col}', fontsize=16)
            plt.xlabel(x_col, fontsize=12)
            plt.ylabel(y_col, fontsize=12)
            plt.legend(title="Cluster", loc='upper right')
            plt.grid(alpha=0.5)
            plt.show()
        def plot_cluster_distribution(df, variable, cluster_column='Cluster'):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x=cluster_column, y=variable, palette='viridis', ci=None)
    plt.title(f'Distribuição de {variable} por Cluster', fontsize=16)
    plt.xlabel('Cluster', fontsize=12)
    plt.ylabel(variable, fontsize=12)
    plt.grid(alpha=0.5)
    plt.show()

    from sklearn.decomposition import PCA

def plot_pca_clusters(df, cluster_column='Cluster'):
    pca = PCA(n_components=2)
    data_scaled = StandardScaler().fit_transform(df.drop(columns=[cluster_column]))
    pca_result = pca.fit_transform(data_scaled)
    
    df['PCA1'] = pca_result[:, 0]
    df['PCA2'] = pca_result[:, 1]
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='PCA1', y='PCA2', hue=cluster_column, palette='viridis', s=100)
    plt.title('Clusters com Redução PCA (2D)', fontsize=16)
    plt.xlabel('PCA1', fontsize=12)
    plt.ylabel('PCA2', fontsize=12)
    plt.legend(title="Cluster", loc='upper right')
    plt.grid(alpha=0.5)
    plt.show()

    def plot_radar_chart(df, cluster_column='Cluster'):
    cluster_means = df.groupby(cluster_column).mean()
    categories = cluster_means.columns
    num_clusters = len(cluster_means)
    
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]  # Fechar o gráfico
    
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    
    for i in range(num_clusters):
        values = cluster_means.iloc[i].tolist()
        values += values[:1]  # Fechar o gráfico
        ax.plot(angles, values, label=f'Cluster {i}')
        ax.fill(angles, values, alpha=0.25)
    
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.title('Características Médias por Cluster', fontsize=16)
    plt.show()
        """