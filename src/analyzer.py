# Bibliotecas
import sqlite3
import pandas as pd
import json
import os

# Análise da qualidade dos dados
def analisar_qualidade(db_path, tabela):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(f"SELECT * FROM {tabela}", conn)
    conn.close()

    relatorio = {
        "tabela": tabela,
        "total_linhas": len(df),
        "total_colunas": len(df.columns),
        "colunas": []
    }

    for col in df.columns:
        total = len(df)
        nulos = df[col].isnull().sum()
        unicos = df[col].nunique()
        duplicatas = total - unicos

        col_info = {
            "coluna": col,
            "tipo": str(df[col].dtype),
            "nulos": int(nulos),
            "percentual_nulos": round((nulos / total) * 100, 2),
            "valores_unicos": int(unicos),
            "duplicatas": int(duplicatas)
    }

        # Estatíticas numéricas
        if df[col].dtype in ["float64", "int64"]:
            col_info["min"] = float(df[col].min())
            col_info["max"] = float(df[col].max())
            col_info["media"] = round(float(df[col].mean()), 2)

        # Score de qualidade (0 a 100)
        score = 100
        if nulos > 0:
            score -= (nulos / total) * 50
        col_info["score_qualidade"] = round(score, 1)

        relatorio["colunas"].append(col_info)
    
    return relatorio

# Análise do dados do banco
def analisar_banco_completo(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = [t[0] for t in cursor.fetchall()]
    conn.close()
    
    relatorios = [analisar_qualidade(db_path, t) for t in tabelas]

    os.makedirs("output", exist_ok=True)
    with open("output/qualidade.json", "w", encoding="utf-8") as f:
        json.dump(relatorios, f, ensure_ascii=False, indent=2)

    print("✓ Análise de qualidade salva em output/qualidade.json")
    return relatorios

if __name__ == "__main__":
    relatorios = analisar_banco_completo("data/banco_exemplo.db")

    # Mostrar resumo no terminal
    for tabela in relatorios:
        print(f"\n📊 Tabela: {tabela['tabela']}")
        print(f"   Linhas: {tabela['total_linhas']}")
        print(f"   Colunas: {tabela['total_colunas']}")
        for col in tabela["colunas"]:
            print(f"   → {col['coluna']}: score {col['score_qualidade']} | nulos: {col['nulos']}")