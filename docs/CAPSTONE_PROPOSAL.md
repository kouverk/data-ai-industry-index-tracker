# Capstone Proposal: AI Industry Intelligence Platform

## Executive Summary

The **AI Industry Intelligence Platform** is a dual-lens analytics system that provides comprehensive visibility into the AI industry through two complementary perspectives:

1. **Market Signals Module** — Tracks job market trends, skill demand, and technology adoption across the data/AI ecosystem
2. **Policy Signals Module** — Monitors what AI companies say publicly versus what they lobby for in Washington

Together, these modules answer two fundamental questions:
- **What is the AI industry building?** (hiring patterns, technology adoption)
- **How is the AI industry shaping policy?** (lobbying activity, stated positions)

Both modules share a common modern data stack (Airflow, dbt, Snowflake) and leverage LLM-powered analysis, unified under a single Streamlit dashboard.

---

## 1. Project Description & Scope

### 1.1 Platform Overview

| Module | Focus | Core Question |
|--------|-------|---------------|
| **Market Signals** | Job postings, skills, GitHub activity | "What's hot, growing, or dying in data/AI?" |
| **Policy Signals** | Lobbying disclosures, policy submissions | "Do AI companies practice what they preach?" |

### 1.2 Market Signals Module

**Purpose:** Build a multi-source analytics platform that tracks interest, demand, and growth signals across the data engineering and AI ecosystem.

**Scope:**
- Ingest job postings from Hacker News "Who Is Hiring" threads (2011-present) and LinkedIn (1.3M jobs)
- Extract skills and technologies from unstructured job text using keyword matching and taxonomy standardization
- Track GitHub repository activity for 81 key data/AI tools
- Aggregate trends by month, technology category, and role type
- Visualize technology adoption curves, role evolution, and cross-platform comparisons

**Key Capabilities:**
- Technology trend analysis (Snowflake vs Databricks adoption over time)
- Role evolution tracking (rise of "Analytics Engineer" title)
- Skill co-occurrence analysis (what technologies appear together)
- Platform comparison (HN startup jobs vs LinkedIn enterprise)

### 1.3 Policy Signals Module

**Purpose:** Create a document intelligence pipeline that surfaces discrepancies between AI companies' public statements and their lobbying activity.

**Scope:**
- Ingest 10,068 AI policy submissions from the Federal Register RFI (90 FR 9088)
- Extract structured policy positions using Claude LLM
- Pull lobbying disclosure filings from Senate LDA API
- Match entities across sources (resolve "OpenAI" vs "OpenAI, Inc." variations)
- Calculate discrepancy scores comparing stated positions to lobbying activity
- Monitor for new filings on an ongoing basis

**Key Capabilities:**
- LLM-powered position extraction from unstructured policy documents
- Lobbying spend tracking by company, year, and issue area
- Discrepancy scoring (0-100 scale measuring say-do gap)
- China rhetoric analysis (tracking how companies invoke "China competition")

---

## 2. Conceptual Data Model & Diagrams

### 2.1 Market Signals Module — Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA SOURCES                                    │
├───────────────────────┬───────────────────────┬─────────────────────────────┤
│   Hacker News         │   LinkedIn Jobs       │   GitHub API                │
│   (HuggingFace)       │   (Kaggle)            │   (REST)                    │
│   Parquet, 93K posts  │   CSV, 1.3M jobs      │   JSON, 81 repos            │
└───────────┬───────────┴───────────┬───────────┴──────────────┬──────────────┘
            │                       │                          │
            ▼                       ▼                          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EXTRACTION LAYER (Python)                            │
│   hn_extract.py              linkedin_load.py           github_extract.py    │
│   - HuggingFace download     - Kaggle CSV load          - GitHub API calls   │
│   - Parquet parsing          - Multi-file join          - Rate limiting      │
└───────────────────────────────────────────────────────────────────────────────┘
            │                       │                          │
            ▼                       ▼                          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SNOWFLAKE RAW LAYER                                  │
│   RAW_HN_JOB_POSTINGS (93K)                                                  │
│   RAW_LINKEDIN_POSTINGS (1.3M)                                               │
│   RAW_LINKEDIN_SKILLS (1.3M)                                                 │
│   RAW_LINKEDIN_SUMMARIES (1.3M)                                              │
│   RAW_GITHUB_REPO_STATS (81)                                                 │
└─────────────────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         dbt TRANSFORMATION                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  STAGING (source-conformed, 1:1 with raw)                                    │
│  ├── stg_hn__job_postings           - Parse dates, clean HTML entities       │
│  ├── stg_linkedin__postings         - Standardize columns                    │
│  ├── stg_linkedin__skills           - Explode skills array                   │
│  ├── stg_linkedin__summaries        - Clean text                             │
│  └── stg_github__repo_stats         - Parse timestamps                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  INTERMEDIATE (business logic, enrichment)                                   │
│  ├── int_hn__technologies_extracted - Match text to 175 tech keywords        │
│  ├── int_hn__roles_extracted        - Match text to 78 role keywords         │
│  ├── int_hn__databases_extracted    - Match text to 53 database keywords     │
│  └── int_linkedin__skills_standard  - Map raw skills to canonical names      │
├─────────────────────────────────────────────────────────────────────────────┤
│  MARTS (analytics-ready dimensional model)                                   │
│  ├── dim_technologies (152)         - Technology master list                 │
│  ├── dim_roles (27)                 - Role taxonomy                          │
│  ├── dim_date (191)                 - Date dimension                         │
│  ├── fct_monthly_technology_trends  - Monthly tech mention aggregates        │
│  ├── fct_monthly_role_trends        - Monthly role mention aggregates        │
│  ├── fct_hn_technology_mentions     - Grain: 1 row per mention               │
│  ├── fct_hn_role_mentions           - Grain: 1 row per mention               │
│  ├── fct_linkedin_skill_counts      - Aggregated skill demand                │
│  └── fct_github_repo_stats          - Repo metrics + activity level          │
└─────────────────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         STREAMLIT DASHBOARD                                  │
│   - Technology trends over time (line charts)                                │
│   - Role trends over time (line charts)                                      │
│   - GitHub repo leaderboard (bar charts)                                     │
│   - LinkedIn top skills (bar charts)                                         │
│   - Year-over-year comparison (gainers/decliners)                            │
│   - Data explorer with CSV export                                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Policy Signals Module — Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA SOURCES                                    │
├───────────────────────┬───────────────────────┬─────────────────────────────┤
│   AI Policy Docs      │   Senate LDA API      │   OpenSecrets               │
│   (Federal Register)  │   (Lobbying Filings)  │   (Bulk CSV)                │
│   10,068 PDFs, 600MB  │   JSON, 110+ filings  │   CSV, monthly              │
└───────────┬───────────┴───────────┬───────────┴──────────────┬──────────────┘
            │                       │                          │
            ▼                       ▼                          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EXTRACTION LAYER (Python)                            │
│   download_ai_submissions.py     lda_extract.py           opensecrets.py     │
│   - Bulk ZIP download            - REST API pagination    - CSV download     │
│   - PDF text extraction          - Rate limiting          - Deduplication    │
│   - Reducto.ai / PyMuPDF         - Fuzzy name matching                       │
└───────────────────────────────────────────────────────────────────────────────┘
            │                       │                          │
            ▼                       ▼                          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SNOWFLAKE RAW LAYER                                  │
│   RAW_AI_SUBMISSIONS (10K docs → chunked)                                    │
│   RAW_LDA_FILINGS (110+ filings)                                             │
│   RAW_OPENSECRETS_LOBBYING (aggregated spend)                                │
└─────────────────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         dbt TRANSFORMATION                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  STAGING                                                                     │
│  ├── stg_submissions                - Clean text, normalize company names    │
│  ├── stg_lda_filings                - Parse filing metadata                  │
│  └── stg_opensecrets                - Standardize spend data                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  INTERMEDIATE (LLM-powered)                                                  │
│  ├── int_llm_positions              - Claude extracts structured positions   │
│  │                                    {topic, stance, quote, confidence}     │
│  └── int_entity_resolution          - Match "OpenAI" across sources          │
├─────────────────────────────────────────────────────────────────────────────┤
│  MARTS                                                                       │
│  ├── dim_company                    - Company master with aliases            │
│  ├── dim_topic                      - Policy topic taxonomy                  │
│  ├── fct_policy_positions           - Extracted positions per company        │
│  ├── fct_lobbying_activity          - Spend, issues, lobbyists               │
│  └── fct_discrepancy_scores         - Say-do gap scoring (0-100)             │
└─────────────────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         STREAMLIT DASHBOARD                                  │
│   - Company discrepancy leaderboard                                          │
│   - Lobbying spend over time                                                 │
│   - Position breakdown by topic                                              │
│   - China rhetoric tracker                                                   │
│   - Document search with position highlights                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Unified Platform Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      AI INDUSTRY INTELLIGENCE PLATFORM                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────┐    ┌─────────────────────────────┐         │
│  │     MARKET SIGNALS          │    │     POLICY SIGNALS          │         │
│  │                             │    │                             │         │
│  │  Sources:                   │    │  Sources:                   │         │
│  │  • HN Who Is Hiring         │    │  • AI Policy Submissions    │         │
│  │  • LinkedIn Jobs            │    │  • Senate LDA Filings       │         │
│  │  • GitHub Repos             │    │  • OpenSecrets Data         │         │
│  │                             │    │                             │         │
│  │  AI Component:              │    │  AI Component:              │         │
│  │  • Skill extraction         │    │  • Position extraction      │         │
│  │  • Role classification      │    │  • Discrepancy scoring      │         │
│  │                             │    │                             │         │
│  │  Outputs:                   │    │  Outputs:                   │         │
│  │  • Tech trends              │    │  • Lobbying analysis        │         │
│  │  • Role evolution           │    │  • Say-do gap scores        │         │
│  │  • Skill demand             │    │  • China rhetoric tracker   │         │
│  └─────────────┬───────────────┘    └───────────────┬─────────────┘         │
│                │                                    │                        │
│                └────────────────┬───────────────────┘                        │
│                                 │                                            │
│                                 ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────┐        │
│  │                    SHARED INFRASTRUCTURE                         │        │
│  │                                                                  │        │
│  │   Orchestration: Airflow (DAGs for each data source)            │        │
│  │   Transformation: dbt (staging → intermediate → marts)          │        │
│  │   Warehouse: Snowflake (unified schema)                         │        │
│  │   LLM: Claude API (position extraction, analysis)               │        │
│  │   Presentation: Streamlit (unified dashboard)                   │        │
│  └─────────────────────────────────────────────────────────────────┘        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Tools, Data Sources, and Formats

### 3.1 Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Orchestration** | Apache Airflow | Schedule extraction jobs, trigger dbt runs |
| **Transformation** | dbt (data build tool) | SQL-based transformations, testing, documentation |
| **Warehouse** | Snowflake | Cloud data warehouse, unified storage |
| **LLM** | Claude API (Anthropic) | Position extraction, document analysis |
| **PDF Processing** | Reducto.ai / PyMuPDF | Extract text from policy documents |
| **Visualization** | Streamlit | Interactive dashboards |
| **Language** | Python | Extraction scripts, API integrations |
| **Version Control** | Git | Code versioning |

### 3.2 Data Sources — Market Signals Module

| Source | Format | Volume | Refresh | Description |
|--------|--------|--------|---------|-------------|
| **HN Who Is Hiring** | Parquet | 93,031 posts | Monthly | Job postings from HN threads (2011-present) |
| **LinkedIn Jobs** | CSV | 1.3M jobs | Static snapshot | January 2024 job postings + pre-extracted skills |
| **GitHub API** | JSON | 81 repos | Daily | Stars, forks, activity for key data/AI repos |
| **Taxonomy Seeds** | CSV | 306 rows | Manual | Technology (175), role (78), database (53) mappings |

**Source Details:**

1. **Hacker News "Who Is Hiring"**
   - Provider: HuggingFace dataset `brusic/hacker-news-who-is-hiring-posts`
   - Content: All first-level comments from monthly hiring threads
   - Fields: `id`, `by` (author), `text` (job posting), `time`, `parent` (thread ID)
   - Incremental: New months via HN Firebase API

2. **LinkedIn Jobs Dataset**
   - Provider: Kaggle `asaniczka/1-3m-linkedin-jobs-and-skills-2024`
   - Files: `linkedin_job_postings.csv`, `job_skills.csv`, `job_summary.csv`
   - Skills: Pre-extracted by Kaggle dataset creator
   - Limitation: Static snapshot, no time series

3. **GitHub Repository Stats**
   - Provider: GitHub REST API
   - Scope: 81 curated data/AI repositories (Airflow, dbt, Snowflake, PyTorch, etc.)
   - Fields: `stars`, `forks`, `open_issues`, `watchers`, `pushed_at`
   - Categories: orchestration, transformation, warehouse, streaming, llm, mlops, etc.

### 3.3 Data Sources — Policy Signals Module

| Source | Format | Volume | Refresh | Description |
|--------|--------|--------|---------|-------------|
| **AI Policy Submissions** | PDF/DOCX | 10,068 docs | One-time | Responses to 90 FR 9088 RFI |
| **Senate LDA API** | JSON | 110+ filings | Weekly | Lobbying disclosure filings |
| **OpenSecrets** | CSV | Aggregated | Monthly | Lobbying spend by company/year |
| **Federal Register** | JSON | Ongoing | Daily | New AI-related RFIs and rules |
| **Regulations.gov** | JSON | Ongoing | Daily | Public comments on AI dockets |

**Source Details:**

1. **AI Action Plan RFI Submissions**
   - Provider: NITRD (National AI Initiative Office)
   - Citation: 90 FR 9088 (Federal Register)
   - Content: Public responses to Trump administration AI policy RFI
   - Key submitters: OpenAI, Anthropic, Google, Meta, Microsoft, trade groups
   - Processing: PDF text extraction, then LLM position extraction

2. **Senate LDA (Lobbying Disclosure Act)**
   - Provider: Senate Office of Public Records
   - API: `https://lda.senate.gov/api/v1/`
   - Content: Quarterly lobbying disclosure filings
   - Fields: `client`, `registrant`, `expenses`, `lobbying_activities`, `issue_codes`
   - Sample: OpenAI ($1.97M in 2023-2024), Anthropic ($720K)

3. **OpenSecrets Bulk Data**
   - Provider: OpenSecrets.org
   - Content: Aggregated lobbying spend by company, year, issue
   - Use: Trend analysis, cross-reference with LDA filings

---

## 4. Ingestion Strategy & Data Quality Checks

### 4.1 Market Signals — Ingestion Strategy

| Source | Strategy | Frequency | Trigger |
|--------|----------|-----------|---------|
| HN Who Is Hiring | Incremental append | Monthly | 2nd of month, after thread closes |
| LinkedIn Jobs | Full load | One-time | Manual (static dataset) |
| GitHub Repos | Full refresh | Daily | 6:00 AM UTC |
| Taxonomy Seeds | Full refresh | On change | Manual dbt seed |

**Airflow DAGs:**

```
dag_hn_monthly
├── task_fetch_latest_thread_id    # Find new "Who Is Hiring" thread
├── task_extract_job_posts         # Pull comments via API
├── task_upload_to_snowflake       # Load raw data
└── task_trigger_dbt_run           # Rebuild models

dag_github_daily
├── task_fetch_repo_stats          # Hit GitHub API for 81 repos
├── task_upload_to_snowflake       # Load raw data
└── task_trigger_dbt_run           # Rebuild models

dag_dbt_transform
├── task_dbt_run_staging           # Build staging models
├── task_dbt_run_intermediate      # Build intermediate models
├── task_dbt_run_marts             # Build mart models
└── task_dbt_test                  # Run data tests
```

### 4.2 Policy Signals — Ingestion Strategy

| Source | Strategy | Frequency | Trigger |
|--------|----------|-----------|---------|
| AI Submissions | Bulk load + chunk | One-time | Manual download |
| Senate LDA | Incremental by date | Weekly | Every Monday |
| OpenSecrets | Full refresh | Monthly | 1st of month |
| Federal Register | Incremental polling | Daily | 8:00 AM UTC |

**Airflow DAGs:**

```
dag_lda_weekly
├── task_fetch_new_filings         # Query LDA API for new filings
├── task_match_target_companies    # Filter to AI companies
├── task_upload_to_snowflake       # Load raw data
└── task_trigger_dbt_run           # Rebuild models

dag_submissions_llm
├── task_get_unprocessed_chunks    # Find docs without positions
├── task_extract_positions         # Call Claude API
├── task_save_positions            # Store structured output
└── task_trigger_dbt_run           # Rebuild models
```

### 4.3 Data Quality Checks

**dbt Tests (Market Signals):**

| Test | Table | Column(s) | Description |
|------|-------|-----------|-------------|
| `unique` | stg_hn__job_postings | posting_id | No duplicate posts |
| `not_null` | stg_hn__job_postings | posting_id, posting_text | Required fields |
| `accepted_values` | fct_monthly_technology_trends | category | Valid technology categories |
| `relationships` | fct_hn_technology_mentions | technology_name → dim_technologies | Referential integrity |
| `row_count` | stg_linkedin__postings | * | Expect ~1.3M rows |

**dbt Tests (Policy Signals):**

| Test | Table | Column(s) | Description |
|------|-------|-----------|-------------|
| `unique` | stg_lda_filings | filing_uuid | No duplicate filings |
| `not_null` | fct_policy_positions | company_name, topic, stance | Required fields |
| `accepted_values` | fct_policy_positions | stance | Valid stance values (support, oppose, neutral) |
| `range` | fct_discrepancy_scores | score | Between 0 and 100 |

**Additional Quality Checks:**

- **Freshness monitoring:** Alert if HN data not updated in 35 days
- **Volume anomaly detection:** Alert if monthly job count drops >50%
- **LLM confidence thresholds:** Flag positions with confidence < 0.7 for review
- **Entity resolution validation:** Manual review of company name matches

---

## 5. Success Metrics & Stakeholder Value

### 5.1 Technical Success Metrics

| Metric | Target | Module |
|--------|--------|--------|
| Data sources integrated | 6+ | Both |
| Total rows in warehouse | 30M+ | Both |
| dbt models | 30+ | Both |
| dbt tests passing | 95%+ | Both |
| Pipeline uptime | 99%+ | Both |
| LLM extraction accuracy | 85%+ | Policy Signals |
| Dashboard load time | <5 seconds | Both |

### 5.2 Market Signals — Stakeholder Value

| Stakeholder | Value Proposition |
|-------------|-------------------|
| **Job Seekers** | Understand which skills are trending up/down to guide learning investments. See what technologies to prioritize. |
| **Bootcamps & Educators** | Data-driven curriculum decisions based on actual market demand. Know what to teach. |
| **Hiring Managers** | Benchmark job requirements against industry trends. Understand competitive landscape. |
| **Practitioners** | Track the health and direction of their field. See which tools are gaining/losing adoption. |

**Example Insights:**
- "Snowflake mentions grew 340% from 2019-2023, while Redshift declined 15%"
- "Analytics Engineer" role first appeared in HN in 2019, now represents 8% of data roles
- dbt and Snowflake co-occur in 67% of modern data stack job posts

### 5.3 Policy Signals — Stakeholder Value

| Stakeholder | Value Proposition |
|-------------|-------------------|
| **Journalists** | Story leads on corporate hypocrisy. Quantified say-do gaps for reporting. |
| **Policy Researchers** | Systematic analysis of industry positions. Track lobbying patterns over time. |
| **Policymakers** | Understand industry consensus and conflicts. See who's lobbying on what issues. |
| **General Public** | Transparency into how AI companies influence regulation. Accountability tool. |

**Example Insights:**
- "OpenAI's CEO testified for AI regulation, but OpenAI lobbied against CA SB-1047"
- "94 policy submissions invoke 'China competition' — 73% of these oppose specific regulations"
- Anthropic's lobbying spend increased 400% in 2024 Q3 after Claude 3 launch

### 5.4 Combined Platform Value

The unified platform provides **360-degree visibility** into the AI industry:

1. **Demand Signals** (Market) — What skills/tools companies are hiring for
2. **Supply Signals** (Market) — What open-source tools are gaining traction (GitHub)
3. **Strategic Signals** (Policy) — What regulatory environment companies want
4. **Credibility Signals** (Policy) — Whether companies' actions match their words

**Cross-module insights:**
- Compare companies' hiring patterns with their lobbying positions
- Track if companies hiring "AI safety" roles also lobby for safety regulations
- Correlate technology adoption trends with policy advocacy

---

## 6. Agentic AI Components

### 6.1 Market Signals — AI Features

| Feature | Implementation | Status |
|---------|----------------|--------|
| **Skill Extraction** | Keyword matching against 175+ technology taxonomy | ✅ Implemented |
| **Role Classification** | Keyword matching against 78 role patterns | ✅ Implemented |
| **Natural Language Queries** | LLM generates SQL from user questions | 🔜 Planned |
| **Automated Insights** | LLM summarizes weekly trends | 🔜 Planned |

**Planned Chat Interface:**
```
User: "What skills are growing fastest in 2024?"
    ↓
LLM generates SQL → Queries Snowflake → Returns answer:
"Based on HN job postings, the fastest growing skills in 2024 are:
1. LangChain (+340% YoY)
2. dbt (+89% YoY)
3. Snowflake (+45% YoY)"
```

### 6.2 Policy Signals — AI Features

| Feature | Implementation | Status |
|---------|----------------|--------|
| **Position Extraction** | Claude reads documents, extracts structured JSON | ✅ Implemented |
| **Discrepancy Scoring** | Algorithm compares positions to lobbying activity | ✅ Implemented |
| **China Rhetoric Analysis** | Classify claims as verifiable vs rhetorical | ✅ Implemented |
| **Document Q&A** | Chat with policy documents | 🔜 Planned |

**Position Extraction Example:**
```json
Input: "We believe that patchwork state regulations will stifle innovation..."

Output: {
  "topic": "state_regulation",
  "stance": "strong_oppose",
  "supporting_quote": "patchwork state regulations will stifle innovation",
  "confidence": 0.95
}
```

---

## 7. Project Timeline

| Week | Milestone |
|------|-----------|
| 1-2 | Data exploration, prototype extraction logic |
| 3-4 | Snowflake setup, raw data loaded |
| 5-6 | dbt models (staging → intermediate → marts) |
| 7-8 | Airflow DAGs, dashboard v1 |
| 9-10 | LLM integration, refinements |
| 11+ | Documentation, presentation prep |

---

## 8. Repository Structure

```
ai-industry-intelligence/
├── CAPSTONE_PROPOSAL.md          # This document
├── README.md                     # Project overview
│
├── market-signals/               # Job market tracking module
│   ├── include/extraction/       # Python extraction scripts
│   │   ├── hn_extract.py
│   │   ├── linkedin_load.py
│   │   └── github_extract.py
│   ├── dbt/                      # dbt project
│   │   ├── models/staging/
│   │   ├── models/intermediate/
│   │   ├── models/marts/
│   │   └── seeds/
│   ├── dags/                     # Airflow DAGs
│   └── dashboard/app.py          # Streamlit dashboard
│
├── policy-signals/               # Lobbying & policy module
│   ├── include/extraction/       # Python extraction scripts
│   │   ├── download_submissions.py
│   │   ├── lda_extract.py
│   │   └── llm_extract_positions.py
│   ├── dbt/                      # dbt project
│   │   ├── models/staging/
│   │   ├── models/intermediate/
│   │   └── models/marts/
│   ├── dags/                     # Airflow DAGs
│   └── dashboard/app.py          # Streamlit dashboard
│
├── shared/                       # Shared infrastructure
│   ├── snowflake_setup.py        # Schema creation
│   └── utils.py                  # Common utilities
│
└── docs/                         # Documentation
    ├── DATA_DICTIONARY.md
    ├── ARCHITECTURE.md
    └── INSIGHTS.md
```

---

## 9. References

**Data Sources:**
- HuggingFace HN Dataset: https://huggingface.co/datasets/brusic/hacker-news-who-is-hiring-posts
- Kaggle LinkedIn Dataset: https://www.kaggle.com/datasets/asaniczka/1-3m-linkedin-jobs-and-skills-2024
- GitHub REST API: https://docs.github.com/en/rest
- Senate LDA API: https://lda.senate.gov/api/
- Federal Register API: https://www.federalregister.gov/api/v1/
- AI Action Plan Submissions: https://www.nitrd.gov/coordination-areas/ai/90-fr-9088-responses/

**Technology Documentation:**
- dbt: https://docs.getdbt.com/
- Snowflake: https://docs.snowflake.com/
- Airflow: https://airflow.apache.org/docs/
- Streamlit: https://docs.streamlit.io/
- Claude API: https://docs.anthropic.com/
