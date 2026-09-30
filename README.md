# 📊 Vendas Corporativas e Análise de Business Intelligence

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)](https://www.sqlite.org/)
[![Pandas](https://img.shields.io/badge/Data_Analysis-Pandas-orange.svg)](https://pandas.pydata.org/)

Sistema analítico corporativo de ponta a ponta (Full-Stack Data Science), desenvolvido para unificar **Engenharia de Dados Relacional (SQLite/SQL)**, **Pipeline de ETL em Python**, **Modelagem Financeira e Curva ABC** com deploy de um **Dashboard Executivo Interativo em Streamlit**.

---

## 🎯 Sobre o Projeto

Em um cenário corporativo orientado a dados, empresas precisam ir além de planilhas estáticas. Este projeto simula um ambiente de Business Intelligence empresarial para monitoramento de faturamento, margens operacionais, rentabilidade de produtos e eficiência de vendas por região, fornecendo insights estratégicos para a tomada de decisão executiva.

---

## 🛠 Arquitetura e Tecnologias Utilizadas

* **Linguagem:** Python
* **Banco de Dados & ETL:** SQLite, Pandas, NumPy, Consultas SQL Nativas
* **Engenharia de Negócios:** Cálculo de Margem de Lucro, Ticket Médio e Análise de Curva ABC (Princípio de Pareto 80/20)
* **Interface & Visualização:** Streamlit (Layout responsivo com filtros executivos dinâmicos e abas analíticas)

---

## 📈 Principais Funcionalidades

1. **Banco de Dados Relacional Normalizado (SQLite):** Arquitetura estruturada com tabelas relacionais (`clientes`, `produtos`, `categorias`, `vendas`) garantindo integridade referencial e simulação de massa de dados transacionais.
2. **Consultas SQL Analíticas Avançadas:** Joins complexos, agregações por períodos e cruzamentos de custos e receitas direto no banco de dados.
3. **Curva ABC Automatizada:** Algoritmo de classificação de produtos por relevância de faturamento (Classe A, B e C) para otimização de estoque e campanhas.
4. **Painel Executivo Dinâmico:** Filtros customizáveis por período de análise, região comercial e categoria de produtos com atualização em tempo real de KPIs de lucratividade.

---

## ⚙️ Como Executar o Projeto Localmente

Para rodar este projeto em sua máquina, siga os passos abaixo:

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/ThayroneConstancio/enterprise-sales-intelligence.git](https://github.com/ThayroneConstancio/enterprise-sales-intelligence.git)

1.Entre na pasta do projeto:
cd enterprise-sales-intelligence

2.Instale as dependências necessárias:
pip install streamlit pandas numpy

3.Execute a aplicação Streamlit:
streamlit run app.py

💡 Insights e Aplicação Comercial
Gestão de Margem: Permite identificar rapidamente quais categorias e regiões entregam maior margem de lucro operacional.

Foco no Core Business (Curva ABC): Direciona esforços comerciais para os produtos essenciais que compõem a faixa de maior receita da empresa.

Desenvolvido por Thayrone Constâncio — Estudante de Ciência de Dados e Inteligência Artificial.
