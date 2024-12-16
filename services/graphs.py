import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Gráfico de linhas para análise temporal
def plot_line_chart(df):
    df['Mes_Ano'] = pd.to_datetime(df['Mes_Ano'])
    df_temp = df.groupby('Mes_Ano')['Qtd_Viagens'].sum().reset_index()
    
    plt.figure(figsize=(12, 6))
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
    sns.barplot(data=df_bilhetagem, x='Total_Viagens', y='Tipo_Bilhetagem', palette='viridis')
    plt.title('Comparação dos Tipos de Bilhetagem')
    plt.xlabel('Total de Viagens')
    plt.ylabel('Tipo de Bilhetagem')
    
    # Renderizar o gráfico no Streamlit
    st.pyplot(plt)

# Função para Top 10 Linhas
def plot_top_linhas(df):
    top_linhas = df.groupby('Linha')['Qtd_Viagens'].sum().reset_index()
    top_linhas = top_linhas.sort_values(by='Qtd_Viagens', ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_linhas, x='Qtd_Viagens', y='Linha', palette='viridis')
    plt.title('Top 10 Linhas com Maior Volume de Viagens')
    plt.xlabel('Total de Viagens')
    plt.ylabel('Linhas')
    st.pyplot(plt)

# Função para Top 10 Empresas
def plot_top_empresas(df):
    top_empresas = df.groupby('Empresa')['Qtd_Viagens'].sum().reset_index()
    top_empresas = top_empresas.sort_values(by='Qtd_Viagens', ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_empresas, x='Qtd_Viagens', y='Empresa', palette='viridis')
    plt.title('Top 10 Empresas com Maior Volume de Viagens')
    plt.xlabel('Total de Viagens')
    plt.ylabel('Empresas')
    st.pyplot(plt)

# Função para análise comparativa entre períodos
def plot_comparacao_empresas(df, periodo1, periodo2):
    df_periodo1 = df[df['Mes_Ano'] == periodo1].groupby('Empresa')['Qtd_Viagens'].sum().reset_index()
    df_periodo1['Periodo'] = periodo1

    df_periodo2 = df[df['Mes_Ano'] == periodo2].groupby('Empresa')['Qtd_Viagens'].sum().reset_index()
    df_periodo2['Periodo'] = periodo2

    df_comparacao = pd.concat([df_periodo1, df_periodo2])

    plt.figure(figsize=(12, 6))
    sns.barplot(data=df_comparacao, x='Empresa', y='Qtd_Viagens', hue='Periodo', palette='viridis')
    plt.title('Comparação do Volume de Viagens Entre Empresas')
    plt.xlabel('Empresas')
    plt.ylabel('Quantidade de Viagens')
    plt.xticks(rotation=45)
    st.pyplot(plt)
    
# Função para análise sazonal por linha
def plot_sazonalidade_por_linha(df, linha_selecionada):
    df_linha = df[df['Linha'] == linha_selecionada]
    df_temp = df_linha.groupby('Mes_Ano')['Qtd_Viagens'].sum().reset_index()
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_temp, x='Mes_Ano', y='Qtd_Viagens', marker='o', color='royalblue')
    plt.title(f'Volume de Viagens da Linha {linha_selecionada} ao Longo do Tempo')
    plt.xlabel('Tempo (Mes/Ano)')
    plt.ylabel('Quantidade de Viagens')
    plt.xticks(rotation=45)
    st.pyplot(plt)