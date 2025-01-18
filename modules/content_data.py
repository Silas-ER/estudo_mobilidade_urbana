
import streamlit as st
from modules.visualizer import DataVisualizer

# Página de explicações dos dados
def content_data(df):

    DataVisualizer(df) # Instanciando a classe DataVisualizer

    st.title('Mobilidade Urbana - Natal/RN')
    st.divider()

    st.markdown('## Bilhetagem Eletrônica')
    st.markdown("""
                A bilhetagem eletrônica é um sistema que permite a cobrança eletrônica de passagens em transportes públicos.
                Através da bilhetagem eletrônica é possível obter informações sobre a quantidade de passageiros transportados,
                valor arrecadado, entre outras informações.
                <br>
                Os dados utilizados para construção desta análise foram obtidos através do portal de <a href='http://dados.natal.br/dataset'>dados abertos</a> 
                da Prefeitura do Natal e abrangem de 2018 a 2022.
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
        st.write(df.isnull().sum()) # Verificação de valores nulos
    
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
        df_to_describe = df.drop(columns=['Ano', 'Mes', 'Linha'])
        st.write(df_to_describe.describe()) # Estatísticas descritivas  
    st.divider()  

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

        st.pyplot(DataVisualizer.plot_heatmap)  

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

        st.pyplot(DataVisualizer.plot_boxplot)
        
    st.divider()