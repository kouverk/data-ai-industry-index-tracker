"""
GitHub Repository Stats Extraction

Fetches repository statistics from GitHub API for 81 data/AI tools.
Saves to data/raw/github_repo_stats.json for loading to Snowflake.

Usage:
    python extraction/fetch_github_data.py

Environment:
    GITHUB_TOKEN (optional): GitHub personal access token for higher rate limits
                             Without: 60 requests/hour
                             With: 5000 requests/hour
"""

import os
import json
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# REPOS TO TRACK (81 repositories across 14 categories)
# =============================================================================

REPOS_TO_TRACK = {
    "orchestration": [
        "apache/airflow",
        "dagster-io/dagster",
        "PrefectHQ/prefect",
        "mage-ai/mage-ai",
        "spotify/luigi",
        "argoproj/argo-workflows",
        "kestra-io/kestra",
    ],
    "transformation": [
        "dbt-labs/dbt-core",
        "apache/spark",
        "pandas-dev/pandas",
        "pola-rs/polars",
        "dask/dask",
        "trinodb/trino",
    ],
    "warehouse": [
        "ClickHouse/ClickHouse",
        "duckdb/duckdb",
        "apache/druid",
        "StarRocks/starrocks",
    ],
    "streaming": [
        "apache/kafka",
        "apache/flink",
        "apache/pulsar",
        "redpanda-data/redpanda",
        "vectordotdev/vector",
    ],
    "table_format": [
        "delta-io/delta",
        "apache/iceberg",
        "apache/hudi",
        "apache/parquet-java",
    ],
    "etl_elt": [
        "airbytehq/airbyte",
        "meltano/meltano",
        "dlt-hub/dlt",
        "singer-io/tap-github",
    ],
    "bi": [
        "metabase/metabase",
        "apache/superset",
        "lightdash/lightdash",
        "evidence-dev/evidence",
        "getredash/redash",
    ],
    "ml_framework": [
        "pytorch/pytorch",
        "tensorflow/tensorflow",
        "scikit-learn/scikit-learn",
        "microsoft/LightGBM",
        "dmlc/xgboost",
        "catboost/catboost",
        "keras-team/keras",
        "google/jax",
    ],
    "llm": [
        "langchain-ai/langchain",
        "run-llama/llama_index",
        "huggingface/transformers",
        "ollama/ollama",
        "vllm-project/vllm",
        "ggerganov/llama.cpp",
        "openai/openai-python",
        "anthropics/anthropic-sdk-python",
    ],
    "mlops": [
        "mlflow/mlflow",
        "kubeflow/kubeflow",
        "wandb/wandb",
        "bentoml/BentoML",
        "iterative/dvc",
        "zenml-io/zenml",
    ],
    "vector_db": [
        "chroma-core/chroma",
        "weaviate/weaviate",
        "qdrant/qdrant",
        "milvus-io/milvus",
        "facebookresearch/faiss",
        "pgvector/pgvector",
    ],
    "data_quality": [
        "great-expectations/great_expectations",
        "datahub-project/datahub",
        "sodadata/soda-core",
        "open-metadata/OpenMetadata",
    ],
    "infrastructure": [
        "kubernetes/kubernetes",
        "docker/compose",
        "hashicorp/terraform",
        "pulumi/pulumi",
        "ansible/ansible",
    ],
    "database": [
        "postgres/postgres",
        "redis/redis",
        "mongodb/mongo",
        "elastic/elasticsearch",
        "apache/cassandra",
        "cockroachdb/cockroach",
        "timescale/timescaledb",
        "questdb/questdb",
        "influxdata/influxdb",
    ],
}


def get_repo_stats(owner_repo: str, token: str = None) -> dict:
    """Fetch stats for a single repo from GitHub API."""
    url = f"https://api.github.com/repos/{owner_repo}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return {
                "repo": owner_repo,
                "name": data.get("name"),
                "full_name": data.get("full_name"),
                "description": data.get("description", "")[:200] if data.get("description") else "",
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "open_issues": data.get("open_issues_count", 0),
                "watchers": data.get("watchers_count", 0),
                "language": data.get("language"),
                "created_at": data.get("created_at"),
                "updated_at": data.get("updated_at"),
                "pushed_at": data.get("pushed_at"),
                "size_kb": data.get("size", 0),
                "default_branch": data.get("default_branch"),
                "topics": data.get("topics", []),
                "license": data.get("license", {}).get("spdx_id") if data.get("license") else None,
                "fetched_at": datetime.utcnow().isoformat(),
                "error": None,
            }
        elif response.status_code == 404:
            return {"repo": owner_repo, "error": "Not found"}
        elif response.status_code == 403:
            return {"repo": owner_repo, "error": "Rate limited"}
        else:
            return {"repo": owner_repo, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"repo": owner_repo, "error": str(e)}


def get_rate_limit(token: str = None) -> dict:
    """Check current GitHub API rate limit."""
    url = "https://api.github.com/rate_limit"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        core = data.get("resources", {}).get("core", {})
        return {
            "limit": core.get("limit"),
            "remaining": core.get("remaining"),
            "reset": datetime.fromtimestamp(core.get("reset", 0)).isoformat(),
        }
    return None


def fetch_all_repos(token: str = None) -> tuple[list, list]:
    """Fetch stats for all repos in REPOS_TO_TRACK."""
    all_stats = []
    errors = []

    total_repos = sum(len(repos) for repos in REPOS_TO_TRACK.values())
    print(f"Fetching {total_repos} repositories...")

    for category, repos in REPOS_TO_TRACK.items():
        print(f"\n  {category} ({len(repos)} repos)")

        for repo in repos:
            stats = get_repo_stats(repo, token)
            stats["category"] = category

            if stats.get("error"):
                errors.append(stats)
                print(f"    ✗ {repo}: {stats['error']}")
            else:
                all_stats.append(stats)
                print(f"    ✓ {repo}: {stats['stars']:,} stars")

            # Rate limiting
            if not token:
                time.sleep(1.0)
            else:
                time.sleep(0.1)

    return all_stats, errors


def save_to_json(all_stats: list, errors: list, output_path: str):
    """Save fetched data to JSON file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        json.dump({
            "fetched_at": datetime.utcnow().isoformat(),
            "repo_count": len(all_stats),
            "repos": all_stats,
            "errors": errors,
        }, f, indent=2)

    print(f"\nSaved to: {output_path}")


def run_github_extraction():
    """Main extraction function."""
    print("=" * 60)
    print("GITHUB REPOSITORY STATS EXTRACTION")
    print("=" * 60)

    token = os.getenv("GITHUB_TOKEN")

    # Check rate limit
    rate_limit = get_rate_limit(token)
    if rate_limit:
        print(f"\nRate limit: {rate_limit['remaining']}/{rate_limit['limit']} remaining")

    if not token:
        print("\nNote: No GITHUB_TOKEN found. Using unauthenticated API (60 req/hour).")

    # Fetch all repos
    all_stats, errors = fetch_all_repos(token)

    # Summary
    print("\n" + "=" * 60)
    print(f"Successfully fetched: {len(all_stats)} repos")
    print(f"Errors: {len(errors)} repos")

    # Save to data/raw
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_path = os.path.join(project_root, "data/raw/github_repo_stats.json")

    save_to_json(all_stats, errors, output_path)

    return all_stats, errors


if __name__ == "__main__":
    run_github_extraction()
