#######################
# Importando libraries
import streamlit as st
import altair as alt
# import webbrowser
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

.stButton button {
    background-color: #0e3558; /* Change background color */
    color: #FFFFFF;            /* Change font color */
    font-size: 16px;           /* Change font size */
    font-weight: bold;         /* Change font weight */
    border-radius: 25px;       /* Add rounded corners */
    padding: 10px 20px;
    border: none;
}

</style>
""", unsafe_allow_html=True)


#######################
# Carregando dataset


@st.cache_data
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/gabrielmprata/Info_seguranca_publica_rj/main/datasets/df_anuario.csv.bz2", sep='|', encoding="Latin 1")


# carrega dataset com as informacoes do anuario
df_anuario = load_data()

# carrega dataset com o historico anual dos principais indicadores
df_hist_anual = pd.read_csv(
    'https://raw.githubusercontent.com/gabrielmprata/Info_seguranca_publica_rj/main/datasets/df_hist_anual.csv', sep=',')

# carrega dataset com a comparacao ano a ano
df_hs_compara = pd.read_csv(
    'https://raw.githubusercontent.com/gabrielmprata/Info_seguranca_publica_rj/main/datasets/df_hs_compara.csv', sep=',')


##############################################################################################
# 📈 Contrução dos gráficos 📊

# 4.6. Relatório RISP
# 4.6.1 Indicadores

# Roubo de Rua
fig = px.histogram(df_regiao_cisp, x="risp", y="roubo_rua", color='ano', barmode='group',
                   labels=dict(risp="RISP", ano="Ano", roubo_rua="Roubos"),
                   color_discrete_sequence=px.colors.sequential.Blues_r, text_auto='.3s',
                   template="plotly_dark"
                   )
fig.update_xaxes(type="category", title=None)
fig.update_traces(textfont_size=12, textangle=0,
                  textposition="outside", cliponaxis=False)
fig.update_layout(yaxis_title="Roubos")
fig.update_layout(showlegend=True)


##################################################################################
##################################################################################
# Dashboard Main Panel

st.markdown("# Relatório RISP")
st.markdown("""
            Na última seção deste relatório, apresentamos as Regiões Integradas de Segurança Pública (RISP).
            
            As RISP são organizadas, a nível prático, com base nas divisões das Áreas Integradas de Segurança Pública (AISP) e Circunscrições Integradas de Segurança Pública (CISP), que são equivalentes à área de um batalhão da Polícia Militar e de uma delegacia da Polícia Civil, respectivamente.

            Ao todo, o estado possui sete RISP, divididas da seguinte maneira:

            **RISP 1:** Capital (Zona Sul, Centro e parte da Zona Norte)
            
            **RISP 2:** Capital (Zona Oeste e parte da Zona Norte)

            **RISP 3:** Baixada Fluminense

            **RISP 4:** Grande Niterói e Região dos Lagos

            **RISP 5:** Sul Fluminense

            **RISP 6:** Norte-Fluminense e Noroeste

            **RISP 7:** Região Serrana

            """)
st.markdown("### :blue[Indicadores na RISP]")
st.markdown("#### :blue[Indicadores de **roubo de rua**]")
# st.plotly_chart(apre_ano, use_container_width=True)
# st.markdown("""As apreensões de drogas em 2025 tiveram um aumento de **7,9%** em relação ano anterior, mantendo a tendência de crescimento registrada nos últimos dois anos.
#                """)
