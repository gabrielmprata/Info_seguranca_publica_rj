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
                   title="Apreensão de drogas",
                   height=525, width=850,  # altura #largura
                   color_discrete_sequence=px.colors.sequential.Blackbody_r,
                   labels=dict(ano="Ano", apreensao_drogas="Apreensão (k)")
                   )
# se o type for date, vai respeitar o intervalo
apre_ano.update_xaxes(type="category", title=None)
apre_ano.update_layout(showlegend=False)
apre_ano.update_traces(line_width=2, textposition='top center')

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


st.markdown("### :blue[Roubos]")
with st.expander("Analises", expanded=True):
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

    st.markdown(
        "### :blue[Análise dos delitos que compõem o indicador **Roubos**]")
    st.markdown("#### :blue[Roubo de carga]")

    st.plotly_chart(roubo_carga_ano, use_container_width=True)

    st.markdown("""Em 2025, ocorreram **3.114 casos de Roubo de Carga**, representando uma diminuição de **9,4%** em relação ao ano anterior.
                """)

    st.markdown("#### :blue[Roubo de Veículo]")

    st.plotly_chart(roubo_veic_ano, use_container_width=True)
    st.plotly_chart(roubo_veic_var, use_container_width=True)
    st.markdown("""
                O ano de 2025 registrou uma queda de **18,4%** nos casos de **Roubo de Veículo**.
                >
                Observamos um aumento significativo nesses casos entre 2015 e 2017, seguido por uma queda brusca até 2020.
                >
                O número se manteve estável até 2022 e encerrou a série com uma nova queda observada em 2025.
                """)

    st.markdown("#### :blue[Roubo de Rua]")

    st.plotly_chart(roubo_rua_ano, use_container_width=True)
    st.plotly_chart(roubo_rua_var, use_container_width=True)
    st.markdown("""
                O indicador de Roubo de Rua vinha apresentando queda dos casos desde 2018.
                >
                Em 2023, registrou-se o menor número de ocorrências desde 2004.
                >
                Já em 2025, apresentou um **decréscimo de 2,7%** em relação ao ano anterior.
                """)

    st.markdown("#### :blue[Roubo a transeunte]")

    st.plotly_chart(rtranseunte_ano, use_container_width=True)

    st.markdown("""
                Em 2025, o roubo a transeunte registrou **queda de 10,6%** casos, mantendo a tendência observada nos últimos anos.
                """)

    st.markdown("#### :blue[Roubo de celular]")

    st.plotly_chart(roubo_celular_ano, use_container_width=True)
    st.markdown("""
                Desde 2013, esse delito apresentava um crescimento constante, interrompido em 2020.
                >
                Ao final da pandemia, observamos uma queda nos números nos anos seguintes, mas, em 2024, os dados apresentaram nova crescente.
                >
                Em 2025, foram registrados **25.625** casos de **roubo de celular**, representando um aumento de **19,7%** em comparação com o ano anterior.
                """)
    st.plotly_chart(roubo_celular_mes, use_container_width=True)
    st.markdown("""
                No mês de março foram registrados **2.469** roubo de celulares, pois nesse mês temos a celebração do carnaval no estado.
                """)

    st.markdown("#### :blue[Roubo em coletivo]")

    st.plotly_chart(roubo_col_ano, use_container_width=True)
    st.markdown("""
                Em 2025, o roubo em coletivo registrou um decréscimo em relação ao ano anterior de **40,6%**.
                """)

    st.markdown("#### :blue[Estelionato]")

    st.plotly_chart(estelionato_ano, use_container_width=True)
    st.markdown("""
                O estelionato foi incluído neste relatório devido ao aumento identificado nos últimos anos.
>
Em 2025 houve um aumento de **2,0%**, superando o ano anterior e somando o maior número de casos da série histórica.
                """)

    st.markdown("#### :blue[Extorção]")

    st.plotly_chart(extorcao_ano, use_container_width=True)
    st.markdown("""
                Em 2025, tivemos **3.646** registros de extorsão, **19,5%** a mais do que em 2024.
                """)
