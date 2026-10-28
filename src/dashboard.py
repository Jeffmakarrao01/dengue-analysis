import streamlit as st
import pandas as pd
import plotly.express as px


# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================

st.set_page_config(
    page_title="Dashboard de Dengue",
    page_icon="🦟",
    layout="wide"
)


# ==============================
# TÍTULO
# ==============================

st.title("🦟 Dashboard de Análise da Dengue")

st.markdown(
    """
    Explore os dados de dengue de **2024** por meio de filtros,
    indicadores e gráficos interativos.
    """
)

st.divider()


# ==============================
# CARREGAMENTO DOS DADOS
# ==============================

arquivo = "dados/dengue_tratado.csv"

df = pd.read_csv(arquivo)


# ==============================
# FILTROS
# ==============================

st.sidebar.header("🔎 Filtros")
st.sidebar.caption("Personalize os dados exibidos no painel.")

anos = sorted(df["nu_ano"].dropna().unique())

ano_selecionado = st.sidebar.selectbox(
    "Selecione o ano",
    anos
)

df_filtrado = df[
    df["nu_ano"] == ano_selecionado
]
sexos = sorted(df_filtrado["cs_sexo"].dropna().unique())

sexo_selecionado = st.sidebar.multiselect(
    "Selecione o sexo",
    sexos,
    default=sexos
)

df_filtrado = df_filtrado[
    df_filtrado["cs_sexo"].isin(sexo_selecionado)
]
# ==============================

# ==============================
# INFORMAÇÕES GERAIS
# ==============================

st.subheader("📊 Informações gerais", divider="gray")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="📋 Total de registros",
        value=len(df_filtrado),
        help="Quantidade de registros conforme os filtros selecionados.",
        border=True
    )

with col2:
    st.metric(
        label="🗂️ Total de variáveis",
        value=len(df.columns),
        help="Quantidade total de variáveis disponíveis no conjunto de dados.",
        border=True
    )



# ==============================
# TABELA
# ==============================

st.dataframe(
    df_filtrado,
    use_container_width=True,
    height=400
)
# ==============================
# CASOS POR SEXO
# ==============================

st.subheader("👥 Casos por sexo", divider="gray")

contagem_sexo = df_filtrado["cs_sexo"].value_counts()

contagem_sexo.index = contagem_sexo.index.map({
    "F": "Feminino",
    "M": "Masculino"
})

fig_sexo = px.bar(
    contagem_sexo,
    x=contagem_sexo.index,
    y=contagem_sexo.values,
    labels={
        "x": "Sexo",
        "y": "Quantidade de casos"
    },
    title="Distribuição dos casos por sexo"
)

fig_sexo.update_layout(
    title_x=0.5
)

st.plotly_chart(fig_sexo, use_container_width=True)

# ==============================
# CASOS POR RAÇA/COR
# ==============================

st.subheader("🎨 Casos por raça/cor", divider="gray")

contagem_raca = df_filtrado["cs_raca"].value_counts().sort_index()

nomes_raca = {
    1: "Branca",
    2: "Preta",
    3: "Amarela",
    4: "Parda",
    5: "Indígena",
    9: "Ignorado"
}

contagem_raca.index = contagem_raca.index.map(
    lambda x: nomes_raca.get(int(x), str(x))
)

fig_raca = px.bar(
    x=contagem_raca.index,
    y=contagem_raca.values,
    text=contagem_raca.values,
    labels={
        "x": "Raça/cor",
        "y": "Quantidade de casos"
    },
    title="Distribuição dos casos por raça/cor"
)

fig_raca.update_traces(
    textposition="outside"
)

fig_raca.update_layout(
    xaxis_title="Raça/cor",
    yaxis_title="Quantidade de casos",
    title_x=0.5
)

st.plotly_chart(
    fig_raca,
    use_container_width=True
)
# ==============================
# CLASSIFICAÇÃO FINAL DOS CASOS
# ==============================

st.subheader("📊 Evolução dos casos por desfecho", divider="gray")

classificacao = df_filtrado["classi_fin"].value_counts().sort_index()

classificacao.index = classificacao.index.map({
    8: "Descartado",
    10: "Dengue",
    11: "Dengue com sinais de alarme",
    12: "Dengue grave"
})

grafico_classificacao = px.bar(
    x=classificacao.index,
    y=classificacao.values,
    text=classificacao.values,
    labels={
        "x": "Classificação final",
        "y": "Quantidade de casos"
    },
    title="Distribuição dos casos por classificação final"
)

grafico_classificacao.update_traces(
    textposition="outside"
)

grafico_classificacao.update_layout(
    xaxis_title="Classificação final",
    yaxis_title="Quantidade de casos",
    title_x=0.5
)

st.plotly_chart(
    grafico_classificacao,
    use_container_width=True
)
# ==============================
# EVOLUÇÃO DOS CASOS
# ==============================

st.subheader("📈 Evolução dos casos", divider="gray")

evolucao = (
    df_filtrado["evolucao"]
    .fillna(-1)
    .value_counts()
    .sort_index()
)


evolucao.index = evolucao.index.map({
    -1: "Sem informação",
    0: "Ignorado",
    1: "Cura",
    2: "Óbito por dengue",
    9: "Óbito por outras causas"
})

grafico_evolucao = px.bar(
    x=evolucao.index,
    y=evolucao.values,
    text=evolucao.values,
    labels={
        "x": "Evolucao",
        "y": "Quantidade de casos"
    },
    title="Distribuição dos casos por evolução"
)

grafico_evolucao.update_traces(
    textposition="outside"
)

grafico_evolucao.update_layout(
    xaxis_title="Evolução",
    yaxis_title="Quantidade de casos",
    title_x=0.5
)

st.plotly_chart(
    grafico_evolucao,
    use_container_width=True
)
# ==============================
# HOSPITALIZAÇÃO
# ==============================

st.subheader("🏥 Hospitalização", divider="gray")

hospitalizacao = df_filtrado["hospitaliz"].value_counts()
st.write("Conferência dos códigos de hospitalização:")
st.write(df_filtrado["hospitaliz"].value_counts(dropna=False).sort_index())

hospitalizacao.index = hospitalizacao.index.map({
    1.0: "Sim",
    2.0: "Não",
    9.0: "Ignorado"
})

grafico_hospitalizacao = px.bar(
    x=hospitalizacao.index,
    y=hospitalizacao.values,
    text=hospitalizacao.values,
    labels={
        "x": "Hospitalização",
        "y": "Quantidade de casos"
    },
    title="Distribuição dos casos por hospitalização"
)

grafico_hospitalizacao.update_traces(
    textposition="outside"
)

grafico_hospitalizacao.update_layout(
    xaxis_title="Hospitalização",
    yaxis_title="Quantidade de casos",
    title_x=0.5
)

st.plotly_chart(
    grafico_hospitalizacao,
    use_container_width=True
)
# ==============================
# FREQUÊNCIA DOS SINTOMAS
# ==============================

st.subheader("🤒 Frequência dos sintomas", divider="gray")

sintomas = {
    "Febre": df_filtrado["febre"],
    "Mialgia": df_filtrado["mialgia"],
    "Cefaleia": df_filtrado["cefaleia"],
    "Exantema": df_filtrado["exantema"],
    "Vômito": df_filtrado["vomito"],
    "Náusea": df_filtrado["nausea"],
    "Artralgia": df_filtrado["artralgia"]
}

casos_sintomas = []

for sintoma, coluna in sintomas.items():

    quantidade = (coluna == 1).sum()

    casos_sintomas.append({
        "Sintoma": sintoma,
        "Casos": quantidade
    })

df_sintomas = pd.DataFrame(casos_sintomas)

st.dataframe(
    df_sintomas,
    use_container_width=True,
    hide_index=True
)

grafico_sintomas = px.bar(
    df_sintomas,
    x="Sintoma",
    y="Casos",
    text="Casos",
    title="Frequência dos sintomas"
)

grafico_sintomas.update_traces(
    textposition="outside"
)

grafico_sintomas.update_layout(
    xaxis_title="Sintoma",
    yaxis_title="Quantidade de casos",
    title_x=0.5
)

st.plotly_chart(
    grafico_sintomas,
    use_container_width=True
)
# ==============================
# EVOLUÇÃO DOS CASOS POR MÊS
# ==============================

st.subheader("📈 Evolução mensal dos casos", divider="gray")

df_filtrado = df_filtrado.copy()

df_filtrado["dt_notific"] = pd.to_datetime(
    df_filtrado["dt_notific"],
    errors="coerce"
)
st.write(
    "Registros sem data de notificação:",
    df_filtrado["dt_notific"].isna().sum()
)


dados_mensais = df_filtrado.dropna(subset=["dt_notific"]).copy()

dados_mensais["Mês"] = (
    dados_mensais["dt_notific"].dt.to_period("M").astype(str)
)

casos_por_mes = (
    dados_mensais
    .groupby("Mês")
    .size()
    .reset_index(name="Casos")
)

st.dataframe(
    casos_por_mes[["Mês", "Casos"]],
    use_container_width=True,
    hide_index=True
)

grafico_evolucao = px.line(
    casos_por_mes,
    x="Mês",
    y="Casos",
    markers=True,
    text="Casos",
    title="Evolução dos casos de dengue por mês"
)

grafico_evolucao.update_traces(
    textposition="top center"
)

grafico_evolucao.update_layout(
    xaxis_title="Mês",
    yaxis_title="Quantidade de casos",
    title_x=0.5
)

st.plotly_chart(
    grafico_evolucao,
    use_container_width=True
)
# ==============================
# DISTRIBUIÇÃO POR FAIXA ETÁRIA
# ==============================
df_filtrado = df_filtrado.copy()
st.subheader("👥 Distribuição dos casos por faixa etária", divider="gray")

# Calcula a idade aproximada no ano da notificação
df_filtrado["idade"] = df_filtrado["nu_ano"] - df_filtrado["ano_nasc"]

# Cria as faixas etárias
def classificar_faixa_etaria(idade):

    if pd.isna(idade):
        return "Ignorado"

    if idade < 10:
        return "0–9 anos"

    elif idade < 20:
        return "10–19 anos"

    elif idade < 30:
        return "20–29 anos"

    elif idade < 40:
        return "30–39 anos"

    elif idade < 50:
        return "40–49 anos"

    elif idade < 60:
        return "50–59 anos"

    else:
        return "60 anos ou mais"


df_filtrado["faixa_etaria"] = df_filtrado["idade"].apply(
    classificar_faixa_etaria
)

# Ordem das faixas
ordem_faixas = [
    "0–9 anos",
    "10–19 anos",
    "20–29 anos",
    "30–39 anos",
    "40–49 anos",
    "50–59 anos",
    "60 anos ou mais",
    "Ignorado"
]

contagem_idade = (
    df_filtrado["faixa_etaria"]
    .value_counts()
    .reindex(ordem_faixas, fill_value=0)
    .reset_index()
)

contagem_idade.columns = [
    "Faixa etária",
    "Casos"
]

# Remove Ignorado se não houver registros
contagem_idade = contagem_idade[
    (contagem_idade["Casos"] > 0) |
    (contagem_idade["Faixa etária"] != "Ignorado")
]

# Gráfico
grafico_idade = px.bar(
    contagem_idade,
    x="Faixa etária",
    y="Casos",
    text="Casos",
    title="Distribuição dos casos por faixa etária"
)

grafico_idade.update_traces(
    textposition="outside"
)

grafico_idade.update_layout(
    xaxis_title="Faixa etária",
    yaxis_title="Quantidade de casos",
    title_x=0.5
)

st.plotly_chart(
    grafico_idade,
    use_container_width=True
)

# Tabela com a quantidade de casos por faixa etária
st.dataframe(
    contagem_idade,
    use_container_width=True,
    hide_index=True
)
st.subheader("🩺 Distribuição dos casos por comorbidades", divider="gray")

# Diabetes
diabetes = df_filtrado["diabetes"].map({
    1: "Sim",
    2: "Não",
    9: "Ignorado"
}).fillna("Ignorado")

contagem_diabetes = (
    diabetes.value_counts()
    .reindex(["Sim", "Não", "Ignorado"], fill_value=0)
    .reset_index()
)

contagem_diabetes.columns = ["Resposta", "Casos"]

st.write("**Diabetes**")

grafico_diabetes = px.bar(
    contagem_diabetes,
    x="Resposta",
    y="Casos",
    text="Casos",
    title="Distribuição dos casos de diabetes"
)

grafico_diabetes.update_traces(textposition="outside")

grafico_diabetes.update_layout(
    xaxis_title="Resposta",
    yaxis_title="Quantidade de casos",
    title_x=0.5
)

st.plotly_chart(
    grafico_diabetes,
    use_container_width=True
)

st.dataframe(
    contagem_diabetes,
    use_container_width=True,
    hide_index=True
)


# Hipertensão
hipertensao = df_filtrado["hipertensa"].map({
    1: "Sim",
    2: "Não",
    9: "Ignorado"
}).fillna("Ignorado")

contagem_hipertensao = (
    hipertensao.value_counts()
    .reindex(["Sim", "Não", "Ignorado"], fill_value=0)
    .reset_index()
)

contagem_hipertensao.columns = ["Resposta", "Casos"]

st.write("**Hipertensão**")

grafico_hipertensao = px.bar(
    contagem_hipertensao,
    x="Resposta",
    y="Casos",
    text="Casos",
    title="Distribuição dos casos de hipertensão"
)

grafico_hipertensao.update_traces(textposition="outside")

grafico_hipertensao.update_layout(
    xaxis_title="Resposta",
    yaxis_title="Quantidade de casos",
    title_x=0.5
)

st.plotly_chart(
    grafico_hipertensao,
    use_container_width=True
)

st.dataframe(
    contagem_hipertensao,
    use_container_width=True,
    hide_index=True
)
# ==============================
# CRITÉRIO DE CONFIRMAÇÃO
# ==============================

st.subheader("🔬 Critério de confirmação dos casos", divider="gray")

contagem_criterio = (
    df_filtrado["criterio"]
    .fillna("Ignorado")
    .astype(str)
    .value_counts()
    .reset_index()
)

contagem_criterio.columns = [
    "Critério",
    "Casos"
]

grafico_criterio = px.bar(
    contagem_criterio,
    x="Critério",
    y="Casos",
    text="Casos",
    title="Distribuição dos casos por critério de confirmação"
)

grafico_criterio.update_traces(
    textposition="outside"
)

grafico_criterio.update_layout(
    xaxis_title="Critério de confirmação",
    yaxis_title="Quantidade de casos",
    title_x=0.5
)

st.plotly_chart(
    grafico_criterio,
    use_container_width=True
)

st.dataframe(
    contagem_criterio,
    use_container_width=True,
    hide_index=True
)
# ==============================
# ORIGEM DOS CASOS
# ==============================

st.subheader("📍 Origem dos casos de dengue", divider="gray")

origem = df_filtrado["tpautocto"].map({
    1: "Autóctone",
    2: "Não autóctone",
    3: "Indeterminado"
}).fillna("Ignorado")

contagem_origem = (
    origem.value_counts()
    .reindex(
        ["Autóctone", "Não autóctone", "Indeterminado", "Ignorado"],
        fill_value=0
    )
    .reset_index()
)

contagem_origem.columns = [
    "Origem",
    "Casos"
]

grafico_origem = px.bar(
    contagem_origem,
    x="Origem",
    y="Casos",
    text="Casos",
    title="Distribuição dos casos por origem"
)

grafico_origem.update_traces(
    textposition="outside"
)

grafico_origem.update_layout(
    xaxis_title="Origem do caso",
    yaxis_title="Quantidade de casos",
    title_x=0.5
)

st.plotly_chart(
    grafico_origem,
    use_container_width=True
)

st.dataframe(
    contagem_origem,
    use_container_width=True,
    hide_index=True
)
# ==============================
# ESCOLARIDADE
# ==============================

st.subheader("🎓 Distribuição dos casos por escolaridade", divider="gray")

escolaridade = df_filtrado["cs_escol_n"].map({
    1: "1ª à 4ª série incompleta",
    2: "4ª série completa",
    3: "5ª à 8ª série incompleta",
    4: "Ensino Fundamental completo",
    5: "Ensino Médio incompleto",
    6: "Ensino Médio completo",
    7: "Ensino Superior incompleto",
    8: "Ensino Superior completo",
    9: "Ignorado",
    10: "Não se aplica"
}).fillna("Ignorado")

contagem_escolaridade = (
    escolaridade.value_counts()
    .reset_index()
)

contagem_escolaridade.columns = [
    "Escolaridade",
    "Casos"
]

grafico_escolaridade = px.bar(
    contagem_escolaridade,
    x="Escolaridade",
    y="Casos",
    text="Casos",
    title="Distribuição dos casos por escolaridade"
)

grafico_escolaridade.update_traces(
    textposition="outside"
)

grafico_escolaridade.update_layout(
    xaxis_title="Escolaridade",
    yaxis_title="Quantidade de casos",
    title_x=0.5
)

st.plotly_chart(
    grafico_escolaridade,
    use_container_width=True
)

st.dataframe(
    contagem_escolaridade,
    use_container_width=True,
    hide_index=True
)
# ==============================
# SITUAÇÃO DE GESTAÇÃO
# ==============================

st.subheader("🤰 Situação de gestação", divider="gray")

contagem_gestacao = df_filtrado["cs_gestant"].value_counts(dropna=False)

gestacao = df_filtrado["cs_gestant"].map({
    1: "1º trimestre",
    2: "2º trimestre",
    3: "3º trimestre",
    4: "Idade gestacional ignorada",
    5: "Não gestante",
    6: "Não se aplica",
    9: "Ignorado"
}).fillna("Ignorado")

contagem_gestacao = (
    gestacao.value_counts()
    .reindex(
        [
            "1º trimestre",
            "2º trimestre",
            "3º trimestre",
            "Idade gestacional ignorada",
            "Não gestante",
            "Não se aplica",
            "Ignorado"
        ],
        fill_value=0
    )
)

dados_gestacao = pd.DataFrame({
    "Situação": contagem_gestacao.index,
    "Casos": contagem_gestacao.values
})

grafico_gestacao = px.bar(
    dados_gestacao,
    x="Situação",
    y="Casos",
    text="Casos",
    title="Distribuição dos casos por situação de gestação"
)

grafico_gestacao.update_traces(
    textposition="outside"
)

grafico_gestacao.update_layout(
    xaxis_title="Situação de gestação",
    yaxis_title="Quantidade de casos",
    title_x=0.5
)

st.plotly_chart(
    grafico_gestacao,
    use_container_width=True
)
# ==============================
# ÓBITOS
# ==============================

st.subheader("🕊️ Óbitos", divider="gray")

obito = df_filtrado["dt_obito"].notna()

contagem_obito = pd.Series({
    "Com óbito": obito.sum(),
    "Sem óbito": (~obito).sum()
})

dados_obito = pd.DataFrame({
    "Situação": contagem_obito.index,
    "Casos": contagem_obito.values
})

grafico_obito = px.bar(
    dados_obito,
    x="Situação",
    y="Casos",
    text="Casos",
   title="Distribuição dos casos por preenchimento de óbito"
)

grafico_obito.update_traces(
    textposition="outside"
)

grafico_obito.update_layout(
    xaxis_title="Situação",
    yaxis_title="Quantidade de casos",
    title_x=0.5
)

st.plotly_chart(
    grafico_obito,
    use_container_width=True
)
# ==============================
# TEMPO ATÉ O ENCERRAMENTO
# ==============================

st.subheader("⏱️ Tempo até o encerramento", divider="gray")


def classificar_tempo(dias):
    if pd.isna(dias):
        return "Sem data de encerramento"
    elif dias <= 7:
        return "Até 7 dias"
    elif dias <= 30:
        return "8 a 30 dias"
    elif dias <= 60:
        return "31 a 60 dias"
    elif dias <= 90:
        return "61 a 90 dias"
    else:
        return "Mais de 90 dias"


df_filtrado["faixa_encerramento"] = df_filtrado["dias_ate_encerramento"].apply(
    classificar_tempo
)

ordem = [
    "Até 7 dias",
    "8 a 30 dias",
    "31 a 60 dias",
    "61 a 90 dias",
    "Mais de 90 dias",
    "Sem data de encerramento"
]

contagem_encerramento = (
    df_filtrado["faixa_encerramento"]
    .value_counts()
    .reindex(ordem, fill_value=0)
)

dados_encerramento = pd.DataFrame({
    "Faixa": contagem_encerramento.index,
    "Casos": contagem_encerramento.values
})

grafico_encerramento = px.bar(
    dados_encerramento,
    x="Faixa",
    y="Casos",
    text="Casos",
    title="Distribuição dos casos por tempo até o encerramento"
)

grafico_encerramento.update_traces(
    textposition="outside"
)

grafico_encerramento.update_layout(
    xaxis_title="Tempo até o encerramento",
    yaxis_title="Quantidade de casos",
    title_x=0.5
)

st.plotly_chart(
    grafico_encerramento,
    use_container_width=True
)
# ==============================
# QUALIDADE DOS DADOS
# ==============================

st.subheader("🔎 Qualidade dos dados", divider="gray")

total_registros = len(df_filtrado)

registros_atuais = total_registros

registros_sem_encerramento = df_filtrado["dt_encerra"].isna().sum()

registros_com_encerramento = df_filtrado["dt_encerra"].notna().sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Registros analisados",
        registros_atuais
    )

with col2:
    st.metric(
        "Com data de encerramento",
        registros_com_encerramento
    )

with col3:
    st.metric(
        "Sem data de encerramento",
        registros_sem_encerramento
    )


dados_qualidade = pd.DataFrame({
    "Situação": [
        "Com data de encerramento",
        "Sem data de encerramento"
    ],
    "Casos": [
        registros_com_encerramento,
        registros_sem_encerramento
    ]
})

grafico_qualidade = px.bar(
    dados_qualidade,
    x="Situação",
    y="Casos",
    text="Casos",
    title="Disponibilidade da data de encerramento"
)

grafico_qualidade.update_traces(
    textposition="outside"
)

grafico_qualidade.update_layout(
    xaxis_title="Situação",
    yaxis_title="Quantidade de casos",
    title_x=0.5
)

st.plotly_chart(
    grafico_qualidade,
    use_container_width=True
)
# ==============================
# RESUMO DO TRATAMENTO DOS DADOS
# ==============================

st.subheader("🧹 Resumo do tratamento dos dados", divider="gray")

registros_originais = 1000
registros_duplicados = 8
registros_finais = 992

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Registros recebidos",
        registros_originais
    )

with col2:
    st.metric(
        "Registros duplicados removidos",
        registros_duplicados
    )

with col3:
    st.metric(
        "Registros utilizados",
        registros_finais
    )

dados_tratamento = pd.DataFrame({
    "Etapa": [
        "Registros recebidos",
        "Duplicados removidos",
        "Registros utilizados"
    ],
    "Quantidade": [
        registros_originais,
        registros_duplicados,
        registros_finais
    ]
})

grafico_tratamento = px.bar(
    dados_tratamento,
    x="Etapa",
    y="Quantidade",
    text="Quantidade",
    title="Resumo do tratamento dos dados"
)

grafico_tratamento.update_traces(
    textposition="outside"
)

grafico_tratamento.update_layout(
    xaxis_title="Etapa",
    yaxis_title="Quantidade de registros",
    title_x=0.5
)

st.plotly_chart(
    grafico_tratamento,
    use_container_width=True
)
# ==============================
# DOWNLOAD DOS DADOS
# ==============================

st.subheader("📋 Dados tratados", divider="gray")

csv = df_filtrado.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Baixar dados tratados em CSV",
    data=csv,
    file_name="dengue_tratado.csv",
    mime="text/csv"
)
# ==============================
# SOBRE OS DADOS
# ==============================

st.subheader("ℹ️ Sobre os dados", divider="gray")

st.write(
    "Os dados utilizados neste dashboard foram obtidos por meio da "
    "API de Dados Abertos do Ministério da Saúde, referentes aos casos "
    "de dengue notificados no ano de 2024."
)

st.write(
    "Foram obtidos inicialmente 1.000 registros. Durante o tratamento "
    "dos dados, foram identificados e removidos 8 registros duplicados, "
    "resultando em 992 registros utilizados nas análises."
)

st.write(
    "As análises apresentadas incluem características dos casos, "
    "sintomas, classificação, evolução, hospitalização, comorbidades, "
    "origem dos casos, escolaridade, gestação, óbitos e tempo até o "
    "encerramento das notificações."
)

st.caption(
    "Fonte: API de Dados Abertos do Ministério da Saúde."
)