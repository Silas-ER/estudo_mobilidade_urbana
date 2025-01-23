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
    st.pyplot(learning.correlation_data())
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
                        <li>Segmentação por Grupos:

Estudantes e usuários de Vale Transporte formam dois grupos principais, com alta frequência de viagens e forte relação com Integração e passagens Inteiras.
Impacto das Integrações:

O uso de Integração está fortemente relacionado ao comportamento de usuários que utilizam Vale Transporte e passagens Inteiras. Isso pode ser investigado em relação a políticas tarifárias e subsídios.
Foco em Políticas Sociais:

As variáveis relacionadas a Tarifa Social e Gratuito apresentam correlações mais moderadas, indicando que essas políticas podem estar destinadas a subgrupos específicos (e.g., estudantes ou usuários ocasionais).</li>
                    <\ul>
                </p>
                """, unsafe_allow_html=True)
    
    
    # Exibir gráfico de regressão
    st.subheader('Evolução do Uso de Transporte Público')
    st.pyplot(learning.model_regression_plot())

    # Exibir coeficientes da regressão linear
    st.subheader('Coeficientes da Regressão Linear')
    st.pyplot(learning.linear_regression_plot())

    # Exibir segmentação de dados
    st.subheader('Segmentação de Dados (Clustering)')
    st.pyplot(learning.data_segmentation())