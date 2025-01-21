import streamlit as st
from modules.machine_learning import MachineLearning
from modules.statistical_models import prophet_forecast

def ml(df):

    learning = MachineLearning(df)

    # Treinamento do modelo de regressão linear
    rmse, r2 = learning.regressao_linear()

    st.markdown(f"""
                <h1>Aplicação de Machine Learning</h1>
                
                <h5>Modelo de regressão linear</h5>
                <p>
                    A regressão linear foi utilizada com base na quantidade de viagens e os tipos de bilhetagem 
                    (Vale_Transporte', 'Estudante_BT', 'Inteira_Especie', 'Integracao_Plena). Considerados mais relevantes anteriormente.
                    <br>
                    Com isso os resulado obtidos pelo modelo foram:
                    <ul>
                        <li>
                            O RMSE: {rmse:.2f} isso indica que o modelo erra em média {rmse:.2f} viagens por mês.
                            Considerando que a média de viagens é de 1430.5 viagens por mês o modelo não tem uma precisão muito alta,
                            porém se compararmos ao valor máximo de viagens ele razoavelmente ajustado.
                        </li>
                        <li>
                            Já o R²: {r2:.2f} indica que o modelo explica {r2:.2f} da variabilidade dos dados. 
                        </li>
                    </ul>
                </p>
                """,unsafe_allow_html=True)
    st.divider()

    # Modelo de Clustering com K-Means
    rmse, r2 = learning.regressao_linear()

    st.markdown(f"""
                <h1>Métodos de Clusternização com K-Means</h1>
                
                <h5>K-Means Clustering:</h5>
                <p>
                    Agrupamento de dados em clusters baseados em similaridades.
                </p>
                """,unsafe_allow_html=True)
    st.pyplot(learning.clustering_kmeans())
    st.divider()

    st.pyplot(prophet_forecast(df))