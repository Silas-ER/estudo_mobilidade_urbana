import streamlit as st
from modules.data_loader import DataLoader
from modules.analyzer import DataAnalyzer
from modules.visualizer import DataVisualizer
from modules.content_data import content_data
from modules.insights import insights

# Configuração da página
st.set_page_config(
    page_title="Mobilidade Urbana - Natal/RN",       
    page_icon="🚌",                     
    layout="wide",                      
    initial_sidebar_state="collapsed",   
)

# Abas para explicações e insights
tab_explicacao_dados, tab_insights = st.tabs(['Data Overview', 'Insights'])

with tab_explicacao_dados:
    content_data(DataLoader.load_data)

with tab_insights:
    insights(DataLoader.load_data)
    