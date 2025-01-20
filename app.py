import streamlit as st
from modules.data_loader import DataLoader
from modules.analyzer import DataAnalyzer
from modules.visualizer import DataVisualizer
from modules.content_data import content_data
from modules.insights import insights
from modules.machine_learning import ml

# Configuração da página
st.set_page_config(
    page_title="Mobilidade Urbana - Natal/RN",       
    page_icon="🚌",                     
    layout="wide",                      
    initial_sidebar_state="collapsed",   
)

# Instanciando as classes
data_loader = DataLoader()
df = data_loader.load_data()

data_analyzer = DataAnalyzer(df)
data_analyzer.clean_data()

st.title('Mobilidade Urbana - Natal/RN')

# Abas para explicações e insights
tab_explicacao_dados, tab_ml, tab_insights = st.tabs(['Data Overview', 'Aplicação de ML', 'Insights'])

with tab_explicacao_dados:
    content_data(df)

with tab_ml:
    ml(df)

with tab_insights:
    insights(df)
    