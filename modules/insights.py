import streamlit as st
from modules.visualizer import DataVisualizer

def insights(df):
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
    with col1: plot_line_chart()
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
