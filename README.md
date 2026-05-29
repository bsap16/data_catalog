<h1 align="center">🗂️ Automated Data Catalog</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=sqlite&logoColor=white"/>
  <img src="https://img.shields.io/badge/Data%20Governance-0A66C2?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Data%20Engineering-FF6F00?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento%20|%20In%20Development-yellow?style=for-the-badge"/>
</p>

---

## 🇧🇷 Português

### Sobre o projeto

Sendo notável que as instituições financeiras lidam com volumes crescentes de dados de clientes e, algumas vezes sem processos estruturados de governança para saber quais dados existem, qual a qualidade deles, quais são sensíveis pela LGPD e quem os acessa.

Este projeto propõe uma solução prática: um catálogo de dados automatizado que documenta a estrutura dos dados, monitora sua qualidade, classifica sensibilidade e gera relatórios de auditoria, tornando a governança de dados acessível e rastreável.

### Fases do projeto

| Fase | Nome | Descrição | Status |
|------|------|-----------|--------|
| Fase 1 — Fundação | Ambiente controlado | Catálogo, metadados, qualidade e dashboard sobre o dataset Churn Modelling do Kaggle | 🔄 Em andamento |
| Fase 2 — Classificação | Sensibilidade LGPD | Classificador de dados sensíveis com ML | ⏳ Previsto |
| Fase 3 — Detecção | Anomalias | Detector de anomalias e inconsistências nos dados | ⏳ Previsto |
| Fase 4 — Auditoria | Churn auditável | Modelo de previsão de churn com rastreabilidade de decisões | ⏳ Previsto |

### Funcionalidades

**Fase 1 — Fundação**
- [x] Extração automática de metadados de tabelas
- [x] Análise de qualidade com score por coluna
- [ ] Score de qualidade enriquecido
- [ ] Dashboard interativo com Streamlit
- [ ] Relatórios de auditoria de acesso

**Fase 2 — Classificação**
- [ ] Classificação de sensibilidade LGPD com ML

**Fase 3 — Detecção**
- [ ] Detector de anomalias e inconsistências

**Fase 4 — Auditoria**
- [ ] Modelo de churn com rastreabilidade de decisões

### Tecnologias

| Tecnologia | Uso no projeto |
|------------|---------------|
| Python 3 | linguagem principal |
| SQLite | banco de dados local |
| Pandas | manipulação e análise dos dados |
| Plotly | geração de gráficos |
| Streamlit | dashboard web interativo |

### Estrutura do projeto

```
data-catalog/
├── data/                  # banco de dados (gerado localmente)
├── docs/                  # documentação técnica detalhada
│   └── documentation.md   # registro completo do desenvolvimento
├── output/                # arquivos gerados pelos scripts
├── src/                   # scripts Python
│   ├── extractor.py       # extrai metadados do banco
│   ├── analyzer.py        # analisa qualidade dos dados
│   └── catalog.py         # orquestra extractor e analyzer
├── app.py                 # dashboard Streamlit
├── requirements.txt       # dependências do projeto
└── README.md
```

### Como instalar e rodar

```bash
# 1. Clone o repositório
git clone https://github.com/bsap16/data-catalog.git
cd data-catalog

# 2. Crie o ambiente virtual
python -m venv venv
venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Baixe o dataset
# Acesse https://www.kaggle.com/datasets/shrutimechlearn/churn-modelling
# Salve o arquivo Churn_Modelling.csv na pasta data/

# 5. Rode os scripts
python src/extractor.py
python src/analyzer.py

# 6. Inicie o dashboard
streamlit run app.py
```

### Documentação completa

Todas as decisões técnicas, análises, limitações e registros diários de desenvolvimento estão em [docs/documentation.md](docs/documentation.md).

### Autora

**Bruna Paiva**
Estudante de engenharia de software | Formada em Odontologia e Letras
Foco em engenharia e governança de dados
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=flat&logo=gmail&logoColor=white)](mailto:brunasap16@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/bruna-paiva16)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github)](https://github.com/bsap16)

---

## 🇺🇸 English

### About the project

It is noteworthy that financial institutions handle growing volumes of customer data and, at times, do so without structured governance processes to determine what data exists, what its quality is, which data is sensitive under the LGPD (Brazil’s General Data Protection Law, similar to the GDPR), and who has access to it.

This project proposes a practical solution: an automated data catalog that documents data structures, monitors data quality, classifies sensitivity, and generates audit reports, making data governance accessible and traceable.

### Project phases

| Phase | Name | Description | Status |
|-------|------|-------------|--------|
| Phase 1 — Foundation | Controlled environment | Catalog, metadata, quality, and dashboard over Kaggle's Churn Modelling dataset | 🔄 In progress |
| Phase 2 — Classification | LGPD Sensitivity | ML-based sensitive data classifier | ⏳ Planned |
| Phase 3 — Detection | Anomalies | Anomaly and inconsistency detector | ⏳ Planned |
| Phase 4 — Audit | Auditable Churn | Churn prediction model with decision traceability | ⏳ Planned |

### Features

**Phase 1 — Foundation**
- [x] Automatic metadata extraction from tables
- [x] Data quality analysis with per-column score
- [ ] Enriched quality score
- [ ] Interactive Streamlit dashboard
- [ ] Access audit reports

**Phase 2 — Classification**
- [ ] LGPD sensitivity classification with ML

**Phase 3 — Detection**
- [ ] Anomaly and inconsistency detector

**Phase 4 — Audit**
- [ ] Churn model with decision traceability

### Tech stack

| Technology | Usage |
|------------|-------|
| Python 3 | main language |
| SQLite | local database |
| Pandas | data manipulation and analysis |
| Plotly | chart generation |
| Streamlit | interactive web dashboard |

### Project structure

```
data-catalog/
├── data/                  # database (generated locally)
├── docs/                  # detailed technical documentation
│   └── documentation.md   # full development log
├── output/                # files generated by scripts
├── src/                   # Python scripts
│   ├── extractor.py       # extracts database metadata
│   ├── analyzer.py        # analyzes data quality
│   └── catalog.py         # orchestrates extractor and analyzer
├── app.py                 # Streamlit dashboard
├── requirements.txt       # project dependencies
└── README.md
```

### How to install and run

```bash
# 1. Clone the repository
git clone https://github.com/bsap16/data-catalog.git
cd data-catalog

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download the dataset
# Go to https://www.kaggle.com/datasets/shrutimechlearn/churn-modelling
# Save Churn_Modelling.csv inside the data/ folder

# 5. Run the scripts
python src/extractor.py
python src/analyzer.py

# 6. Start the dashboard
streamlit run app.py
```

### Full documentation

All technical decisions, analyses, limitations, and daily development logs are available at [docs/documentation.md](docs/documentation.md).

### Author

**Bruna Paiva**
Software Engineering Student | Dentistry and Languages Studies Graduate
Focus on Data Engineer and Governance
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=flat&logo=gmail&logoColor=white)](mailto:brunasap16@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/bruna-paiva16)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github)](https://github.com/bsap16)