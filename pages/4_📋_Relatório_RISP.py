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
    return pd.read_csv("https://raw.githubusercontent.com/gabrielmprata/Info_seguranca_publica_rj/main/datasets/df_regiao_cisp.csv", sep=',')


# carrega dataset com as informacoes do anuario
df_regiao_cisp = load_data()


##############################################################################################
# 📈 Contrução dos gráficos 📊

# 4.6. Relatório RISP
# 4.6.1 Indicadores

# Roubo de Rua
ind_rua = px.histogram(df_regiao_cisp, x="risp", y="roubo_rua", color='ano', barmode='group',
                       labels=dict(risp="RISP", ano="Ano", roubo_rua="Roubos"),
                       color_discrete_sequence=px.colors.sequential.Blues_r, text_auto='.3s',
                       template="plotly_dark"
                       )
ind_rua.update_xaxes(type="category", title=None)
ind_rua.update_traces(textfont_size=12, textangle=0,
                      textposition="outside", cliponaxis=False)
ind_rua.update_layout(yaxis_title="Roubos")
ind_rua.update_layout(showlegend=True)

# Roubo de Veículo
ind_veic = px.histogram(df_regiao_cisp, x="risp", y="roubo_veiculo", color='ano', barmode='group',
                        labels=dict(risp="RISP", ano="Ano",
                                    roubo_veiculo="Roubos"),
                        color_discrete_sequence=px.colors.sequential.Blues_r, text_auto='.3s',
                        template="plotly_dark"
                        )
ind_veic.update_xaxes(type="category", title=None)
ind_veic.update_traces(textfont_size=12, textangle=0,
                       textposition="outside", cliponaxis=False)
ind_veic.update_layout(yaxis_title="Roubos", showlegend=True)

# Roubo de Carga
ind_carga = px.histogram(df_regiao_cisp, x="risp", y="roubo_carga", color='ano', barmode='group',
                         labels=dict(risp="RISP", ano="Ano",
                                     roubo_carga="Roubos"),
                         color_discrete_sequence=px.colors.sequential.Blues_r, text_auto='.3s',
                         template="plotly_dark"
                         )
ind_carga.update_xaxes(type="category", title=None)
ind_carga.update_traces(textfont_size=12, textangle=0,
                        textposition="outside", cliponaxis=False)
ind_carga.update_layout(yaxis_title="Roubos", showlegend=True)

# Letalidade Violenta
ind_letal = px.histogram(df_regiao_cisp, x="risp", y="letalidade_violenta", color='ano', barmode='group',
                         labels=dict(risp="RISP", ano="Ano",
                                     letalidade_violenta="Casos"),
                         color_discrete_sequence=px.colors.sequential.Blues_r, text_auto='.3s',
                         template="plotly_dark"
                         )
ind_letal.update_xaxes(type="category", title=None)
ind_letal.update_traces(textfont_size=12, textangle=0,
                        textposition="outside", cliponaxis=False)
ind_letal.update_layout(yaxis_title="Casos", showlegend=True)


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
st.plotly_chart(ind_rua, use_container_width=True)
st.markdown("""
                O indicador Roubo de Rua apresentou queda em seis das sete RISP: 1, 3, 4, 5, 6 e 7, em relação ao ano anterior.
>
 A maior redução foi observada na RISP 5, com 35,7% (148), enquanto a menor redução ocorreu na RISP 1, com 1,9% (20.734) dos roubos de rua em relação a 2024.
 >
  Já a RISP 2 apresentou um crescimento, foram 7,5% (17.495) casos.
                """)

st.markdown("#### :blue[Indicadores de **roubo de veículos**]")
st.plotly_chart(ind_veic, use_container_width=True)
st.markdown("""
                Quatro das sete RISP do estado apresentaram queda nos casos de **Roubo de Veículo** em 2025, sendo as RISP 5 e 1 com as maiores reduções: **40,7% (54 casos no ano)** e **39,3% (4.951)**.
>
A menor redução foi observada na RISP 2, que diminuiu **4,1% (8.762)**.
>
As RISP 7, 6 e 4, por sua vez, tiveram aumento nos casos. Descatamos aqui a RISP 7 com **40,7% (38 casos)** e a RISP 6 com **32,8% (170 casos)**.
                """)

st.markdown("#### :blue[Indicadores de **roubo de carga**]")
st.plotly_chart(ind_carga, use_container_width=True)
st.markdown("""
            As RISP 5 e 7 apresentaram as maiores quedas nos casos de Roubos de Carga.
            >
            Já a RISP 4 manteve-se estável, com o mesmo número de casos do ano anterior.
                """)

st.markdown("#### :blue[Indicadores de **Letalidade Violenta**]")
st.plotly_chart(ind_letal, use_container_width=True)
st.markdown("""
            O indicador **Letalidade Violenta** apresentou redução em quatro das sete RISP do estado.
>
A maior redução em 2025, em relação ao ano anterior, foi observada na RISP 4, com **11,1% (515 no total).**
>
Em contrapartida, a RISP 1 mostrou um crescimento de **23,3% (546)** do número de casos em 2025.
                """)
