# GitHub Repository Selection Criteria

This document explains the methodology for selecting the 81 GitHub repositories tracked in this project.

## Selection Criteria

Repositories were selected based on the following criteria:

1. **Relevance to Data/AI Ecosystem** - Must be a tool, framework, or library used by data engineers, analytics engineers, ML engineers, or data scientists.

2. **Minimum Popularity Threshold** - Generally 1,000+ stars, with exceptions for newer but significant tools (e.g., emerging LLM frameworks).

3. **Open Source** - Must be publicly accessible on GitHub.

4. **Active Development** - Preference for repositories with commits in the last 12 months.

5. **Category Coverage** - Ensured representation across all major categories in the data/AI stack.

## Categories

| Category | Description | Example Repos |
|----------|-------------|---------------|
| `orchestration` | Workflow/pipeline orchestration tools | Airflow, Dagster, Prefect |
| `transformation` | Data transformation frameworks | dbt, Spark, pandas, Polars |
| `warehouse` | Analytical databases | ClickHouse, DuckDB |
| `streaming` | Real-time data processing | Kafka, Flink, Pulsar |
| `table_format` | Data lake table formats | Delta Lake, Iceberg, Hudi |
| `etl_elt` | Data integration tools | Airbyte, Meltano |
| `bi` | Business intelligence tools | Superset, Metabase |
| `ml_framework` | Machine learning frameworks | PyTorch, TensorFlow, scikit-learn |
| `mlops` | ML operations tools | MLflow, Kubeflow, W&B |
| `llm` | Large language model tools | LangChain, Ollama, Transformers |
| `vector_db` | Vector databases for AI | Milvus, Chroma, pgvector |
| `data_quality` | Data quality/observability | Great Expectations, dbt tests |
| `infrastructure` | DevOps/infra tools common in data | Kubernetes, Terraform |
| `database` | General-purpose databases | PostgreSQL, Redis, Elasticsearch |

## Known Limitations

- **Selection bias** - Repos were curated based on the author's knowledge of the ecosystem. Lesser-known but valuable tools may be missing.
- **Star count ≠ quality** - Popular repos aren't necessarily the best technical choice.
- **Enterprise tools excluded** - Proprietary tools (Snowflake, Databricks, etc.) don't have public GitHub repos for comparison.
- **Point-in-time snapshot** - Star counts change daily; our data reflects the fetch date.

## Full Repository List

See `data/raw/github_repo_stats.csv` or query `fct_github_repo_stats` for the complete list with categories.

## Update Process

The GitHub data is refreshed daily via the `dag_github_daily` Airflow DAG, which calls the GitHub REST API for each repository.
