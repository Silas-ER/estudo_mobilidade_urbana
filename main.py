import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from services.graphs import plot_line_chart, plot_bilhetagem_comparativa, plot_top_linhas, plot_top_empresas
import matplotlib.pyplot as plt

# Carregamento de dados
df = {}
ano_df = 2018

# Laço para carregar os dados de 2018, 2019 e 2020 que tem as mesmas características
for i in range(3):
    df[ano_df] = pd.read_csv(f"data/01-dados-be-{ano_df}-analitico.csv", encoding='latin1', sep=';')
    ano_df += 1
# Carregamento dos dados de 2021 e 2022 que tem características diferentes dos demais
df[2021] = pd.read_csv("data/01-dados-be-2021-analitico.csv")
df[2022] = pd.read_csv("data/01-dados-be-2022-analitico.csv", encoding='latin1', sep=',')

# Renomeação de colunas para padronização
df[2018].rename(columns={'Mês': 'Mes'}, inplace=True)
df[2019].rename(columns={'Mês': 'Mes'}, inplace=True)
df[2021].rename(columns={'Mês': 'Mes'}, inplace=True)

ano_df = 2018

# Lão para adicionar a coluna de ano para identificação quando concatenar os dataframes
for i in range(len(df)):
    df[ano_df]['Ano'] = ano_df
    ano_df += 1

# Concatenação dos dataframes
dfs_bilhetagem = [df[2018], df[2019], df[2020], df[2021], df[2022]]
df_bilhetagem_geral = pd.concat(dfs_bilhetagem, ignore_index=True)

# Manipulação de dados
df_bilhetagem_geral['Empresa'] = df_bilhetagem_geral['Empresa'].replace('CONCEIÇÃO', 'CONCEICAO') # Correção de acentuação
df_bilhetagem_geral['Mes_Ano'] = df_bilhetagem_geral['Mes'].astype(str) + '/' + df_bilhetagem_geral['Ano'].astype(str) # Criação de coluna Mes_Ano

# Viagens por mês/ano
viagens_por_mes = df_bilhetagem_geral.groupby('Mes_Ano')['Qtd_Viagens'].sum().reset_index()

# Configuração da página
st.set_page_config(
    page_title="Mobilidade Urbana - Natal/RN",       
    page_icon="🚌",                     
    layout="wide",                      
    initial_sidebar_state="collapsed",   
)

# Construção da Página
st.title('Mobilidade Urbana - Natal/RN')
st.divider()
st.markdown('## Bilhetagem Eletrônica')
st.markdown("""
            A bilhetagem eletrônica é um sistema que permite a cobrança eletrônica de passagens em transportes públicos.
            Através da bilhetagem eletrônica é possível obter informações sobre a quantidade de passageiros transportados,
            valor arrecadado, entre outras informações.
            <br>
            Os dados utilizados para construção desta análise foram obtidos através do portal de <a href='http://dados.natal.br/dataset'>dados abertos</a> 
            da Prefeitura do Natal.
            <br><br>
        """, unsafe_allow_html=True)
st.divider()

st.markdown("""
            <h5>Objetivo Principal:</h5> 
            <p>Entender padrões e tendências de mobilidade urbana em Natal/RN.</p>
            <br>
            <h5>Objetivos Secundários:</h5>
            <ul>
                <li>Investigar a estrutura, características e qualidade dos dados;</li>
                <li>Identificar padrões, tendências, outliers e relações entre variáveis;</li>
                <li>Gerar informações relevantes e aplicáveis a partir da base de dados;</li>
                <li>Aplicar ferramentas e métodos aprendidos na disciplina para manipulação e visualização de dados.</li>
            </ul>
            <br>
            """, unsafe_allow_html=True)
st.divider()

# Análise dos dados
st.markdown('### Análise inicial dos dados')
st.markdown("""
                <p>
                    Inicicialmente buscamos padronizar as colunas dos dados, que foram recebidos em 5 arquivos csv distintos e 
                    com padrões diferentes.
                    <br>
                    Após a padronização, renomeamos alguns itens que tinham acentos que fugiam do padrão utilizado para exibição.
                    <br>
                    Por fim, criamos e realizamos a conversão da coluna 'Mes_Ano' para o formato de data, para facilitar a análise temporal.
                    E concatenamos todos os dataframes em um único dataframe para facilitar a análise no geral.
                </p>
            """, unsafe_allow_html=True)
st.divider()

# Verficando os dados nulos e estatísticas descritivas
col1, col2 = st.columns([0.5, 1.5])
with col1: 
    st.markdown("""
                <p>
                    Utilizando o método <code>.isnull()</code> e <code>.sum()</code> 
                    conseguimos identificar a quantidade de valores nulos em cada coluna.
                </p>
                """, unsafe_allow_html=True)
    st.write(df_bilhetagem_geral.isnull().sum()) # Verificação de valores nulos
    
with col2: 
    st.markdown("""
                <p>
                    Utilizando o método <code>.describe()</code> para obter as estatisticas sobre as colunas.
                    Com isso, podemos ver que: 
                    <ul>
                        <li>o dataframe contém 4.734 linhas em 14 colunas númericas. Além da média e desvio padrão dessas colunas.</li>
                        <li>o valor mínimo de viagens é 1 e o máximo é 6.080.</li>
                        <li>Além disso, os valores minimos e maximos por categoria de passagem</li>
                        <li>Por fim, os quartis de valor!</li>
                    </ul>
                </p>
            """, unsafe_allow_html=True)
    st.markdown('')
    st.write(df_bilhetagem_geral.describe()) # Estatísticas descritivas  
    
# Análise de correlação e outliers
col1, col2 = st.columns([1, 1]) 
# Correlção de variáveis
with col1: 
    st.markdown("""
                <h5>Correlação de variáveis</h5>
                <p>
                    Utilizando o método <code>.corr()</code> com as colunas que possuem valores inteiros e floats
                    conseguimos criar um heatmap com os valores de correlação entre as colunas.
                    <br>
                    <ul>
                        <li>Sendo 1 uma correlação perfeita, quando uma variável aumenta a outra também aumenta;</li>
                        <li>0 uma correlação nula, quando uma variável aumenta a outra não é afetada;</li>
                        <li>-1 uma correlação negativa, quando uma variável aumenta a outra diminui.</li>
                    </ul>
                </p>
                """, unsafe_allow_html=True)
    plt.figure(figsize=(10, 7.5))
    numeric_cols = df_bilhetagem_geral.select_dtypes(include=['float64', 'int64'])
    numeric_cols = numeric_cols.drop(columns=['Ano','Mes'])
    matriz_correlacao = numeric_cols.corr()
    heatmap = sns.heatmap(matriz_correlacao, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title("Heatmap de Correlação", fontsize=18)
    st.pyplot(plt.gcf())  

# Outliers de viagens     
with col2:
    st.markdown("""
                <h5>Outliers de viagens</h5>
                <p>
                    Afim de observar a presença de outliers na coluna 'Qtd_Viagens' optamos por fazer um boxplot.
                    <br>
                    <ul>
                        <li>A partir dele observamos que o valor limite inferior de viagens é o 0 e o limite superior é na casa dos 4.500.</li>
                        <li>Também podemos ver que o primeiro quartil está na casa das 500 viagens, segundo quartil (mediana) está na casa dos 1.200 ~ viagens e 
                    o terceiro quartil por volta das 2.200 viagens.</li>
                        <li>Também podemos observar a presença de outliers, que são os pontos fora do limite superior e inferior. Numa quantidade significativa e 
                    que devem ser descartados ou avaliados a partir de datas específicas para escolha de manter ou não na análise.</li>
                    </ul>
                </p>
                """, unsafe_allow_html=True)
    plt.figure(figsize=(4, 2))
    boxplot = sns.boxplot(data=df_bilhetagem_geral, x='Qtd_Viagens')
    plt.title("Distribuição de Qtd_Viagens", fontsize=12)
    plt.xlabel("Quantidade de Viagens", fontsize=8)
    plt.ylabel("Densidade", fontsize=8)
    st.pyplot(plt.gcf())
    
st.divider()

# Análise Temporal
st.markdown('### Análise temporal de uso')
st.markdown("""
            <p>
                Para a análise nesse caso extraimos os dados referentes a quantidade de viagens totais realizadas (por todas as linhas), somando-os e 
                agrupando pela coluna 'Mes_Ano' criada durante a limpeza e raspagem de dados.
                <br>
                Com isso, optamos por fazer um gráfico de linhas que expressaria da melhor forma a variação das viagens durante o tempo.
                <br>
            </p>
            """, unsafe_allow_html=True)

col1, col2 = st.columns([1.1, 0.9])
with col1: plot_line_chart(df_bilhetagem_geral)
st.divider()

# Análise Comparativa
st.markdown('### Análise dos tipos de bilhetagem')
st.markdown("""
            <p>
                Para a análise queriamos analisar os tipos de bilhetagem em relação a quantidade de viagens realizadas no total em todo o período, 
                afim de descobrir os tipos de clientes das linhas.
                <br>
                Para tal optamos por um gráfico de barras comparando os tipos de bilhetagem armazenadas no dataframe.
                <br>
            </p>
            """, unsafe_allow_html=True)

col1, col2 = st.columns([1.1, 0.9])
with col1: plot_bilhetagem_comparativa(df_bilhetagem_geral)
st.divider()

st.markdown('### Análise de volumes de viagem por linha')
st.markdown("""
            <p>
                Nesse caso, queriamos verificar o volume de viagens por linha, detectando o que acreditamos ser a maior demanda.
                <br>
                Filtramos também ordenando pelas top 10 linhas com maior quantidade de viagens, presumindo que essas são as com maiores demandas perante os usuários!
                <br>
                Com isso, optamos por fazer um gráfico de barras, mostrando os maiores quantidade de viagens por linha.
                <br>
            </p>
            """, unsafe_allow_html=True)

col1, col2 = st.columns([1.1, 0.9])
with col1: plot_top_linhas(df_bilhetagem_geral)
st.divider()

st.markdown('### Análise de volume de viagens por empresa')
st.markdown("""
            <p>
                Nesse caso optamos por fazer a análise de dados focada na quantidade de viagens por empresa apurando assim qual empresa teria maior impacto na mobilidade urbana.
                <br>
                Mantemos a ideia de um gráfico de barras que expressaria da melhor forma a variação das viagens por empresa.
                <br>
            </p>
            """, unsafe_allow_html=True)

col1, col2 = st.columns([1.1, 0.9])
with col1: plot_top_empresas(df_bilhetagem_geral)
