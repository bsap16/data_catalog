#Libraries
import pandas as pd
import sqlite3
import os

#Visualization
def carregar_csv(caminho):
    df = pd.read_csv(caminho)
    print(f"Dataset carregado: {df.shape[0]} linhas e {df.shape[1]} colunas")
    print(f"\nColunas encontradas: \n{list(df.columns)}") 
    print(f"\nPrimeiras linhas:")
    print(df.head())
    return df

#Salvar alterações
def salvar_no_banco(df, db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    df.to_sql("clientes", conn, if_exists="replace", index=False)
    conn.close()
    print(f"\n✓ Dados salvos no banco: {db_path}")

#Salvar no gitHub
if __name__ == "__main__":
    df = carregar_csv("data/Churn_Modelling.csv")
    salvar_no_banco(df, "data/banco_exemplo.db")