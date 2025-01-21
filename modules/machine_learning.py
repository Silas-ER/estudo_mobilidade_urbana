from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import root_mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans

import seaborn as sns
import matplotlib.pyplot as plt

class MachineLearning:
    def __init__(self, df):
        self.df = df

    def data_preprocessing(self):
        le = LabelEncoder()
        self.df['Mes'] = le.fit_transform(self.df['Mes'])

        #Dividindo entre variaveis de grupo e de teste
        x = self.df.drop('Qtd_Viagens', axis=1)
        y = self.df['Qtd_Viagens']
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        return x_train, x_test, y_train, y_test
    
    def model_regression(self):
        x_train, x_test, y_train, y_test = data_preprocessing(self)

        # Treinamento do modelo
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(x_train, y_train)

        # Previsão e avaliação
        y_pred = model.predict(x_test)
        mse = root_mean_squared_error(y_test, y_pred)
        
        return mse
    
    def model_regression_plot(self):
        x_train, x_test, y_train, y_test = data_preprocessing(self)

        plt.figure(figsize=(12, 8))
        plt.title('Evolução do Uso de Transporte Público em Natal/RN')
        plt.xlabel('')
        plt.ylabel('')

        sns.lineplot(data=?, x=?, y=?, marker='o', color='blue') 
        plt.grid(True, linestyle='--', alpha=0.7) 

        return plt

    def correlation_data(self):
        correlation = self.df.corr()
        heatmap = sns.heatmap(correlation, annot=True)
        
        return heatmap

    def linear_regression(self):
        x_train, x_test, y_train, y_test = data_preprocessing(self)

        model = LinearRegression()
        model.fit(x_train, y_train)

        coefficients = pd.Dataframe(model.coef_, x.columns, columns=['Coeficiente'])

        return coefficients
    
    def linear_regression_plot(self):
        x_train, x_test, y_train, y_test = data_preprocessing(self)

        coef = linear_regression(self)
        coef.plot(kind='bar')
        plt.title('Impacto dos Tipos de Pagamento nas Viagens')

        return plt

    def data_segmentation(self):
        # Normalização
        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(x)

        # Kmeans como Clusterning
        kmeans = KMeans(n_clusters=3, random_state=42)
        kmeans.fit(x_scaled)

        self.df['Cluster'] = kmeans.labels_

        pairplot = sns.pairplot(self.df, hue='Cluster')

        return pairplot
    
    