import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd
import matplotlib.ticker as ticker

# Gráfico de linhas para análise temporal
def plot_line_chart(df):
    df['Mes_Ano'] = pd.to_datetime(df['Mes_Ano'])
    df_temp = df.groupby('Mes_Ano')['Qtd_Viagens'].sum().reset_index()
    
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=df_temp, x='Mes_Ano', y='Qtd_Viagens')
    plt.title('Evolução do Uso de Transporte Público em Natal/RN')
    plt.xlabel('Tempo (mes/ano)')
    plt.ylabel('Quantidade de Viagens')
    #plt.xticks(rotation=90)
    st.pyplot(plt)

# Função para criar gráfico de barras dos tipos de bilhetagem
def plot_bilhetagem_comparativa(df):
    # Somar as colunas de tipos de bilhetagem
    bilhetagem_cols = [
        'Gratuito_Cartao', 'Gratuito_BT', 'Estudante_Cartao', 'Estudante_BT',
        'Vale_Transporte', 'Inteira_Cartao', 'Inteira_Especie', 'Tarifa_Social'
    ]
    df_bilhetagem = df[bilhetagem_cols].sum().reset_index()
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
    st.pyplot(plt)

# Função para Top 10 Linhas
def plot_top_linhas(df):
    top_linhas = df.groupby('Linha')['Qtd_Viagens'].sum().reset_index()
    top_linhas = top_linhas.sort_values(by='Qtd_Viagens', ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_linhas, x='Linha', y='Qtd_Viagens', palette='viridis')
    plt.title('Top 10 Linhas com Maior Volume de Viagens')
    plt.xlabel('Total de Viagens')
    plt.ylabel('Linhas')
    st.pyplot(plt)

# Função para Top 10 Empresas
def plot_top_empresas(df):
    top_empresas = df.groupby('Empresa')['Qtd_Viagens'].sum().reset_index()
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

    st.pyplot(plt)