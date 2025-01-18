
import seaborn as sns
import matplotlib.pyplot as plt

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