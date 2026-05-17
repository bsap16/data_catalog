#Libraries
import pandas as pd
import sqlite3
import json
import os

#Visualization
def carregar_csv(caminho):
    df = pd.read_csv(caminho)
    print(f"✓ Dataset carregado: {df.shape[0]} linhas e {df.shape[1]} colunas")
    print(f"\nColunas encontradas: \n{list(df.columns)}") 
    print(f"\nPrimeiras linhas:")
    print(df.head())
    return df

#Verificar as pastas
def salvar_no_banco(df, db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    df.to_sql("clientes", conn, if_exists="replace", index=False)
    conn.close()
    print(f"\n✓ Dados salvos no banco: {db_path}")

#Listar tabelas
def listar_tabelas(conn):
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    return pd.read_sql(query, conn)["name"].tolist()

#Extrair metadados
def extrair_metadados_tabela(conn, tabela):
    cursor = conn.cursor()

    #Informações das colunas
    cursor.execute(f"PRAGMA table_info({tabela})")
    colunas = cursor.fetchall()

    #Chaves estrangeiras
    cursor.execute(f"PRAGMA foreign_key_list({tabela})")
    fks = cursor.fetchall()

    #Total de registros
    cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
    total = cursor.fetchone()[0]

    metadados = {
        "tabela": tabela,
        "total_registros": total,
        "colunas": [],
        "chaves_estrangeiras": [
            {"coluna": fk[3], "referencia": f"{fk[2]}.{fk[4]}"} for fk in fks
        ]
    }

    for col in colunas:
        metadados["colunas"].append({
            "id": col[0],
            "nome": col[1],
            "tipo": col[2],
            "nao_nulo": bool(col[3]),
            "valor_padrao": col[4],
            "chave_primaria": bool(col[5])
        })
    return metadados

def extrair_catalogo_completo(db_path):
    conn = sqlite3.connect(db_path)
    tabelas = listar_tabelas(conn)
    catalogo = []
    
    for tabela in tabelas:
        meta = extrair_metadados_tabela(conn, tabela)
        catalogo.append(meta)
        print(f"✓ Tabela '{tabela}' catalogada.")
    
    conn.close()
    return catalogo

#Salvar no gitHub
if __name__ == "__main__":
    #Carregar CSV e salva no banco
    df = carregar_csv("data/Churn_Modelling.csv")
    salvar_no_banco(df, "data/banco_exemplo.db")

    #Extrai metadados do banco
    catalogo = extrair_catalogo_completo("data/banco_exemplo.db")

    # Salva o catálogo em JSON
    os.makedirs("output", exist_ok=True)
    with open("output/catalogo.json", "w", encoding="utf-8") as f:
        json.dump(catalogo, f, ensure_ascii=False, indent=2)
    
    print("\n✓ Catálogo salvo em output/catalogo.json")