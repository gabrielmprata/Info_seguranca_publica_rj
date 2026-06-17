# 👮‍♂️ Informações de Segurança Pública do Estado do Rio de Janeiro :police_car:
Dados Abertos do Instituto de segurança pública (ISP)
<p align="left">
<img src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=RED&style=for-the-badge" #vitrinedev/>  

<img src="http://img.shields.io/static/v1?label=vers%C3%A3o%20do%20projeto&message=v2.0.1&color=red&style=for-the-badge&logo=github"/>
</p>
<br><br>

# 🖥️ Demo App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_red.svg)](https://anuario-seguranca-publica.streamlit.app/)
<br></br>

![ezgif-24d0f878e9a7bf8d](https://github.com/user-attachments/assets/2be23875-c5d2-4cc7-81bd-52cbe50a9e76)


<br><br>

# 🧠 Sobre o Projeto

Uma solução analítica desenvolvida para monitorar, analisar e interpretar dados de segurança pública do estado do Rio de Janeiro utilizando dados oficiais do Instituto de Segurança Pública do RJ.
>
O projeto foi construído com foco em:
>
* análise orientada à tomada de decisão
* identificação de padrões criminais
* monitoramento de indicadores críticos
* análise geoespacial e temporal
<br><br>
# :radio_button: Objetivo 
Criar um Dashboard em **Power BI**, para a visualização das informações do anuário de Segurança Pública do Estado do Rio de Janeiro.
>
E apresentar analises comparativas, dos principais indicadores de criminalidade e de atividade policial do estado no período de 2003 a 2025.
>
Os dados são provenientes do Instituto de Segurança Pública do Estado do Rio de Janeiro, com séries históricas tratadas e modeladas para análise temporal e geoespacial.
>
As informações contidas nesse estudo foram extraídas dos registros de ocorrências lavrados nas delegacias de polícia da Secretaria de Estado da Polícia Civil (SEPOL).
>
Os dados apresentados nesse **estudo acadêmico**, tem o objetivo de desenvolver habilidades técnicas, utilizando **dados abertos**. 
<br><br>
# :floppy_disk: Coleta de Dados
>
Os dados foram coletados do sítio do Instituto de segurança pública (ISP), no dia **01/03/2026**.
<br>
<img width="260" align="left" height="46" alt="image" src="https://github.com/user-attachments/assets/f4dee793-9320-4e7e-b483-5c9ff109bb03" />
<br><br>
>
**Dataset:** Estatísticas de segurança: série histórica mensal por área de delegacia desde 01/2003.
>
https://www.ispdados.rj.gov.br/estatistica.html
>
---
>
**Dataset:** População Residente - Estudo de Estimativas Populacionais por Município
>
https://tabnet.datasus.gov.br/cgi/deftohtm.exe?ibge/cnv/popsvs2024br.def
>
---
>
**Dataset:** Relação das Regiões, Áreas e Circunscrições Integradas de Segurança Pública (Bairros/Distritos, Municípios e Regiões de Governo).
>
https://www.ispdados.rj.gov.br/Conteudo.html
>
As Circunscrições Integradas de Segurança Pública - CISP, correspondem às áreas territoriais de atuação e responsabilidade conjunta das delegacias distritais da Secretaria de Estado de Polícia Civil (SEPOL) e das companhias integradas da Secretaria de Estado de Polícia Militar (SEPM)
>
<br><br>

# :recycle: Pré-processamento
>
[![Colab Notebook](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gabrielmprata/seguranca_publica_pwrbi/blob/main/PREP_anuario_seguranca_publica_pwr_bi.ipynb)
>
Esta é a etapa mais demorada e trabalhosa do projeto de ciência de dados, e estima-se que consuma pelo menos 70% do tempo total do projeto.
>
Após coletar e analisar os dados na etapa anterior, é necessário limpar, transformar e apresentar melhor os seus dados, a fim de obter, na próxima etapa, os melhores resultados possíveis nos algoritmos de machine learning ou simplesmente apresentar dados mais confiáveis para os clientes em soluções de
business intelligence.
>
Como o nosso objetivo é criar um Dashboard em **Power BI**, iremos minimizar ao máximo o tamanho e a granularidade dos Datasets disponibilizados, a fim de termos um ambiente mais "leve" para a leitura dos dados.
>
🛠️ Principais técnicas utilizadas:
>
* **Limpeza:** Consiste na verificação da consistência das informações, correção de possíveis erros de preenchimento ou eliminação de valores desconhecidos, redundantes ou não pertencentes ao domínio.

* **Padronização de dados:** Dentro da programação, possuímos alguns padrões de escrita para nomes de variáveis, funções, classes e assim por diante.
Nesse projeto iremos utilizar **Snake Case (snake_case)** nesse estilo, todas as letras são minúsculas e as palavras são separadas por um underscore(_).

* **Agregação:** Também pode ser considerada uma técnica de redução de dimensionalidade, pois reduz o número de linhas e colunas de um dataset.
>
 * **Tratamendo de dados faltantes (missing):** Identificamos e, em seguida, tratamos com um valor adequado. Não foi necessario a exclusão desses registros.

# 🔨 Ferramentas utilizadas

<img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" width="40" height="40"/><img loading="lazy" src="https://img.icons8.com/?size=100&id=3sGOUDo9nJ4k&format=png&color=000000" width="40" height="40"/><img loading="lazy" src="https://img.icons8.com/?size=100&id=8gfeOoqrHqJU&format=png&color=000000" width="40" height="40"/>
</br>
</br>
# 🎨 UI/UX
Acesse o design de interface no Figma!
>
<a href="https://www.figma.com/design/eu7X1863DV4e3wshDA9VBX/Dash_Seguranca?m=auto&t=Kr247IkcIUXa27xq-6"><img src="https://img.icons8.com/?size=100&id=8gfeOoqrHqJU&format=png&color=000000" width="40" height="40" alt="Acesse"></a>
</br></br>
# 📈 Indicadores

* Crimes contra a vida
* Crimes contra o patrimonio
* Atividade Policial

</br></br>
# 📊 Principais Funcionalidades

## 🚨 Monitoramento de KPIs

* Total de Crimes por categoria e tipo
* Taxa por 10 mil habitantes
* Variação percentual mensal e anual


## 🗺️ Análise Geoespacial

* Distribuição de crimes por município
* Distribuição de crimes por RISP (Mapa personalizado)
* Identificação visual de áreas prioritárias

## 📈 Análise Temporal

* Evolução histórica da criminalidade
* Tendências de crescimento e redução

  
</br></br>
# 📌 Diferenciais do Projeto

✔ Dados públicos oficiais
>
✔ Modelagem dimensional profissional
>
✔ Design orientado à UX
>
✔ Indicadores analíticos avançados
>
✔ Análise geoespacial integrada
>
✔ Estrutura escalável para expansão futura
</br></br>
# 🧱 Arquitetura de Dados

O projeto utiliza modelagem dimensional no padrão **Star Schema**, garantindo:

* melhor performance;
* escalabilidade;
* facilidade analítica.
</br></br>
# 🔮 Próximos Passos

* Implementação de modelos preditivos (Forecast/ ARIMA / Prophet)
* Atualização automatizada dos dados
</br></br>
# 👨‍💼💻 Author 
Gabriel Prata
