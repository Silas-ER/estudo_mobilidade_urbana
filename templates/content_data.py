
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
                    <ul>
                        <li>
                            Inicicialmente buscamos padronizar as colunas dos dados, que foram recebidos em 5 arquivos csv distintos e 
                            com padrões diferentes;
                        </li>
                        <li>
                            Após a padronização, renomeamos alguns itens que tinham acentos que fugiam do padrão utilizado para exibição;
                        </li>
                        <li>
                            Além disso agrupamos algumas colunas para facilitar nossa análise, por exemplo existiam duas colunas remetendo 
                            a diferentes formas de pagamento de um mesmo tipo de usuário, como o estudante que tinha 
                            Estudante_BT(Especie) e Estudante_Cartao;
                        </li>
                        <li>
                            Por fim, criamos e realizamos a conversão da coluna 'Mes_Ano' para o formato de data, para facilitar a análise temporal.
                            E concatenamos todos os dataframes em um único dataframe para facilitar a análise no geral.
                        </li>
                    </ul>
                """, unsafe_allow_html=True)
    st.divider()
    col1, col2, col3 = st.columns([0.5, 2, 0.5]) 
    with col2:
        st.markdown("""
                        <h5>
                            Utilizando o método <code>.isnull()</code> e <code>.sum()</code> 
                            conseguimos identificar a quantidade de valores nulos em cada coluna.
                        </h5>
                        <br>
                        """, unsafe_allow_html=True)
        st.write(df.isnull().sum().to_frame().transpose()) # Verificação de valores nulos
        
        st.markdown(""" <br>
                        <h5>
                            Utilizando o método <code>.describe()</code> para obter as estatisticas sobre as colunas.
                            Com isso, podemos ver que: 
                            <ul>
                                <li>o dataframe contém 4.734 linhas em 14 colunas númericas. Além da média e desvio padrão dessas colunas.</li>
                                <li>o valor mínimo de viagens é 1 e o máximo é 6.080.</li>
                                <li>Além disso, os valores minimos e maximos por categoria de passagem</li>
                                <li>Por fim, os quartis de valor!</li>
                            </ul>
                        </h5>
                    """, unsafe_allow_html=True)
        st.markdown('')
        col1, col2, col3 = st.columns([0.5, 2, 0.5]) 
        with col2:
            df_to_describe = df.drop(columns=['Ano', 'Mes', 'Linha'])
            st.write(df_to_describe.describe()) # Estatísticas descritivas  
    st.divider()  

    # Outliers de viagens   
    st.markdown('### Distribuição de variáveis')
    col1, col2, col3 = st.columns([0.1, 1.8, 0.1]) 
    with col2:
        st.markdown("""
                    <p>
                        Afim de observar as variáveis que consideramos mais relevantes, optamos por plotar um boxsplot delas, sendo:
                        <br>
                        <ul>
                            <li>Qtd_Viagens - Representa diretamente o comportamento do uso;</li>
                            <li>Vale_Transporte - Importante para análise de subsídios e uso;</li>
                            <li>Inteira - Alta dispersão pode indicar padrões interessantes;</li>
                            <li>Integracao - Muitos outliers e relevância no contexto de integração;</li>
                            <li>Gratuito - Muitos outliers, útil para investigar anomalias;</li>
                            <li>Estudante - Provavelmente relevante no contexto de análise por público.</li>
                        </ul>
                    </p>
                    """, unsafe_allow_html=True)

        st.pyplot(visualizer.plot_boxplot())
        
    with col2:
        st.markdown("""
                    <p>
                        Observações:
                        <br>
                        <ul>
                            <li>Como pode ser visto, todas as variáveis apresentam muitos outliers;</li>
                            <li>
                                Resumo de comportamento dos dados:
                                <ul>
                                    <li>Estudante e Gratuito possuem medianas próximas a zero, sugerindo que os valores são de níveis baixos;</li>
                                    <li>Vale_trasnporte e Inteira possuem maior dispersão, com medianas de níveis altos;</li>
                                    <li>Inteira seguida de Vale_transporte tem caixas bem amplas, indicando alta variabilidade nos valores;</li>
                                    <li>Integracao e Qtd_Viagens têm caixas menores, sugerindo maior concentração dos valores em uma faixa específica;</li>
                                    <li>Qtd_Viagens apresenta bigodes curtos, indicando que os valores estão muito concentrados em torno da mediana;</li>
                                    <li>Vale_Transporte e Inteira têm bigodes longos, sugerindo maior dispersão nos valores.</li>
                                </ul>
                            </li>
                            <li>
                                Observações Específicas das Variáveis:
                                <ul>
                                    <li>
                                        Estudante: 
                                        <ul>
                                            <li>Alta concentração de outliers em valores elevados;</li>
                                            <li>
                                                Mediana deslocada para valores baixos, 
                                                sugerindo que a maioria dos estudantes usa o serviço moderadamente, 
                                                mas há casos com uso extremo.
                                            </li>
                                        </ul>                                    
                                    </li>
                                    <li>
                                        Gratuito: 
                                        <ul>
                                            <li>Distribuição mais concentrada, com outliers significativos;</li>
                                            <li>
                                                A mediana está muito próxima do limite inferior, 
                                                indicando que a maioria dos dados é composta por valores baixos.
                                            </li>
                                        </ul>                                    
                                    </li>
                                    <li>
                                        Integracao: 
                                        <ul>
                                            <li>Mostra uma distribuição mais concentrada;</li>
                                            <li>
                                                Mediana deslocada para valores mais baixos, mas com muitos outliers, 
                                                indicando que poucos usuários fazem uso intenso da integração.
                                            </li>
                                        </ul>                                    
                                    </li>
                                    <li>
                                        Inteira: 
                                        <ul>
                                            <li>A variável com maior variabilidade (caixa ampla e bigodes longos);</li>
                                            <li>A mediana está posicionada de forma mais central, sugerindo uma distribuição mais equilibrada.</li>
                                        </ul>                                    
                                    </li>
                                    <li>
                                        Vale_Transporte: 
                                        <ul>
                                            <li>Alta dispersão com muitos outliers;</li>
                                            <li>
                                                A mediana está levemente deslocada para valores inferiores, 
                                                indicando que a maioria dos usuários utiliza o vale transporte de forma moderada.
                                            </li>
                                        </ul>
                                    </li>
                                    <li>
                                        Qtd_Viagens: 
                                        <ul>
                                            <li>Apresenta a menor dispersão entre todas as variáveis;</li>
                                            <li>Os dados são mais homogêneos, com poucos valores muito altos ou baixos.</li>
                                        </ul>
                                    </li>
                                </ul>
                            </li>
                        </ul>
                    </p>
                    """, unsafe_allow_html=True)
    st.divider()