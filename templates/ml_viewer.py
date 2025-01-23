import streamlit as st
from modules.machine_learning import MachineLearning

def ml(df):

    learning = MachineLearning(df)

    st.title('Aplicação de Machine Learning')

    # Exibir gráfico de regressão
    st.subheader('Evolução do Uso de Transporte Público')
    st.pyplot(learning.model_regression_plot())

    # Exibir mapa de calor de correlação
    st.subheader('Correlação dos Dados')
    st.pyplot(learning.correlation_data())

    # Exibir coeficientes da regressão linear
    st.subheader('Coeficientes da Regressão Linear')
    st.pyplot(learning.linear_regression_plot())

    # Exibir segmentação de dados
    st.subheader('Segmentação de Dados (Clustering)')
    st.pyplot(learning.data_segmentation())