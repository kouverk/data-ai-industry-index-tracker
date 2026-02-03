# Data Insights

This document captures key insights discovered during data exploration and analysis. These findings will inform dashboard design and highlight interesting trends for the final presentation.

---

## Dataset Overview

### Hacker News "Who Is Hiring"

| Metric | Value |
|--------|-------|
| Total posts (2011-2025) | 93,031 |
| Posts from 2018+ | 56,790 (61%) |
| Posts in 2024 | 4,119 |
| Posts with role detected | 61.6% |
| Posts with technology detected | 52.7% |
| Average technologies per post | 1.3 |

### LinkedIn Jobs

| Metric | Value |
|--------|-------|
| Total job postings | 1,348,454 |
| Jobs with pre-extracted skills | 1,296,381 (96%) |
| Data/ML relevant jobs | 6,383 (0.5%) |
| Coverage | January 2024 snapshot |

### GitHub Repository Stats

| Metric | Value |
|--------|-------|
| Repositories tracked | 81 |
| Categories | 14 |
| Total stars tracked | 2.5M+ |
| Update frequency | Daily (in pipeline) |

---

## Key Findings

### 1. HN Posting Volume Reflects Tech Market Cycles

**Observation:** HN "Who Is Hiring" post counts correlate with tech hiring cycles.

| Year | Post Count | Context |
|------|------------|---------|
| 2018 | 9,828 | Strong market |
| 2019 | 8,664 | Continued growth |
| 2020 | 7,317 | COVID slowdown |
| 2021 | **10,570** | Post-COVID hiring surge (peak) |
| 2022 | 7,787 | Inflation concerns, rate hikes |
| 2023 | 4,306 | Tech layoffs era |
| 2024 | 4,119 | Recovery beginning |
| 2025 | 4,199 | (partial year) |

**Insight:** 2021 was peak hiring; 2023-2024 dropped to ~40% of peak volume.

---

### 2. Role Prevalence in HN Posts (2018+)

| Role | % of Posts | Notes |
|------|------------|-------|
| Software Engineer | 37.9% | Most common (HN is tech-focused) |
| DevOps Engineer | 12.4% | Infrastructure roles common |
| Backend Engineer | 10.1% | Overlaps with many data roles |
| Data Scientist | 8.3% | Strong presence |
| **Data Engineer** | **6.0%** | Core focus of this project |
| Site Reliability Engineer | 5.1% | Modern infra role |
| Machine Learning Engineer | 3.5% | Growing |
| Data Analyst | 1.3% | Less common on HN (more LinkedIn) |
| Analytics Engineer | 0.3% | Still emerging |

**Insight:** Data Engineer at 6% = ~3,400 posts since 2018. Analytics Engineer is still small but growing (emerged ~2019).

---

### 3. Technology Trends: Modern Data Stack Rise

**Cloud Warehouses Overtaking Legacy**

| Year | Redshift | Snowflake | BigQuery | Databricks |
|------|----------|-----------|----------|------------|
| 2018 | 1.3% | 0.2% | 0.5% | 0.1% |
| 2019 | 1.1% | 0.4% | 0.8% | 0.0% |
| 2020 | 0.5% | 0.3% | 0.6% | 0.0% |
| 2021 | 0.5% | 0.6% | 0.7% | 0.1% |
| 2022 | 0.5% | 0.8% | 0.8% | 0.3% |
| 2023 | 0.5% | 1.1% | 0.7% | 0.3% |
| 2024 | 0.2% | **1.6%** | 0.4% | 0.6% |
| 2025 | 0.3% | 1.2% | 1.2% | 0.5% |

**Insight:** Snowflake overtook Redshift around 2021-2022 and now leads the pack. Redshift in decline.

---

### 4. dbt Emergence

| Year | dbt % |
|------|-------|
| 2018 | 0.0% |
| 2019 | 0.0% |
| 2020 | 0.2% |
| 2021 | 0.5% |
| 2022 | 0.6% |
| 2023 | 0.7% |
| 2024 | 0.6% |
| 2025 | 0.8% |

**Insight:** dbt essentially didn't exist in job posts before 2020, then grew steadily. Still under 1% but represents a significant shift in data transformation practices.

---

### 5. AI/ML Framework Shift: PyTorch vs TensorFlow

| Year | PyTorch | TensorFlow | Winner |
|------|---------|------------|--------|
| 2018 | 0.2% | 1.4% | TensorFlow |
| 2019 | 0.5% | 1.2% | TensorFlow |
| 2020 | 0.9% | 1.8% | TensorFlow |
| 2021 | 0.9% | 1.0% | Tie |
| 2022 | **1.5%** | 0.6% | PyTorch |
| 2023 | 1.0% | 1.0% | Tie |
| 2024 | 1.6% | 0.6% | PyTorch |
| 2025 | **2.0%** | 0.4% | PyTorch |

**Insight:** TensorFlow dominated until 2021, then PyTorch took over. PyTorch now leads 2.0% vs 0.4% (5x).

---

### 6. The ChatGPT Effect (OpenAI Mentions)

| Year | OpenAI % | Notes |
|------|----------|-------|
| 2018 | 0.1% | Baseline |
| 2019 | 0.1% | - |
| 2020 | 0.0% | - |
| 2021 | 0.2% | GPT-3 era |
| 2022 | 0.4% | Pre-ChatGPT |
| 2023 | **1.7%** | ChatGPT launched Nov 2022 |
| 2024 | **1.9%** | Continued growth |
| 2025 | **2.7%** | GenAI ubiquity |

**Insight:** OpenAI mentions exploded 4x from 2022 to 2023 (ChatGPT effect) and continue climbing.

---

### 7. Infrastructure Technology Maturity

**Docker peaked and is declining; Kubernetes stable**

| Year | Docker | Kubernetes | Terraform |
|------|--------|------------|-----------|
| 2018 | 10.6% | 8.4% | 2.7% |
| 2019 | 11.1% | 11.0% | 4.3% |
| 2020 | 8.2% | 10.3% | 4.9% |
| 2021 | 6.8% | 10.4% | 5.4% |
| 2022 | 5.9% | 11.5% | 5.8% |
| 2023 | 5.6% | 9.0% | 4.6% |
| 2024 | 4.2% | 7.9% | 4.6% |
| 2025 | 5.5% | 9.2% | 5.2% |

**Insight:** Docker peaked in 2019 (11.1%) and has declined as containerization became assumed. Kubernetes remains stable. Terraform growing steadily.

---

### 8. Database Popularity

| Database | % of Posts | Type |
|----------|------------|------|
| PostgreSQL | 14.6% | Relational OSS |
| Redis | 4.5% | Key-Value |
| MySQL | 3.1% | Relational OSS |
| MongoDB | 3.0% | Document |
| Elasticsearch | 3.0% | Search |
| DynamoDB | 0.7% | Document (AWS) |
| SQL Server | 0.6% | Relational Commercial |
| Cassandra | 0.6% | Wide Column |

**Insight:** PostgreSQL dominates at 14.6% - nearly 3x the next database. HN companies strongly prefer open source.

---

### 9. Programming Language Mentions

| Language | % of Posts |
|----------|------------|
| Python | 23.2% |
| Java | 8.2% |
| Scala | 7.3% |
| Rust | 4.4% |
| Go | 4.1% |
| SQL | 3.9% |
| R | 1.5% |

**Insight:** Python dominates data/ML jobs at 23%. SQL at 3.9% seems low, but SQL is often assumed rather than explicitly listed.

---

### 10. LinkedIn vs HN Comparison

Initial observations from the LinkedIn dataset:

| Aspect | LinkedIn | HN |
|--------|----------|-----|
| Volume | 1.3M jobs | 93K posts |
| Time coverage | Jan 2024 snapshot | 2011-2025 monthly |
| DE/ML jobs | 0.5% (6,383) | 6%+ when filtered |
| Skills | Pre-extracted | Requires NLP |
| Company type | Enterprise + startups | Startup-heavy |

**Insight:** LinkedIn has volume; HN has time series and startup signal. Combining both gives a fuller picture.

---

### 11. GitHub Stars: Developer Interest Signal

**Top 20 Repositories by Stars (Jan 2025)**

| Rank | Repository | Stars | Category |
|------|------------|-------|----------|
| 1 | tensorflow/tensorflow | 193,382 | ml_framework |
| 2 | ollama/ollama | 159,673 | llm |
| 3 | huggingface/transformers | 155,276 | llm |
| 4 | langchain-ai/langchain | 124,420 | llm |
| 5 | kubernetes/kubernetes | 119,880 | infrastructure |
| 6 | pytorch/pytorch | 96,696 | ml_framework |
| 7 | ggerganov/llama.cpp | 93,166 | llm |
| 8 | elastic/elasticsearch | 75,892 | database |
| 9 | redis/redis | 72,553 | database |
| 10 | apache/superset | 70,121 | bi |

**Insight:** LLM tools dominate the top 10 - Ollama, Transformers, LangChain, llama.cpp all in top 7. This is the GenAI boom in developer mindshare.

---

### 12. GitHub: Tool Comparisons Within Categories

**Orchestration**

| Tool | Stars | Notes |
|------|-------|-------|
| Airflow | 43,885 | Incumbent, mature |
| Kestra | 26,243 | Fast-growing newcomer |
| Prefect | 21,350 | Modern alternative |
| Luigi | 18,619 | Original, stable |
| Dagster | 14,762 | Developer-friendly |
| Mage | 8,613 | Notebook-style |

**Insight:** Airflow still dominates but Kestra has surprising momentum (26K stars). Prefect and Dagster are competitive alternatives.

---

**Transformation**

| Tool | Stars | Notes |
|------|-------|-------|
| pandas | 47,606 | Universal |
| Spark | 42,651 | Big data standard |
| Polars | 37,022 | Fast-growing Rust alternative |
| dask | 13,719 | Distributed pandas |
| Trino | 12,430 | Query federation |
| dbt | 12,104 | Analytics transformation |

**Insight:** Polars at 37K stars is remarkable for a newer project - close to Spark. The Rust-based "fast pandas" movement is real.

---

**Vector Databases**

| Tool | Stars | Notes |
|------|-------|-------|
| Milvus | 42,278 | Enterprise-focused |
| FAISS | 38,779 | Facebook's original |
| Qdrant | 28,249 | Rust-based |
| Chroma | 25,528 | Python-native |
| pgvector | 19,320 | PostgreSQL extension |
| Weaviate | 15,420 | GraphQL-first |

**Insight:** Vector DB space is crowded and competitive. pgvector at 19K shows demand for "just add vectors to Postgres" approach.

---

**BI Tools**

| Tool | Stars | Notes |
|------|-------|-------|
| Superset | 70,121 | Apache project, feature-rich |
| Metabase | 45,619 | Simple, popular |
| Redash | 28,155 | Query-focused |
| Evidence | 5,820 | Code-first BI |
| Lightdash | 5,476 | dbt-native |

**Insight:** Superset leads open-source BI significantly. Evidence and Lightdash represent the "BI as code" trend.

---

### 13. Job Market vs Developer Interest Correlation

Comparing HN job mentions with GitHub stars reveals interesting patterns:

| Technology | HN Job % | GitHub Stars | Correlation |
|------------|----------|--------------|-------------|
| TensorFlow | 0.4% (declining) | 193K | Stars high, jobs declining |
| PyTorch | 2.0% (growing) | 97K | Both growing |
| dbt | 0.8% | 12K | Jobs higher relative to stars |
| Airflow | 0.9% | 44K | Mature, stable demand |
| Snowflake | 1.6% | N/A (closed) | Jobs without OSS signal |

**Insight:**
- TensorFlow has legacy stars but PyTorch is winning new jobs
- dbt punches above its star count in job market (practitioners > stargazers)
- Closed-source tools (Snowflake, Databricks) need job data since no GitHub signal

---

## Questions for Dashboard

Based on these insights, the dashboard should answer:

1. **Technology Trends**
   - Which technologies are growing/declining?
   - When did [technology] first appear in job posts?
   - What technologies co-occur frequently?

2. **Role Evolution**
   - Is Analytics Engineer overtaking Data Analyst?
   - What happened to Data Scientist demand post-2022?
   - How do role titles vary between platforms?

3. **Market Events**
   - How did ChatGPT launch affect AI job postings?
   - Did 2023 layoffs show in HN posting volume?
   - COVID effect on remote data roles?

4. **Platform Comparison**
   - Do HN startups want different skills than LinkedIn enterprises?
   - Which platform has more AI/ML focus?

---

## Data Quality Notes

### Issues Discovered

1. **"Atlan" false positive** - The data catalog tool "Atlan" at 0.9% may be matching unrelated text. Needs investigation.

2. **HTML encoding in HN** - Text contains HTML entities (`&#x2F;`, `&amp;`) that need cleaning before analysis.

3. **LinkedIn skills format** - Skills stored as comma-separated strings, not normalized. Requires splitting.

4. **No per-comment timestamp in HN** - Can only bucket by month, not exact date.

### Validation Recommendations

- Spot-check extracted technologies against original text
- Compare HN skill frequencies with LinkedIn skill frequencies
- Verify role extraction with manual sampling

---

## LLM Skill Extraction Analysis

### 14. LLM vs Regex Extraction: Coverage Comparison

A 10,000-post sample was processed through Claude Haiku for structured skill extraction, then compared against the regex-based keyword matching pipeline. Results reveal significant differences in coverage.

| Metric | LLM (Claude Haiku) | Regex (Keyword Match) |
|--------|--------------------|-----------------------|
| Posts processed | 9,818 (98.2% success) | 9,818 (overlapping set) |
| Total mentions | 63,013 | ~15,000 |
| Unique technologies | 4,569 | 152 (taxonomy-limited) |
| Avg technologies/post | ~6.4 | ~1.5 |
| Cost | ~$4.50 | $0 |

**Insight:** The LLM extracts ~4x more technology mentions per post. The regex taxonomy is limited to 152 canonical names, while the LLM identifies 4,569 distinct technologies including frameworks, libraries, and tools not in the seed CSVs.

---

### 15. Agreement Rates: Where LLM and Regex Align

| Technology | LLM Count | Regex Count | Both | Agreement % | Notes |
|------------|-----------|-------------|------|-------------|-------|
| PostgreSQL | 1,757 | 1,178 | 1,162 | 66.1% | Highest agreement - both detect reliably |
| AWS | 2,542 | 1,576 | 1,445 | 56.8% | Strong overlap, LLM catches more |
| MySQL | 948 | 474 | 465 | 49.1% | Solid agreement |
| Python | 4,758 | 2,253 | 2,217 | 46.6% | LLM finds 2x more - regex misses contextual mentions |
| Scala | 632 | 816 | 362 | 44.4% | Regex actually finds more (broader matching) |
| MongoDB | 861 | 383 | 375 | 43.6% | Good agreement on what regex finds |
| Rust | 272 | 586 | 272 | 46.4% | Regex finds 2x more - likely false positives from word "rust" |

**Insight:** PostgreSQL and AWS have the highest agreement (~56-66%), meaning both methods reliably detect them. Technologies with simple, unique names (PostgreSQL, MySQL) have better agreement than ones with common-word names.

---

### 16. LLM-Only Detections: What Regex Misses

Technologies found by the LLM but completely absent from the regex taxonomy:

| Technology | LLM Mentions | In Taxonomy? |
|------------|-------------|--------------|
| React | 1,880 | No |
| JavaScript | 1,479 | No |
| TypeScript | 975 | No |
| Java | 917 | No |
| Node.js | 788 | No |
| Ruby on Rails | 610 | No |
| C++ | ~500 | No |
| GraphQL | ~400 | No |

**Insight:** The regex taxonomy was designed for data/AI-specific tools and deliberately excludes general programming technologies (React, JavaScript, Java). The LLM doesn't have this filter and extracts everything mentioned. This is a feature, not a bug - it shows the LLM captures the full tech stack context around data roles.

---

### 17. Regex-Only Detections: Where LLM Underperforms

| Technology | Regex Count | LLM Count | Regex-Only |
|------------|-------------|-----------|------------|
| Rust | 586 | 272 | 314 |
| Scala | 816 | 632 | 454 |
| GCP | 328 | 1,105 | 190 |
| AWS | 1,576 | 2,542 | 131 |

**Insight:** Rust has 314 regex-only detections, likely false positives from the word "rust" appearing in non-technology contexts. Scala's higher regex count may stem from the keyword matching broader variations. These cases highlight where regex can be overly aggressive.

---

### 18. LLM Extraction Quality Metrics

| Metric | Value |
|--------|-------|
| Success rate | 98.2% (9,818 / 10,000) |
| Failure cause | JSON truncation from max_tokens limit (182 errors) |
| Average confidence score | 0.94 |
| Model used | Claude 3 Haiku |
| Total cost | ~$4.50 for 10K posts |
| Processing time | ~25 minutes |

**Insight:** At $0.00045 per post, LLM extraction is cost-effective for enrichment. The 98.2% success rate is production-viable. The remaining 1.8% failures are all from the LLM's JSON response being truncated (posts with many technologies exceed the 1024 max_tokens limit).

---

### 19. Key Takeaway: LLM vs Regex Trade-offs

| Dimension | LLM | Regex |
|-----------|-----|-------|
| **Coverage** | Broad (4,569 technologies) | Narrow (152 curated) |
| **Precision** | High (0.94 avg confidence) | Moderate (false positives on common words) |
| **Cost** | $0.00045/post | Free |
| **Scalability** | API-limited, ~25 min/10K | Instant on full dataset |
| **Maintenance** | Zero (model handles variations) | Manual (update seed CSVs) |
| **Consistency** | Slight variation between runs | Deterministic |

**Recommendation:** Use regex for the full historical dataset (93K posts) where cost and speed matter. Use LLM extraction on samples for validation, taxonomy discovery, and enrichment. The LLM identified hundreds of technologies not in the seed CSVs, which can be used to expand the regex taxonomy.
