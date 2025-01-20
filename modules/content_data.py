
import streamlit as st
from modules.visualizer import DataVisualizer
import pandas as pd

# Página de explicações dos dados
def content_data(df):

    visualizer = DataVisualizer(df) # Instanciando a classe DataVisualizer

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
    col1, col2, col3 = st.columns([0.6, 1.2, 0.6]) 
    # Correlção de variáveis
    with col2: 
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

        st.pyplot(visualizer.plot_heatmap())  

        st.markdown("""
                    <p>
                        Com base no heatmap podemos observar os seguintes resultados:
                        <br>
                        <ul>
                            <li>
                                Vemos que a maioria das variáveis tem uma alta relação com a quantidade de viagens, 
                                exceto a Integracao_Complementar e a Tarifa_Social, isso pode se dar a esse tipo de passagem ser utilizada apenas
                                em ocasiões especificas na cidade. 
                            </li>
                            <li>
                                Também notamos o destaque das passagens Inteira_Especie e Inteira_Cartao que tem uma forte correlação com a quantidade de viagens, 
                                seguidas pelas Gratuito_BT, Estudante_BT e Vale_Transporte. Além das Integracao_Plena, Gratuito_Cartao e Estudante_Cartao. Isso mostra que 
                                são os métodos de pagamento mais determinantes para o transporte público.
                            </li>
                            <li>
                                Já dentre a correlação entre os meios de pagamento podemos destacar que há uma correlação do Estudante_Cartao e Estudante_BT, assim como
                                Gratuito_Cartao e Gratuito_BT por ambos serem basicamente variações do mesmo método de pagamento, sendo um em espécie e outro eletrônico.
                                As coisas ficam mais interessantes ao ver a relação entre Vale_transporte e a Integracao_Plena, além das Inteira_Cartao e Inteira_Especie, isso mostra
                                uma tendencia de uso similar entre esses métodos de pagamento nas viagens.
                            </li>
                        </ul>
                    </p>
                    """, unsafe_allow_html=True)    

    # Outliers de viagens   
    col1, col2, col3 = st.columns([0.1, 1.8, 0.1]) 
    with col2:
        st.markdown("""
                    <h5>Distribuição de variáveis</h5>
                    <p>
                        Afim de observar as variáveis que consideramos mais relevantes, optamos por plotar um boxsplot delas, sendo:
                        <br>
                        <ul>
                            <li>Qtd_Viagens - Representa diretamente o comportamento do uso;</li>
                            <li>Vale_Transporte - Importante para análise de subsídios e uso;</li>
                            <li>Inteira_Especie - Alta dispersão pode indicar padrões interessantes;</li>
                            <li>Integração_Plena - Muitos outliers e relevância no contexto de integração;</li>
                            <li>Gratuito_BT - Muitos outliers, útil para investigar anomalias;</li>
                            <li>Estudante_Cartao - Provavelmente relevante no contexto de análise por público.</li>
                        </ul>
                    </p>
                    """, unsafe_allow_html=True)

        st.pyplot(visualizer.plot_boxplot())
        
    st.divider()