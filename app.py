import streamlit as st
from modules.data_loader import DataLoader
from modules.data_processing import DataAnalyzer
from modules.visualizer import DataVisualizer
from templates.content_data import content_data
from templates.insights import insights
from templates.ml_viewer import ml

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
data_analyzer.data_formatter()  

st.title('Mobilidade Urbana - Natal/RN')

# Abas para explicações e insights
tab_explicacao_dados, tab_ml, tab_insights = st.tabs(['Data Overview', 'Aplicação de ML', 'Insights'])

#print(df.dtypes)

with tab_explicacao_dados:
    content_data(df)

with tab_ml:
    ml(df)

with tab_insights:
    insights(df)