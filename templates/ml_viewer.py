import streamlit as st
from modules.machine_learning import MachineLearning

def ml(df):

    learning = MachineLearning(df)

    st.title('Aplicação de Machine Learning')

    # Exibir mapa de calor de correlação
    st.subheader('Correlação dos Dados')
    st.markdown(
        """
        <p>
            Começando pela análise de correlação dos dados, optamos por uma apresentação com um heatmap utilizando a Correlação de Pearson.
            que básicamente é uma medida de relação linear entre duas variáveis. O valor da correlação varia de -1 a 1, onde:
            <ul>
                <li>1: Correlação positiva perfeita (quando uma variável aumenta, a outra também aumenta);</li>
                <li>0: Sem correlação (as variáveis não têm relação linear);</li>
                <li>-1: Correlação negativa perfeita (quando uma variável aumenta, a outra diminui).</li>
            </ul>
        </p>
        """, unsafe_allow_html=True
    )    
    col1, col2, col3 = st.columns([0.5, 1, 0.5])
    with col2: st.pyplot(learning.correlation_data())
    st.markdown("""
                <p>
                    Analisando o mapa de calor obtido podemos chegar as seguintes conclusões:
                    <ul>
                        <li>Inteira e Vale_Transporte (0.96) - O que indica que os usuários que utilizam vale transporte tendem a comprar passagens inteiras;</li>
                        <li>Integração e Vale_Transporte (0.94) - Além disso os usuários de vale transporte tendem a fazer deslocamentos mais complexos tendo que utilizar conexões com outros ônibus;</li>
                        <li>Integração e Inteira (0.91) - Também temos uma relação forte entre a Inteira e o uso de Integração, o que mostra que os usuários que utilizaram passagens inteiras tenderam a usar a integração em seguida;</li>
                        <li>Qtd_Viagens e Vale_Transporte (0.89) - Há um crescimento da variável de Qtd_Viagens junto com o Vale_transporte o que indica que esses usuários formam maioria da clientela;</li>
                        <li>Qtd_Viagens e Estudante (0.88) - Da mesma forma observamos que os Estudantes vem logo em seguida como o público que mais utilizam transporte;</li>
                        <li>Tarifa_Social tem uma fraca conexão no geral - Isso acontece porque esse método de pagamento é feito de forma rara em eventos especificos na cidade, além feriados ou realização de concursos e Eleições.</li>
                    </ul>
                    Insights extraídos:
                    <ul>
                        <li>
                            Estudantes e usuários de Vale Transporte formam dois grupos principais, 
                            com alta frequência de viagens e sendo Vale Transporte com forte relação com Integração e passagens Inteiras.
                        </li>
                        <li>
                            Integração tem uma forte relação com o comportamento de usuários que utilizam Vale Transporte e Inteira.
                        </li>
                        <li>
                            Politicas sociais relacionadas a Tarifa Social e Gratuidade estão relacionadas a subgrupos ou eventos específicos (ocasionais),
                            sendo assim, com valores mais moderados.
                        </li>
                    </ul>
                </p>
                """, unsafe_allow_html=True)
    
    ###################################################################################

    # Exibir o K-means com base nos dados citados anteriormente
    st.subheader('Métodos de Clusterização')

    # Gráfico de cotovelo
    st.markdown(
        """
        <p>
            Na parte de Clusterização, foquei nas variáveis mais relevantes encontradas anteriormente ('Inteira', 'Vale_Transporte', 'Integracao', 'Qtd_Viagens', 'Estudante'), 
            com isso parti para o método do cotovelo (que utiliza a medida de variabilidade interna dentro dos cluters - WCSS), que é uma boa forma de obter 
            o número ideal de clusters para a análise do K-means.
            <ul>
                <li>Foram utilizados um intervalo de 1 a 11 para o calculo do WCSS (Within-Cluster Sum of Squares);</li>
                <li>Após isso foi criado o gráfico com o número de clusters no eixo X e o WCSS no eixo Y;</li>
                <li>Com isso, o gráfico abaixo foi criado, onde podemos identificar o 3 como o número ideal de clusters.</li>
            </ul>
        </p>
        """, unsafe_allow_html=True
    )    
    col1, col2, col3 = st.columns([0.5, 1, 0.5])
    with col2: st.pyplot(learning.clustering())
    
    st.markdown(
        """
        <p>
            Com o número ideal de clusters definido, rodamos o K-means, com as possibilidades abaixo:
        </p>
        """, unsafe_allow_html=True
    )  

    col1, col2, col3 = st.columns([0.6, 0.6, 1.8])
    with col1: param1 = st.selectbox("Primeiro parametro (x):", ('Inteira', 'Vale_Transporte', 'Integracao', 'Qtd_Viagens', 'Estudante'))
    with col2: param2 = st.selectbox("Segundo parametro (y):", ('Inteira', 'Vale_Transporte', 'Integracao', 'Qtd_Viagens', 'Estudante'))
    
    col1, col2, col3 = st.columns([0.5, 1, 0.5])
    with col2: st.pyplot(learning.kmeans_clustering(param1, param2))

    ###################################################################################

    # Exibir coeficientes da regressão linear
    st.subheader('Coeficientes da Regressão Linear')
    st.pyplot(learning.linear_regression_plot())

    ###################################################################################
         
    # Exibir gráfico de regressão
    #st.subheader('Evolução do Uso de Transporte Público')
    #st.pyplot(learning.line_chart_plot_emp())

