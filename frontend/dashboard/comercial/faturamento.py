# frontend/dashboard/comercial/faturamento.py

import streamlit as st
import pandas as pd
import plotly.express as px
from backend.services.faturamento import carregar_dados_faturamento
import datetime

st.set_page_config(page_title="Dashboard de Faturamento", layout="wide")
st.title("📊 Dashboard de Faturamento")

# Datas padrão
hoje = datetime.date.today()
data_inicio_default = hoje - datetime.timedelta(days=30)
data_fim_default = hoje

# Sidebar: Filtros principais
st.sidebar.header("🎯 Filtros Principais")
data_inicio = st.sidebar.date_input("Data Início", value=data_inicio_default)
data_fim = st.sidebar.date_input("Data Fim", value=data_fim_default)

# Carregar dados
with st.spinner("🔄 Carregando dados..."):
    df = carregar_dados_faturamento(data_inicio, data_fim)

if df.empty:
    st.warning("Nenhum dado encontrado para o período selecionado.")
    st.stop()

# Filtros adicionais
filtros = {
    "CFOP": "CFOP",
    "Natureza da Operação": "NAT_OPERACAO",
    "Empresa": "NOME_FANTASIA",
    "Status Nota": "STTS_NOTA",
    "Fluxo de Venda": "COMPOE_FLUXO_VENDA"
}

for label, col in filtros.items():
    opcoes = df[col].dropna().unique().tolist()
    selecionados = st.sidebar.multiselect(f"Filtrar por {label}", sorted(opcoes), default=opcoes)
    df = df[df[col].isin(selecionados)]

# Agrupar por mês
df["DATA_EMISSAO"] = pd.to_datetime(df["DATA_EMISSAO"])
df["ANO_MES"] = df["DATA_EMISSAO"].dt.to_period("M").astype(str)

# Filtros dinâmicos (Ano e Representante)
anos_disponiveis = sorted(df["DATA_EMISSAO"].dt.year.unique())
anos_selecionados = st.multiselect("Filtrar Ano", anos_disponiveis, default=anos_disponiveis)
df = df[df["DATA_EMISSAO"].dt.year.isin(anos_selecionados)]

representantes = sorted(df["REPRESENTANTE"].dropna().unique())
reps_selecionados = st.multiselect("Filtrar Representante", representantes, default=representantes)
df = df[df["REPRESENTANTE"].isin(reps_selecionados)]

# Visuais principais
st.subheader("📈 Visualização Dinâmica")
tipo_grafico = st.selectbox("Tipo de gráfico", ["Linha", "Barras", "Colunas", "Pizza"])
valor = st.selectbox("Campo de valor", ["QTD", "VR_TOTAL", "Contagem Itens", "Contagem de Vendas"])
categoria = st.selectbox("Campo de categoria", [
    "REPRESENTANTE", "NOME_FANTASIA", "PRODUTO", "ESPECIE", "SUB_ESPECIE",
    "REGIAO", "CIDADE_CLI", "UF_CLI", "PAIS_CLI", "NAT_OPERACAO", "CFOP", "ANO_MES"
])

if valor == "Contagem Itens":
    df["VALOR"] = 1
elif valor == "Contagem de Vendas":
    df["VALOR"] = df["ID_NOTA_PROPRIA"].astype(str)
else:
    df["VALOR"] = df[valor]

if valor == "Contagem de Vendas":
    dados_plot = df.groupby(categoria)["VALOR"].nunique().reset_index()
else:
    dados_plot = df.groupby(categoria)["VALOR"].sum().reset_index()

# Plot
fig = None
if tipo_grafico == "Linha":
    fig = px.line(dados_plot, x=categoria, y="VALOR", markers=True)
elif tipo_grafico == "Barras":
    fig = px.bar(dados_plot, x=categoria, y="VALOR", orientation='h')
elif tipo_grafico == "Colunas":
    fig = px.bar(dados_plot, x=categoria, y="VALOR")
elif tipo_grafico == "Pizza":
    fig = px.pie(dados_plot, names=categoria, values="VALOR")

if fig:
    fig.update_layout(yaxis_tickformat=",.2f")
    st.plotly_chart(fig, use_container_width=True)

# Tabela resumo por mês
st.subheader("📆 Resumo Mensal")
resumo_mensal = df.groupby("ANO_MES").agg({
    "VR_TOTAL": "sum",
    "QTD": "sum",
    "ID_ITEM_NOTA_PROPRIA": "count"
}).rename(columns={
    "VR_TOTAL": "Total Faturado",
    "QTD": "Qtd Vendida",
    "ID_ITEM_NOTA_PROPRIA": "Itens Vendidos"
}).reset_index()

st.dataframe(resumo_mensal.style.format({
    "Total Faturado": "R$ {:,.2f}",
    "Qtd Vendida": "{:,.0f}",
    "Itens Vendidos": "{:,.0f}"
}))

# Gráfico linha de evolução mensal
st.subheader("📊 Evolução Mensal")
campo_evolucao = st.radio("Evolução baseada em", ["Total Faturado", "Qtd Vendida"], horizontal=True)
fig_evolucao = px.line(resumo_mensal, x="ANO_MES", y=campo_evolucao, markers=True)
fig_evolucao.update_traces(mode="lines+markers")
fig_evolucao.update_layout(yaxis_tickformat=",.2f")
st.plotly_chart(fig_evolucao, use_container_width=True)

# Tabela de dados com colunas selecionadas
st.subheader("📋 Tabela com Dados Filtrados")
colunas_selecionadas = st.multiselect("Escolha as colunas para exibir", df.columns.tolist(), default=["DATA_EMISSAO", "REPRESENTANTE", "PRODUTO", "VR_TOTAL"])
st.dataframe(df[colunas_selecionadas].style.format({
    col: "R$ {:,.2f}" if "VR" in col or "VALOR" in col else "{:,}" for col in colunas_selecionadas
}))

# Exportação
st.markdown("### 📁 Exportar Dados")
formato = st.radio("Formato", ["CSV", "Excel"], horizontal=True)

if formato == "CSV":
    st.download_button("⬇️ Baixar CSV", df[colunas_selecionadas].to_csv(index=False), file_name="faturamento.csv", mime="text/csv")
else:
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df[colunas_selecionadas].to_excel(writer, index=False, sheet_name="Faturamento")
    st.download_button("⬇️ Baixar Excel", output.getvalue(), file_name="faturamento.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
