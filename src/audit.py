import sqlite3
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import random

# ─────────────────────────────────────────
# Dados de simulação
# ─────────────────────────────────────────

USUARIOS = [
    {"id": "BRB001", "nome": "Maria José", "perfil": "Analista de dados"},
    {"id": "BRB002", "nome": "José Silva", "perfil": "Engenheiro de dados"},
    {"id": "BRB003", "nome": "Joana Oliva", "perfil": "Cientista de dados"},
    {"id": "BRB004", "nome": "Carmen Marina", "perfil": "Gestor de governança"},
    {"id": "BRB005", "nome": "Ricardo Santos", "perfil": "Auditor de compliance"},
]

OPERACOES = ["SELECT", "SELECT", "SELECT", "UPDATE", "DELETE", "INSERT"]
TABELAS = ["clientes", "clientes", "clientes", "contas", "transacoes"]
COLUNAS_SENSIVEIS = ["Surname", "CustomerId", "EstimatedSalary", "Balance"]

def gerar_logs(n=50):
    """
    Gera n registros simulados de acesso ao banco de dados.
    Simula acessos dos últimos 30 dias com horários variados.
    Retorna: lista de dicionários com os logs gerados.
    """

    logs = []
    agora = datetime.now()

    for i in range (n):
        usuario = random.choice(USUARIOS)
        operacao = random.choice(OPERACOES)
        tabela = random.choice(TABELAS)
        coluna = random.choice(COLUNAS_SENSIVEIS + [None, None])
        delta = timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        timestamp = (agora - delta).strftime("%d-%m-%Y %H:%M:%S")

        #Classifica o risco de operação
        if operacao in ["DELETE", "UPDATE"] and coluna in COLUNAS_SENSIVEIS:
            risco = "Alto"
        elif operacao in ["DELETE", "UPDATE"]:
            risco = "Médio"
        elif coluna in COLUNAS_SENSIVEIS:
            risco = "Médio"
        else:
            risco = "Baixo"

        logs.append({
            "id_log": i + 1,
            "timestamp": timestamp,
            "usuario_id": usuario["id"],
            "usuario_nome": usuario["nome"],
            "perfil": usuario["perfil"],
            "operacao": operacao,
            "tabela": tabela,
            "coluna_acessada": coluna if coluna else "N/A",
            "dado_sensivel": coluna in COLUNAS_SENSIVEIS,
            "nivel_risco": risco
        })

    return sorted(logs, key=lambda x: x["timestamp"], reverse=True)

def salvar_logs(logs, db_path):
    """
    Salvar os logs gerados em uma tabela SQLite chamada 'audit_logs'.
    Parâmetro: logs → lista de dicionários com os registros.
    Paramêtro: db_path → caminho do banco de dados.
    """
    conn = sqlite3.connect(db_path)
    df_logs = pd.DataFrame(logs)
    df_logs.to_sql("audit_logs", conn, if_exists="replace", index=False)
    conn.close()
    print(f"{len(logs)} logs salvos na tabela audit_logs")

def gerar_relatorio(logs):
    """
    Gerar um relatório resumido dos logs de auditoria com:
    - Total de acessos por usuário;
    - Total de acessos por operações;
    - Acesso a dados sensíveis;
    - Eventos de alto risco;
    Salvar em output/auditoria.json
    """
    df = pd.DataFrame(logs)

    relatorio = {
        "gerado_em": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "total_acessos": len(df),
        "acessos_por_usuario": (
            df.groupby(["usuario_id", "usuario_nome", "perfil"])
            .size()
            .reset_index(name="total")
            .to_dict(orient="records")
        ),
        "acessos_por_operacao": (
            df.groupby("operacao")
            .size()
            .reset_index(name="total")
            .to_dict(orient="records")
        ),
        "acessos_sensiveis": int(df["dado_sensivel"].sum()),
        "percentual_sensivel": round(df["dado_sensivel"].mean() * 100, 1),
        "eventos_alto_risco": (
            df[df["nivel_risco"] == "Alto"]
            [[ "timestamp", "usuario_nome",
            "operacao", "tabela",
            "coluna_acessada"]]
            .to_dict(orient="records")
        ),
        "distribuicao_risco": (
            df.groupby("nivel_risco")
            .size()
            .reset_index(name="total")
            .to_dict(orient="records")
        )
    }

    os.makedirs("output", exist_ok=True)
    with open("output/auditoria.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)

    print("Relatório salvo em output/auditoria.json")
    return relatorio

def imprimir_resumo(relatorio):
    """
    Imprimir um resumo do relatório no terminal.
    """
    print(f"\n RELATÓRIO DE AUDITORIA")
    print(f"Gerado em: {relatorio['gerado_em']}")
    print(f"Total de acessos: {relatorio['total_acessos']}")
    print(f"Acessos a dados sensíveis: {relatorio['acessos_sensiveis']} ({relatorio['percentual_sensivel']}%)")
    print(f"\n Acessos por operação:")
    for op in relatorio["acessos_por_operacao"]:
        print(f" → {op['operacao']}: {op['total']}")
    print(f"\n Eventos de alto risco: {len(relatorio['eventos_alto_risco'])}")
    for ev in relatorio["eventos_alto_risco"][:3]:
        print(f"{ev['timestamp']} | {ev['usuario_nome']} | {ev['operacao']} | {ev['coluna_acessada']}")

if __name__ == "__main__":
    logs = gerar_logs(50)
    salvar_logs(logs, "data/banco_exemplo.db")
    relatorio = gerar_relatorio(logs)
    imprimir_resumo(relatorio)