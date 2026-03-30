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


def toggle_expander():
    st.session_state.summary = not st.session_state.summary


def on_expander_change():
    if st.session_state.summary:
        st.toast("You opened the expander.")
    else:
        st.toast("You closed the expander.")


def toggle_expander1():
    st.session_state.summary1 = not st.session_state.summary1


def on_expander_change1():
    if st.session_state.summary1:
        st.toast("You opened the expander.")
    else:
        st.toast("You closed the expander.")
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
    ((df_hs_compara.letalidade_violenta.values[22])*1000)/365).round(0)

vlr_delta = ((((df_hs_compara.letalidade_violenta.values[21])*1000)/365).round(
    0))-((((df_hs_compara.letalidade_violenta.values[22])*1000)/365).round(0))


vlr_delta_fem = (
    df_hs_compara.feminicidio.values[21])-(df_hs_compara.feminicidio.values[22])

# Homicídio doloso por CISP
df_homiciodio_un = (df_anuario.groupby(['risp_desc', 'cisp', 'unidade_territorial'])['hom_doloso'].sum().reset_index()
                    ).sort_values(by='hom_doloso', ascending=False).head(10)

# Rank the 'Score' column in descending order
df_homiciodio_un['Rank'] = df_homiciodio_un['hom_doloso'].rank(ascending=False)

# Mortes por intervençao de agente do estado
df_interv_un = (df_anuario.groupby(['risp_desc', 'cisp', 'unidade_territorial'])['hom_por_interv_policial'].sum().reset_index()
                ).sort_values(by='hom_por_interv_policial', ascending=False).head(10)

##############################################################################################
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

# 4.3.2 Homicídio doloso
# por ano
hom1 = px.line(df_hs_compara, x='ano', y='hom_doloso',
               markers=True, text='hom_doloso',
               # height=600, width=800, #altura x largura
               line_shape="spline",
               template="plotly_dark",
               render_mode="svg",
               title="Homicídio doloso por Ano",
               labels=dict(ano="Ano", hom_doloso="Homicídio (k)")
               )
hom1.update_xaxes(type="category", title=None)
hom1.update_traces(line_width=2, textposition='top center')


hom2 = px.bar(df_hs_compara, x="ano", y="var_hom_doloso", title="Diferença YxY(%)", template="plotly_dark", text_auto=True,
              # height=300, width=1160,  #largura
              # , hover_data=['ano', 'dif','var']
              labels=dict(ano="Ano", var_hom_doloso='Variação')
              )
hom2.update_traces(textangle=0, textfont_size=12, textposition='outside',
                   cliponaxis=False, marker_color=df_hs_compara["color_hom"])
hom2.update_yaxes(showticklabels=False, showgrid=False,
                  visible=False, fixedrange=True)
hom2.update_xaxes(showgrid=False, visible=False,
                  fixedrange=True, type="category", title=None)

# por mes
hommes = px.line(df_anuario.groupby(['mes', 'mes_char'])['hom_doloso'].sum().reset_index(), x='mes_char', y=['hom_doloso'],
                 markers=True, text='value', line_shape="spline", template="plotly_dark",
                 title="Homicídio doloso por mês", color_discrete_sequence=px.colors.sequential.Blackbody_r,
                 labels=dict(mes_char="Mês", value="Homicídio",
                             variable="Homicídio")
                 )
hommes.update_xaxes(type="category", title=None)
hommes.update_layout(showlegend=False)
hommes.update_traces(line_width=2, textposition='top center')

# Homicídio doloso por RISP
hom_risp = px.pie(df_anuario.groupby(['risp_desc'])['hom_doloso'].sum().reset_index(), values='hom_doloso', names='risp_desc',
                  hole=0.5, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Blues_r,
                  labels=dict(hom_doloso="Homicídio", risp_desc="RISP")
                  )

hom_cisp = go.Figure(data=[go.Table(

    header=dict(values=['Rank', 'RISP', 'Delagacia', 'Unidade Territorial', 'Total'],
                fill_color='royalblue',
                align='left'),
    cells=dict(values=[df_homiciodio_un.Rank, df_homiciodio_un.risp_desc, df_homiciodio_un.cisp, df_homiciodio_un.unidade_territorial, df_homiciodio_un.hom_doloso],
               fill_color='lightskyblue',
               align='center',
               font=dict(color='darkslategray', size=11)
               ))
], layout=go.Layout(template="plotly_dark"))

# 4.3.3 Roubos seguido de morte (latrocínio)
# Por ano
lat_ano = px.line(df_hist_anual.groupby(['ano'])['latrocinio'].sum().reset_index(), x='ano', y=['latrocinio'],
                  markers=True, text='value', line_shape="spline", template="plotly_dark",
                  title="Latrocínio", height=525, width=850,
                  color_discrete_sequence=px.colors.sequential.Blackbody_r,
                  labels=dict(ano="Ano", value="Latrocínio",
                              variable="Latrocínio")
                  )
lat_ano.update_xaxes(type="category", title=None)
lat_ano.update_layout(showlegend=False)
lat_ano.update_traces(line_width=2, textposition='top center')

# Por mes
lat_mes = px.line(df_anuario.groupby(['mes', 'mes_char'])['latrocinio'].sum().reset_index(), x='mes_char', y=['latrocinio'],
                  markers=True, text='value', line_shape="spline", template="plotly_dark",
                  title="Latrocínio por mês", color_discrete_sequence=px.colors.sequential.Blackbody_r,
                  labels=dict(mes_char="Mês", value="Latrocínio",
                              variable="Latrocínio")
                  )
lat_mes.update_xaxes(type="category", title=None)
lat_mes.update_layout(showlegend=False)
lat_mes.update_traces(line_width=2, textposition='top center')

# 4.3.4 Lesão corporal seguida de morte
les_ano = px.line(df_hist_anual.groupby(['ano'])['lesao_corp_morte'].sum().reset_index(), x='ano', y=['lesao_corp_morte'],
                  markers=True, text='value', line_shape="spline", template="plotly_dark",
                  title="Lesão corporal seguida de morte por ano",
                  height=525, width=850, color_discrete_sequence=px.colors.sequential.Blackbody_r,
                  labels=dict(ano="Ano", value="lesão corporal",
                              variable="lesão corporal")
                  )
les_ano.update_xaxes(type="category", title=None)
les_ano.update_layout(showlegend=False)
les_ano.update_traces(line_width=2, textposition='top center')
# Por mes
les_mes = px.line(df_anuario.groupby(['mes', 'mes_char'])['lesao_corp_morte'].sum().reset_index(), x='mes_char', y=['lesao_corp_morte'],
                  markers=True, text='value', line_shape="spline", template="plotly_dark",
                  title="Lesão corporal seguida de morte por mês",
                  color_discrete_sequence=px.colors.sequential.Blackbody_r,
                  labels=dict(mes_char="Mês", value="lesão corporal",
                              variable="lesão corporal")
                  )
les_mes.update_xaxes(type="category", title=None)
les_mes.update_layout(showlegend=False)
les_mes.update_traces(line_width=2, textposition='top center')

# 4.3.5 Mortes por Intervenção de Agente do Estado
# Por ano
agente_ano = px.line(df_hist_anual.groupby(['ano'])['hom_por_interv_policial'].sum().reset_index(), x='ano', y=['hom_por_interv_policial'],
                     markers=True, text='value', line_shape="spline", template="plotly_dark",
                     title="Mortes por Intervenção de Agente do Estado por ano",
                     height=525, width=850, color_discrete_sequence=px.colors.sequential.Blackbody_r,
                     labels=dict(ano="Ano", value="Mortes", variable="Mortes")
                     )
agente_ano.update_xaxes(type="category", title=None)
agente_ano.update_layout(showlegend=False)
agente_ano.update_traces(line_width=2, textposition='top center')
# Poe mes
agente_mes = px.line(df_anuario.groupby(['mes', 'mes_char'])['hom_por_interv_policial'].sum().reset_index(), x='mes_char', y=['hom_por_interv_policial'],
                     markers=True, text='value', line_shape="spline", template="plotly_dark",
                     title="Mortes por Intervenção de Agente do Estado por mês",
                     color_discrete_sequence=px.colors.sequential.Blackbody_r,
                     labels=dict(mes_char="Mês", value="Mortes",
                                 variable="Mortes")
                     )
agente_mes.update_xaxes(type="category", title=None)
agente_mes.update_layout(showlegend=False)
agente_mes.update_traces(line_width=2, textposition='top center')

# grafico de calor
agente_heat = px.density_heatmap(df_hist_anual.groupby(['ano', 'mes', 'mes_char'])['hom_por_interv_policial'].sum().reset_index().sort_values(['ano', 'mes'], ascending=[True, True]),
                                 x="mes_char", y="ano", z="hom_por_interv_policial",
                                 histfunc="sum", text_auto=True,
                                 labels=dict(mes_char="Mês",  ano="Ano",
                                             hom_por_interv_policial="Mortes"),
                                 color_continuous_scale="RdYlBu_r", template="plotly_dark"
                                 )

agente_heat.layout['coloraxis']['colorbar']['title'] = 'Mortes'
agente_heat.update_yaxes(type="category")
agente_heat.update_xaxes(type="category")

# Por CISP
agente_tb = go.Figure(data=[go.Table(

    header=dict(values=['RISP', 'Delagacia', 'Unidade Territorial', 'Total'],
                fill_color='royalblue',
                align='left'),
    cells=dict(values=[df_interv_un.risp_desc, df_interv_un.cisp, df_interv_un.unidade_territorial, df_interv_un.hom_por_interv_policial],
               fill_color='lightskyblue',
               align='center',
               font=dict(color='darkslategray', size=11)
               ))
], layout=go.Layout(template="plotly_dark"))

# 4.3.6 Vitimização policial
vit_pol_ano = px.line(df_hist_anual.groupby(['ano'])['pol_mortos_serv'].sum().reset_index(), x='ano', y=['pol_mortos_serv'],
                      markers=True, text='value', line_shape="spline", template="plotly_dark",
                      title="Policiais mortos em serviço", height=525, width=850,
                      color_discrete_sequence=px.colors.sequential.Blackbody_r,
                      labels=dict(ano="Ano", value="Mortes", variable="Mortes")
                      )
vit_pol_ano.update_xaxes(type="category", title=None)
vit_pol_ano.update_layout(showlegend=False)
vit_pol_ano.update_traces(line_width=2, textposition='top center')

vit_pol_mes = px.line(df_anuario.groupby(['mes', 'mes_char'])['pol_mortos_serv'].sum().reset_index(), x='mes_char', y=['pol_mortos_serv'],
                      markers=True, text='value', line_shape="spline", template="plotly_dark",
                      title="Policiais mortos em serviço",
                      color_discrete_sequence=px.colors.sequential.Blackbody_r,
                      labels=dict(mes_char="Mês", value="Mortes",
                                  variable="Mortes")
                      )
vit_pol_mes.update_xaxes(type="category", title=None)
vit_pol_mes.update_layout(showlegend=False)
vit_pol_mes.update_traces(line_width=2, textposition='top center')

vit_pol = px.bar(df_hist_anual.groupby('ano')[['pol_militares_mortos_serv', 'pol_civis_mortos_serv']].apply(lambda x: x.sum()).reset_index(),
                 x="ano", y=['pol_militares_mortos_serv', 'pol_civis_mortos_serv'],
                 labels=dict(pol_militares_mortos_serv="Polícial Militar",
                             pol_civis_mortos_serv="Policial Civil", ano="Ano", value="Mortes", variable="Categoria"),
                 color_discrete_sequence=px.colors.sequential.Blues_r,
                 template="plotly_dark", text='value'
                 )
vit_pol.update_layout(legend=dict(yanchor="top", y=-0.15, xanchor="left", x=0))
vit_pol.update_traces(textfont_size=12, textangle=0,
                      textposition="outside", cliponaxis=False)
vit_pol.update_xaxes(type="category", title=None)

##################################################################################
##################################################################################
# Dashboard Main Panel


st.markdown("# Crimes contra a vida")
st.markdown("### :blue[Resumo dos principais resultados]")

with st.expander("Indicadores    (click aqui para ver)", expanded=True, on_change=on_expander_change1, key="summary1"):

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
        st.markdown('### Morte por Intervenção de Agente do Estado')
        st.metric(label="", value=int(
            df_hs_compara.hom_por_interv_policial.values[22]), delta=str(df_hs_compara.var_hom_por_interv_policial.values[22]), delta_color="inverse", border=True)

    col3 = st.columns((1.6, 1.6), gap='small')

    with col3[0]:
        # Quadro com o total e a variação
        st.markdown(
            '#### Feminicídios')
        st.metric(label="", value=int(
            df_hs_compara.feminicidio.values[22]), delta=int(vlr_delta_fem), delta_color="inverse", border=True)

    with col3[1]:
        st.markdown('### Policiais mortos em serviço')
        st.metric(label="", value=int(
            df_hs_compara.pol_mortos_serv.values[22]), delta=str(df_hs_compara.var_pol_mortos_serv.values[22]), delta_color="inverse", border=True)

    st.button("Recolher", key=1, on_click=toggle_expander1)

st.markdown("### :blue[Letalidade Violenta]")
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

st.markdown(
    "#### :blue[Análise dos delitos que compõem a Letalidade Violenta]")
st.markdown("### :blue[Homicídio doloso]")
with st.expander("Analises", expanded=True, on_change=on_expander_change, key="summary"):
    st.plotly_chart(hom1, use_container_width=True)
    st.plotly_chart(hom2, use_container_width=True)
    st.markdown("""Destacamos que o estado registrou 2.833 vítimas de **homicídio doloso**,
                representando uma **queda de 2.48%**, menos setenta e duas vítimas se comparado com 2024.
                """)

    st.plotly_chart(hommes, use_container_width=True)
    st.markdown("""
                **Janeiro** foi o mês com mais registros de homicídio doloso no estado no ano de 2025.
                """)

    st.markdown("### :blue[Por RISP]")
    st.plotly_chart(hom_risp, use_container_width=True)
    st.markdown("""
                A **Baixada Fluminense** é a região que mais registrou homicídios, foram 779, correspondendo a 27.5% do Estado.
                """)
    st.markdown("### :blue[Homicídio por CISP e unidade territorial]")
    st.plotly_chart(hom_cisp, use_container_width=True)
    st.markdown("""
                A delegacia que mais registrou homicídios, está localizada na Baixada Fluminense, e atende as localidades de:
                >
                Posse, Austin, Miguel Couto, Vila de Cava e Tinguá
                """)
    st.button("Recolher", key=2, on_click=toggle_expander)

st.markdown("### :blue[Latrocínio]")
with st.expander("Analises", expanded=True):
    st.plotly_chart(lat_ano, use_container_width=True)
    st.markdown("""
                Foram 77 vítimas de roubos seguido de morte (latrocínio) no estado, apresentando uma queda de 22 casos no número de vítimas em relação ao ano anterior.
                """)
    st.plotly_chart(lat_mes, use_container_width=True)
    st.markdown("""
                No mês de dezembro foram registrados 13 casos, um aumento de 117% em relação ao mês anterior.
                """)

st.markdown("### :blue[Lesão corporal seguida de morte]")
with st.expander("Analises", expanded=True):
    st.plotly_chart(les_ano, use_container_width=True)
    st.markdown("""
                O crime de lesão corporal seguida de morte contabilizou 67 vítimas, 2 casos a menos em relacão ao ano anterior.
                """)
    st.plotly_chart(les_mes, use_container_width=True)
    st.markdown("""
                Os meses com mais casos foram Janeiro e Março, e no final do ano vemos uma queda de 67% nesse delito.
                """)

st.markdown("### :blue[Mortes por Intervenção de Agente do Estado]")
with st.expander("Analises", expanded=True):
    st.plotly_chart(agente_ano, use_container_width=True)
    st.markdown("""
                As Mortes por Intervenção de Agente do Estado subiram 13,4% (797 no total do ano) em relação a 2024, que havia registrado 703 vítimas.
                """)
    st.plotly_chart(agente_mes, use_container_width=True)
    st.markdown("""
                No mês de **Outubro** foram registrados 175 casos desse delito, um aumento de 250% em relação ao mês anterior.
                >
                No dia 28/10/2025, ocorreu uma operação policial nos complexos do Alemão e da Penha, onde 121 pessoas morreram e 113 foram presas.
                >
                De acordo com a Polícia Civil, dentre os 121 mortos, 4 eram policiais.
                """)
    st.plotly_chart(agente_heat, use_container_width=True)
    st.markdown("""
                No No gráfico de calor, podemos verificar com mais clareza, os meses com mais casos ao longo dos anos.
                2019 registrou o maior número de mortes por policiais no estado do Rio desde o início da série de dados. 
                Julho foi o mês que mais acumulou mortes por intervenção de agentes do estado, 
                somando **195 vítimas**, 50% maior do que o registrado no mesmo período do ano anterior.
                """)
    st.markdown(":blue[por CISP e unidade territorial]")
    st.plotly_chart(agente_tb, use_container_width=True)

st.markdown("### :blue[Vitimização policial]")
with st.expander("Analises", expanded=True):
    st.plotly_chart(vit_pol_ano, use_container_width=True)
    st.markdown("""
                Destacamos o aumento no número de policiais mortos que cresceu **58,3%** em comparação com o ano de 2024.
                """)
    st.plotly_chart(vit_pol_mes, use_container_width=True)
    st.markdown(
        " :blue[Considerando a separação entre Polícia Militar e Polícia Civil]")
    st.plotly_chart(vit_pol, use_container_width=True)
