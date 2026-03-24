#######################
# Importando libraries
import streamlit as st
import altair as alt
import json
from urllib.request import urlopen
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


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
df_ind_anual = df_hist_anual[(df_hist_anual['ano'] >= 2024)].groupby('ano')[['total', 'letalidade_violenta', 'hom_doloso', 'lesao_corp_morte', 'latrocinio', 'feminicidio', 'hom_por_interv_policial', 'total_roubos',
                                                                             'total_furtos', 'estelionato', 'apreensao_drogas', 'pol_militares_mortos_serv', 'pol_mortos_serv', 'roubo_carga', 'roubo_veiculo', 'roubo_rua', 'roubo_transeunte', 'roubo_celular']].apply(lambda x: x.sum()).reset_index()

# 📈 Contrução dos gráficos 📊

# 4. Anuário de Seguranca Publica

# 4.1 Resumo dos principais indicadores


#######################
# Construção dos Gráficos

# 1. Histórico indicadores


#######################
# Dashboard Main Panel

st.markdown(
    "# 👮‍♂️ Informações de Segurança Pública do Estado do Rio de Janeiro 🚓")

text = """:orange[**Introdução**]"""

with st.expander(text, expanded=True):
    st.markdown("""
                Os dados apresentados nesse estudo acadêmico, foram extraídas dos registros de ocorrências feitos nas delegacias do estado do Rio de Janeiro, com as vítimas.
            
                As informações das ocorrências, estão disponíveis nos **Dados Abertos** do Instituto de segurança pública (ISP).

                

""")

st.markdown("## :blue[Apresentação]")
st.markdown("""
                O anuário de 2025 apresenta uma análise dos principais indicadores de criminalidade e da atividade policial no estado do Rio de Janeiro, abrangendo o período de 2003 a 2025.
            
                Esses indicadores são organizados em três categorias: **crimes contra a vida, crimes contra o patrimônio e atividade policial.**
            
                O relatório está estruturado da seguinte forma: na primeira parte, são apresentados os principais resultados dos delitos selecionados em 2025, com destaque para a variação anual.
                
                Na segunda parte, são exibidos gráficos e análises que auxiliam na interpretação dos dados.

""")

st.markdown("## :blue[Resumo dos principais resultados]")

with st.expander("Indicadores", expanded=True):

    col = st.columns((1.6, 1.3, 1.3), gap='medium')

    with col[0]:
        #######################
        # Quadro com o total e a variação
        st.markdown('### Ocorrências')
        st.metric(label="", value=str(
            df_hs_compara.total.values[22]), delta=str(df_hs_compara.var_total.values[22]))

    with col[1]:
        st.markdown('### Letalidade Violenta')
        st.metric(label="", value=str(
            (df_hs_compara.letalidade_violenta.values[22]).round(2)), delta=str(df_hs_compara.var_letalidade_violenta.values[22]))

    with col[2]:
        st.markdown('### Homicídio doloso')
        st.metric(label="", value=str(
            df_hs_compara.hom_doloso.values[22]), delta=str(df_hs_compara.var_hom_doloso.values[22]))

    col2 = st.columns((1.6, 1.3, 1.3), gap='medium')

    with col2[0]:
        st.markdown('### Roubos')
        st.metric(label="", value=str(
            df_hs_compara.total_roubos.values[22]), delta=str(df_hs_compara.var_roubos.values[22]))

    with col2[1]:
        st.markdown('### Roubo de rua')
        st.metric(label="", value=str(
            df_hs_compara.roubo_rua.values[22]), delta=str(df_hs_compara.var_roubo_rua.values[22]))

    with col2[2]:
        st.markdown('### Roubo Veículos')
        st.metric(label="", value=str(
            df_hs_compara.roubo_veiculo.values[22]), delta=str(df_hs_compara.var_roubo_veiculo.values[22]))

    col3 = st.columns((1.6, 1.3, 1.3), gap='medium')

    with col3[0]:
        st.markdown('### Roubo de Carga')
        st.metric(label="", value=str(
            df_hs_compara.roubo_carga.values[22]), delta=str(df_hs_compara.var_roubo_carga.values[22]))

    with col3[1]:
        st.markdown('### Latrocínio')
        st.metric(label="", value=str(
            df_hs_compara.latrocinio.values[22]), delta=str(df_hs_compara.var_latrocinio.values[22]))

    with col3[2]:
        st.markdown('### Estelionato')
        st.metric(label="", value=str(
            df_hs_compara.estelionato.values[22]), delta=str(df_hs_compara.var_estelionato.values[22]))

    col4 = st.columns((1.6, 1.3, 1.3), gap='medium')

    with col4[0]:
        st.markdown('### Morte por interv. Policial')
        st.metric(label="", value=str(
            df_hs_compara.hom_por_interv_policial.values[22]), delta=str(df_hs_compara.var_hom_por_interv_policial.values[22]))

    with col4[1]:
        st.markdown('### Policiais mortos em serviço')
        st.metric(label="", value=str(
            df_hs_compara.pol_mortos_serv.values[22]), delta=str(df_hs_compara.var_pol_mortos_serv.values[22]))

    with col4[2]:
        st.markdown('### Apreensão de drogas')
        st.metric(label="", value=str(
            df_hs_compara.apreensao_drogas.values[22]), delta=str(df_hs_compara.var_apreensao_drogas.values[22]))


st.markdown("""
**Na comparação ANO contra ANO, tivemos os principais resultados:**
>
Os **registros de ocorrências** tiveram um aumento de 4.6% em relação a 2024, cerca de 42k registros a mais nas delegacias de polícia.
>
O indicador **Letalidade Violenta**, que corresponde à soma das vítimas de homicídio doloso, Morte por Intervenção de Agente do Estado, roubo seguido de morte (Latrocínio) e lesão corporal seguida de morte, apresentou aumento de 1,9%, 70 casos a mais.
>
O ano de 2025 registrou 70 casos a menos de **homicídio doloso** (quando há intenção de matar), e o crime de **latrocínio** (roubo seguido de morte) teve uma queda de 22 casos, contabilizando 77 vítimas.
>
Já o número de **feminicídios**, não é possível comparar com o ano anterior, pois o dataset disponibilizado pelo ISP, está incompleto para 2024(apenas 3 meses de registros).
Em 2025 foram registrados 104 **feminicídios** e 307 **tentativas desse delito**.
>
Os registros de **roubo** apresentaram uma queda de 8.6%, uma redução de 9.207 registros desse delito.
>
Destaca-se, nessa categoria, a queda de **9.4%** no indicador de **roubo de carga**.
Os indicadores **Roubo de Rua e Roubo de Veículo** registraram quedas de 2,7% e 18,4%, respectivamente.
>
Tivemos um aumento de 7.9% na **apreensão de drogas**, 1.901 registros a mais em relação ao ano anterior.


""")
