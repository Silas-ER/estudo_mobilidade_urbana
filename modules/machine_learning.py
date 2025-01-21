from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error, r2_score, mean_squared_error
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt

class MachineLearning:
    def __init__(self, df):
        self.df = df

    def regressao_linear(self):
        # Seleção de variáveis preditoras e alvo
        X = self.df[['Vale_Transporte', 'Estudante_BT', 'Inteira_Especie', 'Integracao_Plena']]
        y = self.df['Qtd_Viagens']

        # Divisão dos dados
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Treinamento do modelo
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Previsões
        y_pred = model.predict(X_test)

        # Avaliação do modelo
        rmse = root_mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        return rmse, r2
    
    def clustering_kmeans(self):
        kmeans = KMeans(n_clusters=3, random_state=42)
        self.df['Cluster'] = kmeans.fit_predict(self.df[['Vale_Transporte', 'Estudante_BT', 'Inteira_Especie', 'Integracao_Plena']])

        # Visualização
        sns.scatterplot(data=self.df, x='Inteira_Especie', y='Qtd_Viagens', hue='Cluster', palette='viridis')
        plt.title('Clusters de Usuários')

        return plt