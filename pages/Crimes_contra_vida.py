#######################
# Importando libraries
import streamlit as st
import altair as alt
# import webbrowser
import pandas as pd
import plotly.express as px
# from streamlit.components.v1 import html

#######################
# Configuração da página
st.set_page_config(
    page_title="Anuário 2025 de Segurança Pública",
    page_icon="👮‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

alt.themes.enable("dark")


#######################
# CSS styling
st.markdown("""
<style>

section[data-testid="stSidebar"] {
            width: 200px;
        }                    

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

#######################
# Carregando dataset
# carrega dataset com a comparacao ano a ano
df_hs_compara = pd.read_csv(
    'https://raw.githubusercontent.com/gabrielmprata/Info_seguranca_publica_rj/main/datasets/df_hs_compara.csv', sep=',')

# Construção dos Datasets
# 1. Histórico indicadores

# 2. Satisfação Geral por Prestadora


#######################
# 📈 Contrução dos gráficos 📊

# 4.3. Crimes contra a vida
# 4.3.1 Letalidade Violenta


let = px.line(df_hs_compara, x='ano', y='letalidade_violenta',
              markers=True, text='letalidade_violenta',
              # height=600, width=800, #altura x largura
              line_shape="spline",
              template="plotly_dark",
              render_mode="svg",
              title="Letalidade Violenta por Ano",
              labels=dict(
                  ano="Ano", letalidade_violenta="Letalidade Violenta(k)")
              )
# se o type for date, vai respeitar o intervalo
let.update_xaxes(type="category", title=None)
let.update_traces(line_width=2, textposition='top center')

let2 = px.bar(df_hs_compara, x="ano", y="var_letalidade_violenta", title="Diferença YxY(%)", template="plotly_dark", text_auto=True,
              # height=300, width=1160,  #largura
              # , hover_data=['ano', 'dif','var']
              labels=dict(ano="Ano", var_letalidade_violenta='Variação')
              )
let2.update_traces(textangle=0, textfont_size=12, textposition='outside',
                   cliponaxis=False, marker_color=df_hs_compara["color_let"])
let2.update_yaxes(showticklabels=False, showgrid=False,
                  visible=False, fixedrange=True)
let2.update_xaxes(showgrid=False, visible=False,
                  fixedrange=True, type="category", title=None)


#######################
# Dashboard Main Panel

st.markdown("# Crimes contra a vida")
st.markdown("## :blue[Letalidade Violenta]")
with st.expander("Histórico", expanded=True):
    st.plotly_chart(let, use_container_width=True)
    st.plotly_chart(let2, use_container_width=True)
