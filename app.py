"""
Projeto: Enterprise Sales & Business Intelligence Analytics
Autor: Thayrone Constâncio
Descrição: Sistema analítico corporativo com SQLite, Consultas SQL Avançadas, 
           Curva ABC de Produtos e Dashboard Executivo em Streamlit.
"""

import sqlite3
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILO VISUAL
# ==========================================
st.set_page_config(
    page_title="Enterprise BI & Sales Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .stMetric { 
            background-color: rgba(128, 128, 128, 0.1); 
            padding: 15px; 
            border-radius: 10px; 
            border: 1px solid rgba(128, 128, 128, 0.2);
        }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. BANCO DE DADOS & PIPELINE ETL (SQLITE)
# ==========================================


@st.cache_resource
def init_database():
  """Inicializa o banco de dados relacional e popula com dados corporativos simulados"""
  conn = sqlite3.connect("enterprise_data.db", check_same_thread=False)
  cursor = conn.cursor()

  # Criação das Tabelas Relacionais
  cursor.execute(
      """
        CREATE TABLE IF NOT EXISTS categorias (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_categoria TEXT NOT NULL
        )
    """
  )

  cursor.execute(
      """
        CREATE TABLE IF NOT EXISTS produtos (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_produto TEXT NOT NULL,
            id_categoria INTEGER,
            preco_custo REAL,
            preco_venda REAL,
            FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
        )
    """
  )

  cursor.execute(
      """
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_cliente TEXT NOT NULL,
            segmento TEXT,
            estado TEXT
        )
    """
  )

  cursor.execute(
      """
        CREATE TABLE IF NOT EXISTS vendas (
            id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
            data_venda TEXT,
            id_cliente INTEGER,
            id_produto INTEGER,
            quantidade INTEGER,
            desconto REAL,
            regiao TEXT,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
            FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
        )
    """
  )

  # Verifica se o banco já possui dados
  cursor.execute("SELECT COUNT(*) FROM vendas")
  count = cursor.fetchone()[0]

  if count == 0:
    # Populando Categorias
    categorias = [
        ("Tecnologia & Hardware",),
        ("Insumos Logísticos",),
        ("Móveis Corporativos",),
        ("Automação Comercial",),
    ]
    cursor.executemany(
        "INSERT INTO categorias (nome_categoria) VALUES (?)", categorias
    )

    # Populando Produtos
    produtos = [
        ("Notebook Corporativo i7", 1, 3200.0, 4800.0),
        ("Leitor de Código de Barras Laser", 4, 180.0, 350.0),
        ("Bobina Térmica Caixa (Cx c/ 20)", 2, 90.0, 150.0),
        ("Cadeira Ergonômica Escritório", 3, 450.0, 850.0),
        ("Coletor de Dados de Inventário", 1, 1500.0, 2400.0),
        ("Paleteira Manual Hidráulica 2T", 2, 1100.0, 1750.0),
        ("Mesa Executiva em L", 3, 700.0, 1200.0),
        ("Impressora de Etiquetas Térmica", 4, 600.0, 1050.0),
    ]
    cursor.executemany(
        """
            INSERT INTO produtos (nome_produto, id_categoria, preco_custo, preco_venda) 
            VALUES (?, ?, ?, ?)
        """,
        produtos,
    )

    # Populando Clientes
    clientes = [
        ("Supermercados Estrela S/A", "Varejo", "RJ"),
        ("Atacadista Boa Praça Ltda", "Atacado", "SP"),
        ("Logística Integrada Sudeste", "Logística", "MG"),
        ("Comercial Horizonte", "Varejo", "RJ"),
        ("Distribuidora Alpha", "Atacado", "ES"),
        ("Tech Solutions Corp", "Serviços", "SP"),
    ]
    cursor.executemany(
        """
            INSERT INTO clientes (nome_cliente, segmento, estado) 
            VALUES (?, ?, ?)
        """,
        clientes,
    )

    # Gerando massa de dados transacionais simulados (últimos 12 meses)
    np.random.seed(42)
    start_date = datetime.now() - timedelta(days=365)
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste"]
    segmentos_venda = []

    for _ in range(3500):
      dias_aleatorios = np.random.randint(0, 365)
      data_v = (start_date + timedelta(days=dias_aleatorios)).strftime(
          "%Y-%m-%d"
      )
      id_cli = np.random.randint(1, 7)
      id_prod = np.random.randint(1, 9)
      qtd = np.random.randint(1, 15)
      desc = np.random.choice([0.0, 0.05, 0.10, 0.15], p=[0.6, 0.2, 0.15, 0.05])
      regiao = np.random.choice(regioes)
      segmentos_venda.append((data_v, id_cli, id_prod, qtd, desc, regiao))

    cursor.executemany(
        """
            INSERT INTO vendas (data_venda, id_cliente, id_produto, quantidade, desconto, regiao) 
            VALUES (?, ?, ?, ?, ?, ?)
        """,
        segmentos_venda,
    )
    conn.commit()

  return conn


conn = init_database()

# ==========================================
# 3. CAMADA DE CONSULTAS SQL AVANÇADAS
# ==========================================


@st.cache_data
def load_analytical_data():
  """Executa joins complexos e agregações via SQL direto no SQLite"""
  query = """
        SELECT 
            v.id_venda,
            v.data_venda,
            strftime('%Y-%m', v.data_venda) as ano_mes,
            c.nome_cliente,
            c.segmento,
            p.nome_produto,
            cat.nome_categoria,
            v.quantidade,
            v.desconto,
            v.regiao,
            p.preco_custo,
            p.preco_venda,
            (v.quantidade * p.preco_venda * (1 - v.desconto)) as faturamento_total,
            (v.quantidade * p.preco_custo) as custo_total,
            ((v.quantidade * p.preco_venda * (1 - v.desconto)) - (v.quantidade * p.preco_custo)) as lucro_total
        FROM vendas v
        JOIN clientes c ON v.id_cliente = c.id_cliente
        JOIN produtos p ON v.id_produto = p.id_produto
        JOIN categorias cat ON p.id_categoria = cat.id_categoria
    """
  return pd.read_sql(query, conn)


df = load_analytical_data()
df["data_venda"] = pd.to_datetime(df["data_venda"])

# ==========================================
# 4. BARRA LATERAL (FILTROS EXECUTIVOS)
# ==========================================
st.sidebar.title("🎛️ Filtros Executivos")
st.sidebar.markdown("---")

# Filtro de Período
min_date = df["data_venda"].min().date()
max_date = df["data_venda"].max().date()
date_range = st.sidebar.date_input(
    "Período de Análise", value=(min_date, max_date), min_value=min_date, max_value=max_date
)

# Filtro de Região
regioes_disponiveis = ["Todas"] + list(df["regiao"].unique())
regiao_selecionada = st.sidebar.selectbox("Região Comercial", regioes_disponiveis)

# Filtro de Categoria
categorias_disponiveis = ["Todas"] + list(df["nome_categoria"].unique())
categoria_selecionada = st.sidebar.selectbox(
    "Categoria de Produto", categorias_disponiveis
)

# Aplicando Filtros no DataFrame
df_filtered = df.copy()
if len(date_range) == 2:
  start_dt, end_dt = date_range
  df_filtered = df_filtered[
      (df_filtered["data_venda"].dt.date >= start_dt)
      & (df_filtered["data_venda"].dt.date <= end_dt)
  ]

if regiao_selecionada != "Todas":
  df_filtered = df_filtered[df_filtered["regiao"] == regiao_selecionada]

if categoria_selecionada != "Todas":
  df_filtered = df_filtered[df_filtered["nome_categoria"] == categoria_selecionada]

# ==========================================
# 5. CABEÇALHO E KPIS PRINCIPAIS
# ==========================================
st.title("📈 Enterprise Sales & Business Intelligence")
st.markdown(
    "Painel executivo avançado para acompanhamento de faturamento, rentabilidade,"
    " margens operacionais e Curva ABC de produtos integrado com banco"
    " relacional SQLite."
)
st.markdown("---")

# Cálculo de KPIs
total_faturamento = df_filtered["faturamento_total"].sum()
total_lucro = df_filtered["lucro_total"].sum()
margem_lucro_media = (
    (total_lucro / total_faturamento * 100) if total_faturamento > 0 else 0
)
ticket_medio = (
    total_faturamento / df_filtered["id_venda"].nunique()
    if df_filtered["id_venda"].nunique() > 0
    else 0
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Faturamento Total", f"R$ {total_faturamento:,.2f}")
col2.metric("📦 Lucro Operacional", f"R$ {total_lucro:,.2f}")
col3.metric("📊 Margem de Lucro", f"{margem_lucro_media:.2f}%")
col4.metric("🏷️ Ticket Médio por Venda", f"R$ {ticket_medio:,.2f}")

st.markdown("---")

# ==========================================
# 6. ABAS DE NAVEGAÇÃO ANALÍTICA
# ==========================================
tab1, tab2, tab3 = st.tabs(
    [
        "📊 Visão Geral & Desempenho",
        "📦 Curva ABC de Produtos",
        "🛠️ Explorador SQL & Dados",
    ]
)

with tab1:
  st.subheader("Evolução Temporal do Faturamento e Lucratividade")

  # Agregação mensal
  df_mensal = (
      df_filtered.groupby("ano_mes")
      .agg({"faturamento_total": "sum", "lucro_total": "sum"})
      .reset_index()
  )

  st.line_chart(
      df_mensal.set_index("ano_mes")[["faturamento_total", "lucro_total"]]
  )

  col_a, col_b = st.columns(2)

  with col_a:
    st.subheader("Desempenho por Categoria")
    df_cat = (
        df_filtered.groupby("nome_categoria")["faturamento_total"]
        .sum()
        .reset_index()
    )
    st.bar_chart(df_cat.set_index("nome_categoria"))

  with col_b:
    st.subheader("Faturamento por Região")
    df_reg = (
        df_filtered.groupby("regiao")["faturamento_total"].sum().reset_index()
    )
    st.bar_chart(df_reg.set_index("regiao"))

with tab2:
  st.subheader("📊 Análise de Curva ABC (Pareto 80/20)")
  st.markdown(
      "Identificação dos produtos que geram a maior fatia da receita da empresa."
  )

  # Lógica de Curva ABC
  df_abc = (
      df_filtered.groupby("nome_produto")["faturamento_total"]
      .sum()
      .reset_index()
  )
  df_abc = df_abc.sort_values(by="faturamento_total", ascending=False)
  df_abc["Participação (%)"] = (
      df_abc["faturamento_total"] / df_abc["faturamento_total"].sum()
  ) * 100
  df_abc["Participação Acumulada (%)"] = df_abc["Participação (%)"].cumsum()

  def classificar_abc(acumulado):
    if acumulado <= 80:
      return "Classe A (Foco Principal)"
    elif acumulado <= 95:
      return "Classe B (Intermediário)"
    else:
      return "Classe C (Cauda Longa)"

  df_abc["Classificação ABC"] = df_abc["Participação Acumulada (%)"].apply(
      classificar_abc
  )

  st.dataframe(
      df_abc.style.format({
          "faturamento_total": "R$ {:,.2f}",
          "Participação (%)": "{:.2f}%",
          "Participação Acumulada (%)": "{:.2f}%",
      }),
      use_container_width=True,
  )

with tab3:
  st.subheader("🛠️ Auditoria de Banco de Dados & Consultas SQL")
  st.markdown(
      "Visualize diretamente as tabelas do banco relacional SQLite subjacente."
  )

  tabela_escolhida = st.selectbox(
      "Selecione a tabela para inspecionar:",
      ["vendas", "produtos", "clientes", "categorias"],
  )

  cursor = conn.cursor()
  cursor.execute(f"SELECT * FROM {tabela_escolhida} LIMIT 50")
  dados_tabela = cursor.fetchall()
  colunas = [description[0] for description in cursor.description]

  df_tabela = pd.DataFrame(dados_tabela, columns=colunas)
  st.dataframe(df_tabela, use_container_width=True)

  st.info(
      "💡 Este projeto utiliza arquitetura relacional robusta com SQLite, garantindo"
      " integridade referencial e alta performance em consultas analíticas."
  )