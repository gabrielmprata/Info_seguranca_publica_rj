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

# Construção dos Datasets
# 1. Histórico indicadores

# 2. Satisfação Geral por Prestadora


#######################
# 📈 Contrução dos gráficos 📊

# 4.3. Crimes contra a vida
# 4.3.1 Letalidade Violenta

# historico anual
let = px.line(df_hs_compara, x='ano', y='letalidade_violenta', markers=True, text='letalidade_violenta',
              line_shape="spline", template="plotly_dark", title="Letalidade Violenta por Ano",
              labels=dict(
                  ano="Ano", letalidade_violenta="Letalidade Violenta(k)")
              )
let.update_xaxes(type="category", title=None)
let.update_traces(line_width=2, textposition='top center')

let2 = px.bar(df_hs_compara, x="ano", y="var_letalidade_violenta", title="Diferença YxY(%)", template="plotly_dark", text_auto=True,
              labels=dict(ano="Ano", var_letalidade_violenta='Variação')
              )
let2.update_traces(textangle=0, textfont_size=12, textposition='outside',
                   cliponaxis=False, marker_color=df_hs_compara["color_let"])
let2.update_yaxes(showticklabels=False, showgrid=False,
                  visible=False, fixedrange=True)
let2.update_xaxes(showgrid=False, visible=False,
                  fixedrange=True, type="category", title=None)

# Por mês
letmes = px.line(df_anuario.groupby(['mes', 'mes_char'])['letalidade_violenta'].sum().reset_index(), x='mes_char', y=['letalidade_violenta'],
                 markers=True, text='value', line_shape="spline", template="plotly_dark",
                 title="Letalidade Violenta por mês", color_discrete_sequence=px.colors.sequential.Blackbody_r,
                 labels=dict(mes_char="Mês", value="Letalidade",
                             variable="Letalidade")
                 )
letmes.update_xaxes(type="category", title=None)
letmes.update_layout(showlegend=False)
letmes.update_traces(line_width=2, textposition='top center')

##################################################################################
# Dashboard Main Panel

vlr_atual = (
    ((df_hs_compara.letalidade_violenta.values[22])*1000)/365).round(0)

vlr_delta = ((((df_hs_compara.letalidade_violenta.values[21])*1000)/365).round(
    0))-((((df_hs_compara.letalidade_violenta.values[22])*1000)/365).round(0))

st.markdown("# Crimes contra a vida")
st.markdown("## :blue[Resumo dos principais resultados]")

with st.expander("Indicadores", expanded=True):

    col = st.columns((1.6, 1.6), gap='small')

    with col[0]:
        # Quadro com o total e a variação
        st.markdown('### Letalidade Violenta')
        st.metric(label="", value=str(
            df_hs_compara.letalidade_violenta.values[22]), delta=str(df_hs_compara.var_letalidade_violenta.values[22]), delta_color="inverse", border=True)

    with col[1]:
        st.markdown('### Vítimas média dia')
        st.metric(label="", value=int(vlr_atual),
                  delta=int(vlr_delta), border=True)

    col1 = st.columns((1.6, 1.6), gap='small')

    with col1[0]:
        # Quadro com o total e a variação
        st.markdown('### Homicídio doloso')
        st.metric(label="", value=str(
            df_hs_compara.hom_doloso.values[22]), delta=str(df_hs_compara.var_hom_doloso.values[22]), delta_color="inverse", border=True)

    with col1[1]:
        st.markdown('### Latrocínio')
        st.metric(label="", value=int(
            df_hs_compara.latrocinio.values[22]), delta=str(df_hs_compara.var_latrocinio.values[22]), delta_color="inverse", border=True)

    col2 = st.columns((1.6, 1.6), gap='small')

    with col2[0]:
        # Quadro com o total e a variação
        st.markdown('### Lesão corporal seguida de morte')
        st.metric(label="", value=int(
            df_hs_compara.lesao_corp_morte.values[22]), delta=str(df_hs_compara.var_lesao.values[22]), delta_color="inverse", border=True)

    with col2[1]:
        st.markdown('### Latrocínio')
        st.metric(label="", value=int(
            df_hs_compara.latrocinio.values[22]), delta=str(df_hs_compara.var_latrocinio.values[22]), delta_color="inverse", border=True)


st.markdown("## :blue[Letalidade Violenta]")
with st.expander("Histórico por Ano", expanded=True):
    st.plotly_chart(let, use_container_width=True)
    st.plotly_chart(let2, use_container_width=True)
    st.markdown("""
        O indicador de Letalidade Violenta registrou, em 2025, 3.881 vítimas (um aumento de 1,9% em relação ao ano anterior).
                """)
    st.plotly_chart(letmes, use_container_width=True)
    st.markdown("""
                **Outubro** foi o mês com mais registros de letalidade violenta no estado no ano de 2025.
                >
                **Nota:** 
                No dia 28/10, ocorreu uma operação policial nos complexos do Alemão e da Penha, onde 121 pessoas morreram e 113 foram presas.

                De acordo com a Polícia Civil, dentre os 121 mortos, 4 eram policiais.
                """)
