import streamlit as st
import pandas as pd
import numpy as np
from services.graphs import plot_line_chart, plot_bilhetagem_comparativa, plot_top_linhas, plot_top_empresas, plot_comparacao_empresas, plot_sazonalidade_por_linha

# Carregamento de dados
df = {}

ano_df = 2018

for i in range(3):
    df[ano_df] = pd.read_csv(f"data/01-dados-be-{ano_df}-analitico.csv", encoding='latin1', sep=';')
    ano_df += 1

df[2021] = pd.read_csv("data/01-dados-be-2021-analitico.csv")
df[2022] = pd.read_csv("data/01-dados-be-2022-analitico.csv", encoding='latin1', sep=',')

df[2018].rename(columns={'Mês': 'Mes'}, inplace=True)
df[2019].rename(columns={'Mês': 'Mes'}, inplace=True)
df[2021].rename(columns={'Mês': 'Mes'}, inplace=True)

ano_df = 2018

for i in range(len(df)):
    df[ano_df]['Ano'] = ano_df
    ano_df += 1

dfs_bilhetagem = [df[2018], df[2019], df[2020], df[2021], df[2022]]
df_bilhetagem_geral = pd.concat(dfs_bilhetagem, ignore_index=True)
df_bilhetagem_geral['Empresa'] = df_bilhetagem_geral['Empresa'].replace('CONCEIÇÃO', 'CONCEICAO')

# Conversão de colunas 
df_bilhetagem_geral['Mes_Ano'] = df_bilhetagem_geral['Mes'].astype(str) + '/' + df_bilhetagem_geral['Ano'].astype(str)

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
            <h5>Objetivo Principal:</h5> Entender padrões e tendências de mobilidade urbana em Natal/RN.
            <br>
            <h5>Objetivos Secundários:</h5>
            <ul>
                <li>Padrões de uso do transporte público ao longo do tempo: Como o número de viagens e os tipos de bilhetagem variaram ao longo dos anos e meses?</li>
                <li>Impacto da gratuidade e das integrações: Qual o efeito das tarifas gratuitas e integrações nos padrões de uso?</li>
                <li>Análise de sazonalidade: Existem períodos do ano (meses) com maior ou menor número de viagens?</li>
                <li>Distribuição do uso por linhas e empresas: Quais linhas ou empresas são mais utilizadas e em quais meses?</li>
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

col1, col2 = st.columns([0.5, 1.5])
with col1: 
    st.markdown("""
                <p>
                    Utilizando o método <code>.isnull()</code> e <code>.sum()</code> 
                    conseguimos identificar a quantidade de valores nulos em cada coluna.
                </p>
                """, unsafe_allow_html=True)
    st.write(df_bilhetagem_geral.isnull().sum())
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
    st.write(df_bilhetagem_geral.describe())   
st.divider()

# Análise Temporal
st.markdown('### Análise temporal de uso')
st.markdown("""
            <p>
                Para a análise nesse caso extraimos os dados referentes a quantidade de viagens totais realizadas (por todas as linhas), somando-os e 
                agrupando pela coluna 'Mes_Ano' criada durante a limpeza e raspagem de dados.
                <br>
                Com isso, optamos por fazer um gráfico de linhas que expressaria da melhor forma a variação das viagens durante o tempo.
            </p>
            """, unsafe_allow_html=True)

col1, col2 = st.columns([1.1, 0.9])
with col1:
    ##df_bilhetagem_geral.groupby('Mes_Ano')['Qtd_Viagens'].sum().st.pyplot(kind='line', title='Total de Viagens por Mês/Ano')
    plot_line_chart(df_bilhetagem_geral)

# Análise Comparativa
st.markdown('### Análise dos tipos de bilhetagem')
st.markdown("""
            <p>
                Para a análise queriamos analisar os tipos de bilhetagem em relação a quantidade de viagens realizadas no total em todo o período, 
                afim de descobrir os tipos de clientes das linhas.
                <br>
                Para tal optamos por um gráfico de barras comparando os tipos de bilhetagem armazenadas no dataframe.
            </p>
            """, unsafe_allow_html=True)

col1, col2 = st.columns([1.1, 0.9])
with col1:
    plot_bilhetagem_comparativa(df_bilhetagem_geral)

st.markdown('### Análise de volumes de viagem por linha')
st.markdown("""
            <p>
                Nesse caso, queriamos verificar o volume de viagens por linha, detectando o que acreditamos ser a maior demanda.
                <br>
                Filtramos também ordenando pelas top 10 linhas com maior quantidade de viagens, presumindo que essas são as com maiores demandas perante os usuários!
                <br>
                Com isso, optamos por fazer um gráfico de barras, mostrando os maiores quantidade de viagens por linha.
            </p>
            """, unsafe_allow_html=True)

col1, col2 = st.columns([1.1, 0.9])
with col1:
    plot_top_linhas(df_bilhetagem_geral)

st.markdown('### Análise de volume de viagens por empresa')
st.markdown("""
            <p>
                Nesse caso optamos por fazer a análise de dados focada na quantidade de viagens por empresa apurando assim qual empresa teria maior impacto na mobilidade urbana.
                <br>
                Mantemos a ideia de um gráfico de barras que expressaria da melhor forma a variação das viagens por empresa.
            </p>
            """, unsafe_allow_html=True)

col1, col2 = st.columns([1.1, 0.9])
with col1:
    plot_top_empresas(df_bilhetagem_geral)

# Filtro para selecionar a linha
linha_escolhida = st.selectbox('Selecione uma Linha:', df_bilhetagem_geral['Linha'].unique())
plot_sazonalidade_por_linha(df_bilhetagem_geral, linha_escolhida)

periodo1 = st.selectbox('Selecione o Primeiro Período:', df_bilhetagem_geral['Mes_Ano'].unique(), key='p1')
periodo2 = st.selectbox('Selecione o Segundo Período:', df_bilhetagem_geral['Mes_Ano'].unique(), key='p2')

if periodo1 != periodo2:
    plot_comparacao_empresas(df_bilhetagem_geral, periodo1, periodo2)
else:
    st.warning("Selecione dois períodos diferentes para comparar.")
    