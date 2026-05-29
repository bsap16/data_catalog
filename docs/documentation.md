# 📋 Documentação Técnica | Technical Documentation

---

## 🇧🇷 Português

### Sobre este arquivo

Este arquivo registra de forma completa e cronológica todo o desenvolvimento do projeto: decisões técnicas, scripts criados, ferramentas escolhidas, análises realizadas, limitações encontradas e próximos passos.

A atualização será realizada ao final de cada dia de desenvolvimento do projeto.

---

### Contexto do projeto

#### Problema
Instituições financeiras lidam com volumes crescentes de dados de clientes e, algumas vezes, sem processos estruturados de governança para saber quais dados existem, qual a qualidade deles, quais são sensíveis pela LGPD e quem os acessa.

#### Solução proposta
Um catálogo de dados automatizado que:
- Documentar automaticamente a estrutura de qualquer banco de dados
- Monitorar a qualidade dos dados com scoring por coluna
- Classificar a sensibilidade dos dados com base na LGPD
- Gerar relatórios de auditoria de acesso
- Apresentar tudo em um dashboard interativo

#### Fases do projeto

| Fase | Nome | Descrição |
|------|------|-----------|
| Fase 1 — Fundação | Ambiente controlado | Catálogo, metadados, qualidade e dashboard sobre o dataset Churn Modelling do Kaggle |
| Fase 2 — Classificação | Sensibilidade LGPD | Classificador de dados sensíveis com ML |
| Fase 3 — Detecção | Anomalias | Detector de anomalias e inconsistências nos dados |
| Fase 4 — Auditoria | Churn auditável | Modelo de previsão de churn com rastreabilidade de decisões |

---

### Stack técnica e justificativas

| Ferramenta | Versão | Por que foi escolhida |
|------------|--------|----------------------|
| Python | latest | linguagem que possibilita a engenharia de dados |
| SQLite3 | nativa | banco leve, nativa, sem servidor, ideal para Fase 1 |
| Pandas | latest | organização, limpeza e manipulação dos dados |
| Plotly | latest | gráficos interativos e profissionais |
| Streamlit | latest | dashboard web e interativos |

---

### Dataset — Fase 1 — Fundação

**Nome:** Churn Modelling
**Fonte:** Kaggle — shrutimechlearn
**URL:** https://www.kaggle.com/datasets/shrutimechlearn/churn-modelling
**Registros:** 10.000 clientes bancários
**Colunas:** 14

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| RowNumber | INTEGER | índice da linha |
| CustomerId | INTEGER | identificador único do cliente |
| Surname | TEXT | sobrenome do cliente |
| CreditScore | INTEGER | score de crédito |
| Geography | TEXT | país do cliente |
| Gender | TEXT | gênero do cliente |
| Age | INTEGER | idade do cliente |
| Tenure | INTEGER | anos como cliente do banco |
| Balance | REAL | saldo em conta |
| NumOfProducts | INTEGER | número de produtos contratados |
| HasCrCard | INTEGER | possui cartão de crédito (0/1) |
| IsActiveMember | INTEGER | é membro ativo (0/1) |
| EstimatedSalary | REAL | salário estimado |
| Exited | INTEGER | saiu do banco (1) ou não (0) |

**Características:** o dataset está limpo. Sem valores nulos, duplicatas, outliers ou dados discrepantes, pois foi criado para fins educacionais, o que é ideal para a **fase 1**, permitindo validar todas as funcionalidades do catálogo em um ambiente controlado e previsível.

**Limitação:** por ser um dataset educacional, não reflete os problemas reais de qualidade de dados encontrados em produção.

---

### Registro de desenvolvimento

---

#### 📅 Dia 1 — Setup do projeto

**Data:** 15 de maio de 2026
**Objetivo do dia:** criar a estrutura do projeto, configurar o ambiente e publicar o primeiro commit.

**O que foi feito:**
- Criado repositório no GitHub com licença MIT;
- Clonado o repositório localmente via HTTPS;
- Criadas as pastas `data/`, `src/` e `output/`;
- Configurado ambiente virtual Python com `venv`;
- Instaladas as bibliotecas: Streamlit, Pandas, Plotly;
- Gerado `requirements.txt` com as dependências;
- Configurado `.gitignore` para ignorar venv, banco de dados e outputs gerados;
- Criados os arquivos vazios `extractor.py`, `analyzer.py`, `catalog.py` e `app.py`.

**Decisões tomadas:**
- **Git + GitHub desde o início:** o uso do controle de versão permite rastrear todas as alterações e apresentar o histórico de evolução para quem visualizar o projeto;
- **Ambiente virtual com venv:** isola as bibliotecas do projeto, evitando conflitos de versão;
- **Separação src/, data/, output/:** convenção que facilita navegação e manutenção do projeto;
- **.gitignore desde o início:** evita que arquivos desnecessários ou sensíveis subam ao GitHub.

**Commit:** `feat: project structure and initial setup`

---

#### 📅 Dia 2 — Base de dados

**Data:** 16 de maio de 2026
**Objetivo do dia:** baixar o dataset, entender sua estrutura e salvá-lo no banco SQLite.

**O que foi feito:**
- Baixado o dataset Churn Modelling do Kaggle;
- Analisada a estrutura das 14 colunas e 10.000 registros;
- Escrito o script inicial do `extractor.py` com duas funções:
  - `carregar_csv()` — lê o CSV com Pandas;
  - `salvar_no_banco()` — converte o CSV em tabela SQLite;
- Banco `banco_exemplo.db` gerado na pasta `data/`.

**Decisões tomadas:**
- **SQLite como banco de dados:** não requer instalação de servidor, o banco inteiro fica em um único arquivo `.db` e já vem integrado ao Python via `sqlite3`;
- **Dataset Churn Modelling:** dataset real com 10.000 registros bancários, amplamente reconhecido pela comunidade, relevante para o contexto bancário/fintech;
- **Converter CSV para SQLite:** o projeto simula um ambiente real onde os dados estão em banco, não em arquivos soltos.

**Commit:** `feat: load kaggle dataset and save to sqlite database`

---

#### 📅 Dia 3 — Extração de metadados

**Data:** 17 de maio de 2026
**Objetivo do dia:** expandir o extractor para varrer o banco e gerar o catálogo em JSON.

**O que foi feito:**
- Foi expandido o `extractor.py` com três novas funções:
  - `listar_tabelas()` — foi listado todas as tabelas do banco via `sqlite_master`;
  - `extrair_metadados_tabela()` — extraído a estrutura completa de cada tabela via `PRAGMA`;
  - `extrair_catalogo_completo()` — percorrido todas as tabelas e montado o catálogo;
- Gerado o arquivo `output/catalogo.json` com metadados completos.

**Decisões tomadas:**
- **PRAGMA do SQLite para metadados:** comando nativo do SQLite que retorna informações internas da estrutura do banco sem bibliotecas externas.
- **Salvar em JSON:** formato universal de troca de dados, legível por qualquer linguagem e consumível por APIs e dashboards.


**Commit:** `feat: extract and save table metadata to json`

---

#### 📅 Dia 4 — Análise de qualidade

**Data:** 18 de maio de 2026
**Objetivo do dia:** criar o analyzer para medir a qualidade dos dados com score por coluna.

**O que foi feito:**
- Foi criado o `src/analyzer.py` com duas funções:
  - `analisar_qualidade()` — foi analisado os nulos, duplicatas, únicos e estatísticas por coluna;
  - `analisar_banco_completo()` — percorrido todas as tabelas e gerado o relatório completo;
- Gerado o arquivo `output/qualidade.json`;
- Implementado score de qualidade de 0 a 100 por coluna.

**Decisões tomadas:**
- **Arquivo separado analyzer.py:** separação de responsabilidades, pois o extractor extrai estrutura, o analyzer analisa qualidade.
- **Score de 0 a 100:** transforma informações técnicas em algo compreensível para qualquer pessoa.

**Limitação identificada:**
- Análise dos dados incompleta (sem avaliar outlier, dados discrepantes, etc.) por compreender que esse não é o foco principal desse projeto.

**Observação sobre os dados:**
- O dataset retornou score 100 em todas as colunas por ser educacional e sem valores nulos, o que era um comportamento esperado e documentado.

**Commit:** `feat: data quality analyzer with null and score metrics`

---

#### 📅 Dia 5 — Documentação

**Data:** 28 de maio de 2026
**Objetivo do dia:** documentar todas as decisões técnicas, atualizar o README e adicionar comentários no código.

**O que foi feito:**
- Criado `docs/documentation.md` com registro completo do desenvolvimento;
- Atualizado `README.md` bilíngue com objetivo, fases, stack, estrutura e instruções;
- Adicionados comentários explicativos em todas as funções do `extractor.py`.

**Decisões tomadas:**
- **README bilíngue com seções separadas:** português e inglês independentes para que todos possam compreender o projeto.
- **Documentação diária:** registrar decisões no momento em que são tomadas evita perda de contexto.

**Commit:** `docs: add documentation, update README and code comments`

---

### Limitações do projeto

| Limitação | Impacto | Plano |
|-----------|---------|-------|
| Dataset educacional sem nulos | score irreal na fase 1 |
| Score só penaliza nulos | métrica incompleta |
| Banco SQLite sem multiusuário | sem logs de acesso reais |

---

### Próximos passos

- [ ] Construir dashboard Streamlit
- [ ] Classificar sensibilidade LGPD com ML — Fase 2
- [ ] Detector de anomalias — Fase 3
- [ ] Modelo de churn auditável — Fase 4

---

---

## 🇺🇸 English

### About this file

This file provides a complete and chronological record of the entire project development process: technical decisions, created scripts, selected tools, analyses performed, limitations encountered, and next steps.

Updates will be made at the end of each project development day.

---

### Project context

#### Problem
Financial institutions deal with growing volumes of customer data and, in some cases, lack structured governance processes to identify what data exists, assess its quality, determine which data is sensitive under the LGPD, and track who has access to it.

#### Proposed solution
An automated data catalog that:
- Automatically documents the structure of any database;
- Monitors data quality with per-column scoring;
- Classifies data sensitivity based on LGPD;
- Generates access audit reports;
- Presents everything in an interactive dashboard.

#### Project phases

| Phase | Name | Description |
|-------|------|-------------|
| Phase 1 — Foundation | Controlled environment | Catalog, metadata, quality, and dashboard over Kaggle's Churn Modelling dataset |
| Phase 2 — Classification | LGPD Sensitivity | ML-based sensitive data classifier |
| Phase 3 — Detection | Anomalies | Anomaly and inconsistency detector |
| Phase 4 — Audit | Auditable Churn | Churn prediction model with decision traceability |

---

### Tech stack and justifications

| Tool | Version | Why it was chosen |
|------|---------|-------------------|
| Python | latest | standard language for data engineering |
| SQLite | native | lightweight, serverless, ideal for Phase 1 |
| Pandas | latest | data organization, cleaning, and manipulation |
| Plotly | latest | interactive and professional charts |
| Streamlit | latest | interactive web dashboards |

---

### Dataset — Phase 1 — Foundation

**Name:** Churn Modelling
**Source:** Kaggle — shrutimechlearn
**URL:** https://www.kaggle.com/datasets/shrutimechlearn/churn-modelling
**Records:** 10,000 banking customers
**Columns:** 14

| Column | Type | Description |
|--------|------|-------------|
| RowNumber | INTEGER | row index |
| CustomerId | INTEGER | unique customer identifier |
| Surname | TEXT | customer surname |
| CreditScore | INTEGER | credit score |
| Geography | TEXT | customer country |
| Gender | TEXT | customer gender |
| Age | INTEGER | customer age |
| Tenure | INTEGER | years as bank customer |
| Balance | REAL | account balance |
| NumOfProducts | INTEGER | number of contracted products |
| HasCrCard | INTEGER | has credit card (0/1) |
| IsActiveMember | INTEGER | is active member (0/1) |
| EstimatedSalary | REAL | estimated salary |
| Exited | INTEGER | left the bank (1) or not (0) |

**Characteristics:** the dataset is clean, with no null values, duplicates, outliers, or inconsistent data, since it was created for educational purposes. This makes it ideal for **Phase 1**, allowing all catalog functionalities to be validated in a controlled and predictable environment.

**Limitation:** because it is an educational dataset, it does not reflect the real-world data quality issues typically found in production environments.

---

### Development log

---

#### 📅 Day 1 — Project setup

**Goal:** create project structure, configure the environment, and publish the first commit.

**What was done:**
- Created GitHub repository with MIT license;
- Cloned repository locally via HTTPS;
- Created folders `data/`, `src/` and `output/`;
- Configured Python virtual environment with `venv`;
- Installed libraries: Streamlit, Pandas, Plotly;
- Generated `requirements.txt` with dependencies;
- Configured `.gitignore` to ignore venv, database, and generated outputs;
- Created empty files: `extractor.py`, `analyzer.py`, `catalog.py`, and `app.py`.

**Decisions made:**
- **Git + GitHub from the start:** the use of version control makes it possible to track all changes and present the project’s evolution history to anyone reviewing it.
- **Virtual environment with venv:** isolates project libraries, avoiding version conflicts.
- **src/, data/, output/ separation:** convention that facilitates navigation and maintenance.
- **.gitignore from the start:** prevents unnecessary or sensitive files from being pushed to GitHub.

**Commit:** `feat: project structure and initial setup`

---

#### 📅 Day 2 — Database

**Goal:** download the dataset, understand its structure, and save it to SQLite.

**What was done:**
- Downloaded Churn Modelling dataset from Kaggle;
- Analyzed structure of 14 columns and 10,000 records;
- Written initial `extractor.py` script with two functions:
  - `carregar_csv()` — reads CSV with Pandas;
  - `salvar_no_banco()` — converts CSV to SQLite table;
- Generated `banco_exemplo.db` in the `data/` folder.

**Decisions made:**
- **SQLite as database:** no server installation required, entire database in a single `.db` file, natively integrated with Python via `sqlite3`.
- **Churn Modelling dataset:** real dataset with 10,000 banking records, widely recognized by the data community.
- **Convert CSV to SQLite:** simulates a real environment where data lives in a database, not loose files.

**Commit:** `feat: load kaggle dataset and save to sqlite database`

---

#### 📅 Day 3 — Metadata extraction

**Goal:** expand the extractor to scan the database and generate the catalog in JSON.

**What was done:**
- Expanded `extractor.py` with three new functions:
  - `listar_tabelas()` — lists all tables via `sqlite_master`;
  - `extrair_metadados_tabela()` — extracts full structure via `PRAGMA`;
  - `extrair_catalogo_completo()` — iterates all tables and builds catalog;
- Generated `output/catalogo.json` with complete metadata.

**Decisions made:**
- **SQLite PRAGMA for metadata:** native command that returns internal structure information without external libraries.
- **Save as JSON:** universal data exchange format, readable by any language.


**Commit:** `feat: extract and save table metadata to json`

---

#### 📅 Day 4 — Quality analysis

**Goal:** create the analyzer to measure data quality with per-column scoring.

**What was done:**
- Created `src/analyzer.py` with two functions:
  - `analisar_qualidade()` — analyzes nulls, duplicates, unique values, and statistics per column;
  - `analisar_banco_completo()` — iterates all tables and generates full report;
- Generated `output/qualidade.json`;
- Implemented quality score from 0 to 100 per column.

**Decisions made:**
- **Separate analyzer.py file:** separation of concerns, extractor extracts structure, analyzer measures quality.
- **Score from 0 to 100:** transforms technical information into something understandable for anyone.

**Limitation identified:**
- Incomplete data analysis (without evaluating outliers, inconsistent data, etc.), as this is not considered the main focus of this project.

**Note on the data:**
- The dataset returned a score of 100 for all columns because it is educational and contains no null values, which was an expected and documented behavior.

**Commit:** `feat: data quality analyzer with null and score metrics`

---

#### 📅 Day 5 — Documentation

**Goal:** document all technical decisions, update README, and add code comments.

**What was done:**
- Created `docs/documentation.md` with complete development log;
- Updated bilingual `README.md` with objective, phases, stack, structure, and instructions;
- Added explanatory comments to all functions in `extractor.py`.

**Decisions made:**
- **Bilingual README with separate sections:** independent Portuguese and English sections, so that everyone can understand the project.
- **Daily documentation:** recording decisions at the moment they are made helps prevent loss of context.

**Commit:** `docs: add documentation, update README and code comments`

---

### Project limitations

| Limitation | Impact | Plan |
|------------|--------|------|
| Educational dataset without nulls | unrealistic score in Phase 1 |
| Score only penalizes nulls | incomplete metric |
| SQLite without multi-user | no real access logs |

---

### Next steps

- [ ] Build Streamlit dashboard
- [ ] LGPD sensitivity classification with ML — Phase 2
- [ ] Anomaly detector — Phase 3
- [ ] Auditable churn model — Phase 4