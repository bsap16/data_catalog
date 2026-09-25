# Bibliotecas
import sqlite3
import pandas as pd
import json
import os

# Análise de outliers
def detectar_outliers(serie):
    """
    Detectar outliers usando o método intervalo interquartil (IQR).
    Um valor é outlier se estiver abaixo de Q1 - 1.5*IQR
    ou acima de Q3 + 1.5*IQR.
    Retornará: quantidade de outliers encontrados
    """
    if serie.dtype not in ["float64", "int64"]:
        return 0
    Q1 = serie.quantile(0.25)
    Q3 = serie.quantile(0.75)
    IQR = Q3 - Q1
    outliers = ((serie < (Q1 - 1.5 * IQR)) | (serie > (Q3 + 1.5 * IQR))).sum()
    return int(outliers)

# Análise de valores discrepantes
def verificar_valores_discrepantes(df):
    """
    Verificar valores discrepantes conhecidos para o dataset bancário:
    - CreditScore fora do range 300-850
    - Age negativa ou acima de 100
    - Balance negativo
    - EstimatedSalary negativo
    Retornará: dicionário com colunas e quantidade de valores discrepantes
    """
    problemas = {}

    regras = {
        "CreditScore": lambda x: (x < 300) | (x > 850),
        "Age": lambda x: (x < 0) | (x > 100),
        "Balance": lambda x: x < 0,
        "EstimatedSalary": lambda x: x < 0
    }

    for coluna, regra in regras.items():
        if coluna in df.columns:
            qtd = int(regra(df[coluna]).sum())
            if qtd > 0:
                problemas[coluna] = qtd

    return problemas

# Análise das duplicatas
def verificar_duplicatas_id(df):
    """
    Verificar se há CustomerId duplicados no dataset.
    Em dados bancários reais, cada cliente deve ter um ID único.
    Retornará: quantidade de IDs duplicados
    """
    if "CustomerID" not in df.columns:
        return 0
    return int(df["CustomerID"].duplicated().sum())

# Score dos dados
def calcular_score(nulos, total, outliers, valores_discrepantes, duplicatas_id, unicos):
    """
    Calcular o score de qualidade de 0 a 100 com múltiplas dimensões:
    - Nulos: penaliza até 30 pontos
    - Outliers: penaliza até 20 pontos
    - Valores discrepantes: penaliza até 30 pontos
    - Duplicatas de ID: penaliza até 20 pontos
    Retornará: score final arredondado
    """
    score = 100

    # Penalidade por nulos (até 30 pontos)
    if nulos > 0:
        score -= (nulos / total) * 30

    # Penalidade por outliers (até 20 pontos)
    if outliers > 0:
        score -= (outliers / total) * 20

    # Penalidade por valores discrepantes (até 30 pontos)
    if valores_discrepantes > 0:
        score -= (valores_discrepantes / total) * 30

    # Penalidade por duplicatas de ID (até 20 pontos)
    if duplicatas_id > 0:
        score -= (duplicatas_id / total) * 20

    return round(max(score, 0), 1)

# Análise da qualidade do dados
def analisar_qualidade(db_path, tabela):
     """
    Analisar a qualidade completa da tabela do banco de dados.
    Combinar: nulos, outliers, valores discrepantes e duplicatas de ID.
    Retornará: dicionário com o relatório completo da tabela
    """
     conn = sqlite3.connect(db_path)
     df = pd.read_sql(f"SELECT * FROM {tabela}", conn)
     conn.close()

     # Verificações globais da tabela
     duplicatas_id = verificar_duplicatas_id(df)
     valores_discrepantes = verificar_valores_discrepantes(df)

     relatorio = {
         "tabela": tabela,
         "total_linhas": len(df),
         "total_colunas": len (df.columns),
         "duplicatas_id": duplicatas_id,
         "valores_discrepantes": valores_discrepantes,
         "colunas": []
     }

     for col in df.columns:
         total = len(df)
         nulos = int(df[col].isnull().sum())
         unicos = int(df[col].nunique())
         outliers = detectar_outliers(df[col])
         discrepantes = valores_discrepantes.get(col, 0)

         col_info = {
             "coluna": col,
             "tipo": str(df[col].dtype),
             "nulos": nulos,
             "percentual_nulos": round((nulos / total) * 100, 2),
             "valores_unicos": unicos,
             "duplicatas": int(total - unicos),
             "outliers": outliers,
             "percentual_outliers": round((outliers / total) * 100, 2),
             "valores_discrepantes": discrepantes
         }

         # Estatísticas numéricas
         if df[col].dtype in ["float64", "int64"]:
             col_info["min"] = float(df[col].min())
             col_info["max"] = float(df[col].max())
             col_info["media"] = round(float(df[col].mean()), 2)
             col_info["mediana"] = round(float(df[col].median()), 2)
             col_info["desvio_padrao"] = round(float(df[col].std()), 2)

        # Score enriquecido
         col_info["score_qualidade"] = calcular_score(
            nulos, total, outliers, discrepantes, duplicatas_id, unicos
        )

         relatorio["colunas"].append(col_info)

     return relatorio

# Análise do banco de dados
def analisar_banco_completo(db_path):
    """
    Percorre todas as tabelas do banco e gera o relatório de qualidade completo.
    Salva o resultado em output/qualidade.json
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = [t[0] for t in cursor.fetchall()]
    conn.close()

    relatorios = [analisar_qualidade(db_path, t) for t in tabelas]

    os.makedirs("output", exist_ok=True)
    with open("output/qualidade.json", "w", encoding="utf-8") as f:
        json.dump(relatorios, f, ensure_ascii=False, indent=2)

    print("Análise de qualidade salva em output/qualidade.json")
    return relatorios

if __name__ == "__main__":
    relatorios = analisar_banco_completo("data/banco_exemplo.db")

    for tabela in relatorios:
        print(f"\n Tabela: {tabela['tabela']}")
        print(f"  Linhas:{tabela['total_linhas']}")
        print(f"  Duplicatas de ID: {tabela['duplicatas_id']}")
        print(f"  Valores discrepantes: {tabela['valores_discrepantes']}")
        print(f"\n {'Coluna':<20} {'Score':>6} {'Nulos':>6} {'Outliers':>9} {'Discrepantes':>12}")
        print(f"  {'-'*57}")
        for col in tabela["colunas"]:
            print(f"  {col['coluna']:<20} {col['score_qualidade']:>6} {col['nulos']:>6} {col['outliers']:>9} {col['valores_discrepantes']:>12}")