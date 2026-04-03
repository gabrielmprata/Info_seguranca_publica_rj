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
st.sidebar.success("Selecione a categoria⬆️")

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

# Construção de listas para mini gráfico

vlr_atual = (
    ((df_hs_compara.apreensao_drogas.values[22])*1000)/365).round(0)

vlr_delta = ((((df_hs_compara.apreensao_drogas.values[21])*1000)/365).round(
    0))-((((df_hs_compara.apreensao_drogas.values[22])*1000)/365).round(0))


vlr_atual_apf = (
    ((df_hs_compara.apf.values[22])*1000)/365).round(0)

vlr_delta_apf = ((((df_hs_compara.apf.values[21])*1000)/365).round(
    0))-((((df_hs_compara.apf.values[22])*1000)/365).round(0))

##############################################################################################
# 📈 Contrução dos gráficos 📊

# 4.5. Atividade Policia
# 4.5.1 Apreensão de drogas

# historico anual
apre_ano = px.line(df_hist_anual.groupby('ano')[['apreensao_drogas']].apply(lambda x: x.sum()/1000).round(1).reset_index(),
                   x='ano', y='apreensao_drogas',
                   markers=True, text='apreensao_drogas', line_shape="spline", template="plotly_dark",
                   title="Apreensão de drogas", height=525, width=850,
                   color_discrete_sequence=px.colors.sequential.Blackbody_r,
                   labels=dict(ano="Ano", apreensao_drogas="Apreensão (k)")
                   )

apre_ano.update_xaxes(type="category", title=None)
apre_ano.update_layout(showlegend=False)
apre_ano.update_traces(line_width=2, textposition='top center')

# 4.5.2 Prisão em flagrante
apf_ano = px.line(df_hist_anual.groupby('ano')[['apf']].apply(lambda x: x.sum()/1000).round(1).reset_index(),
                  x='ano', y='apf', markers=True, text='apf', line_shape="spline", template="plotly_dark",
                  title="Prisões em flagrante", height=525, width=850,
                  color_discrete_sequence=px.colors.sequential.Blackbody_r,
                  labels=dict(ano="Ano", apreensao_drogas="Prisões (k)")
                  )

apf_ano.update_xaxes(type="category", title=None)
apf_ano.update_layout(showlegend=False)
apf_ano.update_traces(line_width=2, textposition='top center')

# 4.5.3 Auto de apreensão de adolescente por prática de ato infracional
aaapai_ano = px.line(df_hist_anual.groupby('ano')[['aaapai']].apply(lambda x: x.sum()/1000).round(1).reset_index(),
                     x='ano', y='aaapai',
                     markers=True, text='aaapai', line_shape="spline", template="plotly_dark",
                     title="Auto de apreensão de adolescente",
                     height=525, width=850,  # altura #largura
                     color_discrete_sequence=px.colors.sequential.Blackbody_r,
                     labels=dict(ano="Ano", aaapai="Autos (k)")
                     )
aaapai_ano.update_xaxes(type="category", title=None)
aaapai_ano.update_layout(showlegend=False)
aaapai_ano.update_traces(line_width=2, textposition='top center')

##################################################################################
##################################################################################
# Dashboard Main Panel

st.markdown("# Atividade Policial")
st.markdown("### :blue[Resumo dos principais resultados]")

with st.expander("Indicadores    (click aqui para ver)", expanded=True):

    col = st.columns((1.6, 1.6), gap='small')

    with col[0]:
        st.markdown('### Apreensão de drogas')
        st.metric(label="", value=str(
            df_hs_compara.apreensao_drogas.values[22]), delta=str(df_hs_compara.var_apreensao_drogas.values[22]), border=True)

    with col[1]:
        st.markdown('### Apreensão drogas média dia')
        st.metric(label="", value=int(vlr_atual),
                  delta=int(vlr_delta), border=True)

    col1 = st.columns((1.6, 1.6), gap='small')
    with col1[0]:
        st.markdown('### Prisão em flagrante')
        st.metric(label="", value=str(
            (df_hs_compara.apf.values[22]/1000).round(2)), delta=str(df_hs_compara.var_apf.values[22]), border=True)

    with col1[1]:
        st.markdown('### Prisão flagrante média dia')
        st.metric(label="", value=int(vlr_atual),
                  delta=int(vlr_delta), border=True)

    col2 = st.columns((1), gap='small')

    with col2[0]:
        st.markdown(
            '### Auto de apreensão de adolescente por prática de ato infracional')
        st.metric(label="", value=str(
            (df_hs_compara.aaapai.values[22]/1000).round(2)), delta=str(df_hs_compara.var_aaapai.values[22]), delta_color="inverse", border=True)


st.markdown("### :blue[Apreensão drogas]")
st.plotly_chart(apre_ano, use_container_width=True)
st.markdown("""As apreensões de drogas em 2025 tiveram um aumento de **7,9%** em relação ano anterior, mantendo a tendência de crescimento registrada nos últimos dois anos.
                """)

st.markdown("### :blue[Prisão em flagrante]")
st.plotly_chart(apf_ano, use_container_width=True)
st.markdown("""Em 2025, foram registradas **42.295** prisões em flagrante em todo o estado, representando uma diminuição de **0,2%** em relação ao ano anterior.
>
Em 2020, o número de prisões diminuiu devido às restrições de mobilidade impostas pela pandemia. No entanto, nos últimos anos, observamos uma tendência de aumento que se manteve até 2024, período em que obteve o maior número de toda a série.
            """)

st.markdown(
    "### :blue[Auto de apreensão de adolescente por prática de ato infracional]")
st.plotly_chart(aaapai_ano, use_container_width=True)
st.markdown("""Desde 2013, observamos uma queda no número de autos de apreensão de adolescentes por prática de ato infracional.
>
Em 2025, houve registro de 5.232 casos, um **crescimento de 6,4%** no número de adolescentes apreendidos em relação ao ano anterior.
                """)
