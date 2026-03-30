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

# Construção de listas para mini gráfico

vlr_atual = (
    ((df_hs_compara.total_roubos.values[22])*1000)/365).round(0)

vlr_delta = ((((df_hs_compara.total_roubos.values[21])*1000)/365).round(
    0))-((((df_hs_compara.total_roubos.values[22])*1000)/365).round(0))

# roubos por cisp
df_roubo_un = (df_anuario.groupby(['risp_desc', 'cisp', 'unidade_territorial'])['total_roubos'].sum().reset_index()
               ).sort_values(by='total_roubos', ascending=False).head(10)

# Rank the 'Score' column in descending order
df_roubo_un['Rank'] = df_roubo_un['total_roubos'].rank(ascending=False)

##############################################################################################
# 📈 Contrução dos gráficos 📊

# 4.4. Crimes contra o patrimônio
# 4.4.1 Roubos

# historico anual
roubo_ano = px.line(df_hs_compara, x='ano', y='total_roubos', title="Roubos por Ano",
                    markers=True, text='total_roubos', line_shape="spline", template="plotly_dark",
                    labels=dict(ano="Ano", letalidade_violenta="Roubos(k)")
                    )
roubo_ano.update_xaxes(type="category", title=None)
roubo_ano.update_traces(line_width=2, textposition='top center')


roubo_ano_var = px.bar(df_hs_compara, x="ano", y="var_roubos", title="Diferença YxY(%)", template="plotly_dark", text_auto=True,
                       # height=300, width=1160,  #largura
                       # , hover_data=['ano', 'dif','var']
                       labels=dict(ano="Ano", var_roubos='Variação')
                       )
roubo_ano_var.update_traces(textangle=0, textfont_size=12, textposition='outside',
                            cliponaxis=False, marker_color=df_hs_compara["color_roubo"])
roubo_ano_var.update_yaxes(
    showticklabels=False, showgrid=False, visible=False, fixedrange=True)
roubo_ano_var.update_xaxes(
    showgrid=False, visible=False, fixedrange=True, type="category", title=None)

# por mes
roubo_mes = px.line(df_anuario.groupby(['mes', 'mes_char'])['total_roubos'].sum().reset_index(),
                    x='mes_char', y=['total_roubos'], markers=True, text='value',
                    line_shape="spline", template="plotly_dark", title="Roubos por mês",
                    color_discrete_sequence=px.colors.sequential.Blackbody_r,
                    labels=dict(mes_char="Mês", value="Roubos",
                                variable="Roubos")
                    )
roubo_mes.update_xaxes(type="category", title=None)
roubo_mes.update_layout(showlegend=False)
roubo_mes.update_traces(line_width=2, textposition='top center')

# roubo por CISP
roubo_cisp = go.Figure(data=[go.Table(

    header=dict(values=['Rank', 'RISP', 'Delagacia', 'Unidade Territorial', 'Total'],
                fill_color='royalblue',
                align='left'),
    cells=dict(values=[df_roubo_un.Rank, df_roubo_un.risp_desc, df_roubo_un.cisp, df_roubo_un.unidade_territorial, df_roubo_un.total_roubos],
               fill_color='lightskyblue',
               align='center',
               font=dict(color='darkslategray', size=11)
               ))
], layout=go.Layout(template="plotly_dark"))

##################################################################################
##################################################################################
# Dashboard Main Panel

st.markdown("# Crimes contra o patrimônio")
st.markdown("### :blue[Resumo dos principais resultados]")

with st.expander("Indicadores    (click aqui para ver)", expanded=True):

    col = st.columns((1.6, 1.6), gap='small')

    with col[0]:
        st.markdown('### Roubos')
        st.metric(label="", value=str(
            df_hs_compara.total_roubos.values[22]), delta=str(df_hs_compara.var_roubos.values[22]), delta_color="inverse", border=True)

    with col[1]:
        st.markdown('### Roubos média dia')
        st.metric(label="", value=int(vlr_atual),
                  delta=int(vlr_delta), delta_color="inverse", border=True)

    col1 = st.columns((1.6, 1.6), gap='small')

    with col1[0]:
        st.markdown('### Roubo Carga')
        st.metric(label="", value=str(
            df_hs_compara.roubo_carga.values[22]), delta=str(df_hs_compara.var_roubo_carga.values[22]), delta_color="inverse", border=True)

    with col1[1]:
        st.markdown('### Roubo Veículos')
        st.metric(label="", value=int(
            df_hs_compara.roubo_veiculo.values[22]), delta=str(df_hs_compara.var_roubo_veiculo.values[22]), delta_color="inverse", border=True)

    col2 = st.columns((1.6, 1.6), gap='small')

    with col2[0]:
        st.markdown('### Roubo Rua')
        st.metric(label="", value=int(
            df_hs_compara.roubo_rua.values[22]), delta=str(df_hs_compara.var_roubo_rua.values[22]), delta_color="inverse", border=True)

    with col2[1]:
        st.markdown('### Roubo a transeunte')
        st.metric(label="", value=str(
            df_hs_compara.roubo_transeunte.values[22]/1000), delta=str(df_hs_compara.var_rtranseunte.values[22]), delta_color="inverse", border=True)

    col3 = st.columns((1.6, 1.6), gap='small')
    with col3[0]:
        st.markdown(
            '#### Roubo Celular')
        st.metric(label="", value=str(
            df_hs_compara.roubo_celular.values[22]/1000), delta=str(df_hs_compara.var_rcelular.values[22]), delta_color="inverse", border=True)

    with col3[1]:
        st.markdown('### Estelionato')
        st.metric(label="", value=int(
            df_hs_compara.estelionato.values[22]), delta=str(df_hs_compara.var_estelionato.values[22]), delta_color="inverse", border=True)

st.markdown("### :blue[Roubos]")
with st.expander("Histórico por Ano", expanded=True):
    st.markdown("Esse indicador engloba **todos** os delitos de: roubo a transeunte, roubo de celular, roubo em coletivo, roubo de rua, roubo de veiculo, roubo de carga, roubo de comercio, roubo de residência, roubo de banco, roubo de caixa eletrônico, roubo condução saque roubo apos saque, roubo bicicleta e outros roubos.")
    st.plotly_chart(roubo_ano, use_container_width=True)
    st.plotly_chart(roubo_ano_var, use_container_width=True)
    st.markdown("""O indicador de **Roubos** registrou, em 2025, 97.712 vítimas,  8.6% menor em relação ao ano anterior).
                """)
    st.plotly_chart(roubo_mes, use_container_width=True)
    st.markdown("""
                O mês com mais registros de ocorrências de roubos, foram Janeiro e Dezembro.
                >
                Sendo que de Novembro para Dezembro tivemos um aumento de 22%.
                """)

    st.markdown("#### :blue[Roubos por CISP e unidade territorial]")
    st.plotly_chart(roubo_cisp, use_container_width=True)
    st.markdown("""
                A delegacia com mais registros de roubos no estado, é a 59 DP, que atende a região de Duque de Caxias.
                """)
