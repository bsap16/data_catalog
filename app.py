import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly. graph_objects as go
import json
from streamlit_option_menu import option_menu

# ─────────────────────────────────────────
# Configuração geral
# ─────────────────────────────────────────

st.set_page_config(
    page_title="Data catalog dashboard",
    layout="wide"
)

# ─────────────────────────────────────────
# Idioma
# ─────────────────────────────────────────

idioma = st.sidebar.radio("Language / Idioma", ["Português", "English"])
pt = idioma == "Português"

# ─────────────────────────────────────────
# Textos bilíngues
# ─────────────────────────────────────────

textos = {
    "titulo": "Data catalog dashboard" if not pt else "Data catalog dashboard",
    "subtitulo": (
        "Automated data catalog for financial data"
        if not pt else
        "Catálogo de dados automatizado de dados financeiros"
    ),
    "paginas": (
        ["Overview", "Customer profile", "Financial behavior", "Churn risk"]
        if not pt else
        ["Visão geral", "Perfil dos clientes", "Comportamentos financeiros", "Risco de churn"]
    ),
    "total_clientes": "Total customers" if not pt else "Total de clientes",
    "paises": "Countries" if not pt else "Países",
    "taxa_churn": "Churn rate" if not pt else "Taxa de churn",
    "score_medio": "Avg. quality score" if not pt else "Score médio de qualidade",
    "sobre_dados": "About the data" if not pt else "Sobre os dados",
    "sobre_texto": (
        "This dataset contains 10.000 banking customers from France, Germany, and Spain. "
        "It was obtained from Kaggle's churn modelling dataset and it is used here to demonstrate "
        "automated data governance in a controlled environment."
        if not pt else
        "Este dataset contém 10.000 clientes bancários da França, Alemanha e Espanha. "
        "Ele foi obtido do dataset churn modelling do Kaggle e é utilizado aqui para demonstrar "
        "governança de dados automatizada em ambiente controlado."
    ),
    "qualidade_titulo": "Data quality" if not pt else "Qualidade dos dados",
    "qualidade_texto": (
        "Each column was evaluated across four dimensions: outliers "
        "and ID duplicates. Score ranges from 0 to 100."
        if not pt else
        "Cada coluna foi avaliada em quatro dimensões: outliers "
        "e duplicatas de ID. O score varia de 0 a 100."
    ),
    "col_score": "Quality score" if not pt else "Score de qualidade",
    "col_outliers": "Outliers" if not pt else "Outliers",
    "dist_pais": "Customers by country" if not pt else "Clientes por país",
    "dist_genero": "Customers by gender" if not pt else "Clientes por gênero",
    "dist_idade": "Age distribution" if not pt else "Distribuição por idade",
    "dist_produtos": "Products per customer" if not pt else "Produtos por clientes",
    "cartao": "Has credit card" if not pt else "Possui cartão de crédito",
    "ativo": "Active members" if not pt else "Membros ativos",
    "sim": "Yes" if not pt else "Sim",
    "nao": "No" if not pt else "Não",
    "dist_saldo": "Balance distribution" if not pt else "Distribuição de saldo",
    "dist_salario": "Estimated salary distribution" if not pt else "Distribuição de salário estimado",
    "credit_pais": "Credit score by country" if not pt else "Score de crédito por país",
    "tenure": "Years as customer" if not pt else "Anos como cliente",
    "churn_pais": "Churn rate by country" if not pt else "Taxa de churn por país",
    "churn_genero": "Churn rate by gender" if not pt else "Taxa de churn por gênero",
    "churn_idade": "Churn by age group" if not pt else "Taxa de churn por faixa etária",
    "churn_produtos": "Churn by number of products" if not pt else "Churn por número de produtos",
    "saiu": "Left" if not pt else "Saiu",
    "ficou": "Stayed" if not pt else "Ficou",
    "faixa": "Age group" if not pt else "Faixa etária",
    "aviso_qualidade": (
        "This dataset is educational and has no nulls or anomalous values. "
        "Outliers represent real extreme values present in the data."
        if not pt else
        "Este dataset é educacional e não possui nulos ou valores discrepantes. "
        "Outliers representam valores extremos reais presentes nos dados."
    )
}

# ─────────────────────────────────────────
# Carregamento dos dados
# ─────────────────────────────────────────

@st.cache_data
def carregar_dados():
    conn = sqlite3.connect("data/banco_exemplo.db")
    df = pd.read_sql("SELECT * FROM clientes", conn)
    conn.close()
    return df
@st.cache_data
def carregar_qualidade():
    with open("output/qualidade.json", encoding="utf-8") as f:
        return json.load(f)

df = carregar_dados()
qualidade = carregar_qualidade()
df_qual = pd.DataFrame(qualidade[0]["colunas"])

# ─────────────────────────────────────────
# Cabeçalho
# ─────────────────────────────────────────

st.title(textos["titulo"])
st.caption(textos["subtitulo"])
st.divider()

# ─────────────────────────────────────────
# Menu de navegação
# ─────────────────────────────────────────

pagina = option_menu(
    menu_title=None,
    options=textos["paginas"],
    icons=["house", "people", "cash-coin", "exclamation-triangle"],
    orientation="horizontal"
)

# ─────────────────────────────────────────
# Página 1 - Visão geral
# ─────────────────────────────────────────

p1 = textos["paginas"][0]
if pagina == p1:

    # Métricas
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(textos["total_clientes"], f"{len(df):,}")
    c2.metric(textos["paises"], df["Geography"].nunique())
    c3.metric(textos["taxa_churn"], f"{df['Exited'].mean()*100:.1f}%")
    c4.metric(textos["score_medio"], f"{df_qual['score_qualidade'].mean():.1f}/100")

    st.divider()

    # Sobre os dados
    st.subheader(textos["sobre_dados"])
    st.info(textos["sobre_texto"])

    st.divider()

    # Qualidade de dados
    st.subheader(textos["qualidade_titulo"])
    st.caption(textos["qualidade_texto"])
    st.warning(textos["aviso_qualidade"])

    fig_score = px.bar(
        df_qual,
        x="coluna",
        y="score_qualidade",
        color="score_qualidade",
        color_continuous_scale="RdYlGn",
        title=textos["col_score"],
        labels={"coluna": "", "score_qualidade": textos["col_score"]}
    )
    st.plotly_chart(fig_score, use_container_width='stretch')

    fig_out = px.bar(
        df_qual[df_qual["outliers"] > 0],
        x="coluna", y="outliers",
        title=textos["col_outliers"],
        labels={"coluna": "", "outliers": textos["col_outliers"]},
        color_discrete_sequence=["#FF6B6B"]
    )
    st.plotly_chart(fig_out, use_container_width='stretch')


# ─────────────────────────────────────────
# Página 2 - Perfil dos clientes
# ─────────────────────────────────────────

p2 = textos["paginas"][1]
if pagina == p2:

    col1, col2 = st.columns(2)

    with col1:
        fig_pais = px.pie(
            df, names="Geography",
            title=textos["dist_pais"],
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_pais, width="stretch")

    with col2:
        genero_map = {"Male": "Masculino", "Female": "Feminino"} if pt else {}
        df_gen = df.copy()
        df_gen["Gender"] = df_gen["Gender"].map(genero_map) if pt else df_gen["Gender"]
        fig_gen = px.pie(
            df_gen, names="Gender",
            title=textos["dist_genero"],
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_gen, width="stretch")

    fig_idade = px.histogram(
        df, x="Age", nbins=20,
        title=textos["dist_idade"],
        labels={"Age": "Idade" if pt else "Age", "count": "Quantidade" if pt else "Count"},
        color_discrete_sequence=["#353EC0"]
    )
    st.plotly_chart(fig_idade, width="stretch")

    col3, col4 = st.columns(2)

    with col3:
        cartao = df["HasCrCard"].map({1: textos["sim"], 0: textos["nao"]}).value_counts().reset_index()
        cartao.columns = [textos["cartao"], "count"]
        fig_cartao = px.pie(
            cartao, names=textos["cartao"], values="count",
            title=textos["cartao"],
            color_discrete_sequence=["#00CC96", "#EF553B"]
        )
        st.plotly_chart(fig_cartao, width="stretch")

    with col4:
        ativo = df["IsActiveMember"].map({1: textos["sim"], 0: textos["nao"]}).value_counts().reset_index()
        ativo.columns = [textos["ativo"], "count"]
        fig_ativo = px.pie(
            ativo, names=textos["ativo"], values="count",
            title=textos["ativo"],
            color_discrete_sequence=["#00CC96", "#EF553B"]
        )
        st.plotly_chart(fig_ativo, width="stretch")

# ─────────────────────────────────────────
# Página 3 - Comportamento financeiro
# ─────────────────────────────────────────

p3 = textos["paginas"][2]
if pagina == p3:

    fig_saldo = px.histogram(
        df, x="Balance", nbins=30,
        title=textos["dist_saldo"],
        labels={"Balance": "Saldo" if pt else "Balance", "count": "Quantidade" if pt else "Count"},
        color_discrete_sequence=["#2B808F"]
    )
    st.plotly_chart(fig_saldo, width="stretch")

    fig_salario = px.histogram(
        df, x="EstimatedSalary", nbins=30,
        title=textos["dist_salario"],
        labels={"EstimatedSalary": "Salário estimado" if pt else "Estimated salary",
                "count": "Quantidade" if pt else "Count"},
        color_discrete_sequence=["#AB63FA"]
    )
    st.plotly_chart(fig_salario, width="stretch")

    col1, col2 = st.columns(2)

    with col1:
        fig_credit = px.box(
            df, x="Geography", y="CreditScore",
            title=textos["credit_pais"],
            labels={"Geography": "País" if pt else "Country",
                    "CreditScore": "Score de crédito" if pt else "Credit score"},
            color="Geography",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_credit, width="stretch")

    with col2:
        fig_tenure = px.histogram(
            df, x="Tenure",
            title=textos["tenure"],
            labels={"Tenure": "Anos" if pt else "Years",
                    "count": "Quantidade" if pt else "Count"},
            color_discrete_sequence=["#FFA15A"]
        )
        st.plotly_chart(fig_tenure, width="stretch")

# ─────────────────────────────────────────
# Página 4 — Risco de churn
# ─────────────────────────────────────────

p4 = textos["paginas"][3]
if pagina == p4:

    # Taxa geral
    churn_rate = df["Exited"].mean() * 100
    st.metric(
        textos["taxa_churn"],
        f"{churn_rate:.1f}%",
        delta=f"{churn_rate - 50:.1f}% vs 50%" if churn_rate > 50 else None
    )
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        churn_pais = df.groupby("Geography")["Exited"].mean().reset_index()
        churn_pais["Exited"] = (churn_pais["Exited"] * 100).round(1)
        fig_cp = px.bar(
            churn_pais, x="Geography", y="Exited",
            title=textos["churn_pais"],
            labels={"Geography": "País" if pt else "Country",
                    "Exited": "Churn (%)" },
            color="Geography",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_cp, width="stretch")

    with col2:
        churn_gen = df.groupby("Gender")["Exited"].mean().reset_index()
        churn_gen["Exited"] = (churn_gen["Exited"] * 100).round(1)
        if pt:
            churn_gen["Gender"] = churn_gen["Gender"].map(
                {"Male": "Masculino", "Female": "Feminino"}
            )

        fig_cg = px.bar(
            churn_gen, x="Gender", y="Exited",
            title=textos["churn_genero"],
            labels={"Gender": "Gênero" if pt else "Gender", "Exited": "Churn (%)"},
            color="Gender",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_cg, width="stretch")

    # Churn por faixa etária
    df_idade = df.copy()
    df_idade["FaixaEtaria"] = pd.cut(
        df_idade["Age"],
        bins=[0, 25, 35, 45, 55, 100],
        labels=["< 25", "25-35", "35-45", "45-55", "> 55"]
    )
    churn_idade = df_idade.groupby("FaixaEtaria", observed='s')["Exited"].mean().reset_index()
    churn_idade["Exited"] = (churn_idade["Exited"] * 100).round(1)
    fig_ci = px.bar(
        churn_idade, x="FaixaEtaria", y="Exited",
        title=textos["churn_idade"],
        labels={"FaixaEtaria": textos["faixa"], "Exited": "Churn (%)"},
        color="Exited",
        color_continuous_scale="RdYlGn_r"
    )
    st.plotly_chart(fig_ci, width="stretch")

    # Churn por número de produtos
    churn_prod = df.groupby("NumOfProducts")["Exited"].mean().reset_index()
    churn_prod["Exited"] = (churn_prod["Exited"] * 100).round(1)
    fig_cprod = px.bar(
        churn_prod, x="NumOfProducts", y="Exited",
        title=textos["churn_produtos"],
        labels={"NumOfProducts": "Nº de produtos" if pt else "No. of Products",
                "Exited": "Churn (%)"},
        color="Exited",
        color_continuous_scale="RdYlGn_r"
    )
    st.plotly_chart(fig_cprod, width="stretch")


