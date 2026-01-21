"""
GitHub Repository Stats Exploration

This script explores using GitHub API to track repository stats for
data/AI tools in our taxonomy. This provides a "developer interest"
signal to complement job market data.

Key metrics:
- Stars (popularity)
- Forks (active usage/contribution)
- Open issues (activity level)
- Recent commits (maintenance health)

No auth required for basic public repo stats (60 requests/hour).
With auth: 5000 requests/hour.
"""

import requests
import time
from datetime import datetime
import json

# =============================================================================
# REPOS TO TRACK
# =============================================================================
# Organized by category, matching our taxonomy
# Format: "owner/repo"

REPOS_TO_TRACK = {
    # -------------------------------------------------------------------------
    # ORCHESTRATION
    # -------------------------------------------------------------------------
    "orchestration": [
        "apache/airflow",
        "dagster-io/dagster",
        "PrefectHQ/prefect",
        "mage-ai/mage-ai",
        "spotify/luigi",
        "argoproj/argo-workflows",
        "kestra-io/kestra",
    ],

    # -------------------------------------------------------------------------
    # TRANSFORMATION
    # -------------------------------------------------------------------------
    "transformation": [
        "dbt-labs/dbt-core",
        "apache/spark",
        "pandas-dev/pandas",
        "pola-rs/polars",
        "dask/dask",
        "trinodb/trino",
    ],

    # -------------------------------------------------------------------------
    # WAREHOUSES / QUERY ENGINES
    # -------------------------------------------------------------------------
    "warehouse": [
        "ClickHouse/ClickHouse",
        "duckdb/duckdb",
        "apache/druid",
        "StarRocks/starrocks",
    ],

    # -------------------------------------------------------------------------
    # STREAMING
    # -------------------------------------------------------------------------
    "streaming": [
        "apache/kafka",
        "apache/flink",
        "apache/pulsar",
        "redpanda-data/redpanda",
        "vectordotdev/vector",
    ],

    # -------------------------------------------------------------------------
    # TABLE FORMATS / DATA LAKE
    # -------------------------------------------------------------------------
    "table_format": [
        "delta-io/delta",
        "apache/iceberg",
        "apache/hudi",
        "apache/parquet-java",
    ],

    # -------------------------------------------------------------------------
    # ETL / ELT
    # -------------------------------------------------------------------------
    "etl_elt": [
        "airbytehq/airbyte",
        "meltano/meltano",
        "dlt-hub/dlt",
        "singer-io/tap-github",  # Singer spec reference
    ],

    # -------------------------------------------------------------------------
    # BI / VISUALIZATION
    # -------------------------------------------------------------------------
    "bi": [
        "metabase/metabase",
        "apache/superset",
        "lightdash/lightdash",
        "evidence-dev/evidence",
        "getredash/redash",
    ],

    # -------------------------------------------------------------------------
    # ML FRAMEWORKS
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # LLMS / GENAI
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # MLOPS
    # -------------------------------------------------------------------------
    "mlops": [
        "mlflow/mlflow",
        "kubeflow/kubeflow",
        "wandb/wandb",
        "bentoml/BentoML",
        "iterative/dvc",
        "zenml-io/zenml",
    ],

    # -------------------------------------------------------------------------
    # VECTOR DATABASES
    # -------------------------------------------------------------------------
    "vector_db": [
        "chroma-core/chroma",
        "weaviate/weaviate",
        "qdrant/qdrant",
        "milvus-io/milvus",
        "facebookresearch/faiss",
        "pgvector/pgvector",
    ],

    # -------------------------------------------------------------------------
    # DATA QUALITY / CATALOG
    # -------------------------------------------------------------------------
    "data_quality": [
        "great-expectations/great_expectations",
        "datahub-project/datahub",
        "sodadata/soda-core",
        "open-metadata/OpenMetadata",
    ],

    # -------------------------------------------------------------------------
    # INFRASTRUCTURE
    # -------------------------------------------------------------------------
    "infrastructure": [
        "kubernetes/kubernetes",
        "docker/compose",
        "hashicorp/terraform",
        "pulumi/pulumi",
        "ansible/ansible",
    ],

    # -------------------------------------------------------------------------
    # DATABASES
    # -------------------------------------------------------------------------
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


def get_repo_stats(owner_repo, token=None):
    """
    Fetch stats for a single repo from GitHub API.

    Returns dict with: stars, forks, open_issues, updated_at, etc.
    """
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


def get_rate_limit(token=None):
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


# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)

    # Check for GitHub token (optional but recommended)
    token = os.environ.get("GITHUB_TOKEN")

    print("="*60)
    print("GITHUB REPOSITORY STATS EXPLORATION")
    print("="*60)

    # Check rate limit
    rate_limit = get_rate_limit(token)
    if rate_limit:
        print(f"\nAPI Rate Limit: {rate_limit['remaining']}/{rate_limit['limit']} remaining")
        print(f"Resets at: {rate_limit['reset']}")

    if not token:
        print("\nNote: No GITHUB_TOKEN found. Using unauthenticated API (60 req/hour).")
        print("Set GITHUB_TOKEN env var for 5000 req/hour.")

    # Count total repos
    total_repos = sum(len(repos) for repos in REPOS_TO_TRACK.values())
    print(f"\nTotal repos to track: {total_repos}")

    # Fetch stats for all repos
    all_stats = []
    errors = []

    for category, repos in REPOS_TO_TRACK.items():
        print(f"\n--- {category.upper()} ({len(repos)} repos) ---")

        for repo in repos:
            stats = get_repo_stats(repo, token)
            stats["category"] = category

            if stats.get("error"):
                errors.append(stats)
                print(f"  ❌ {repo}: {stats['error']}")
            else:
                all_stats.append(stats)
                print(f"  ✓ {repo}: {stats['stars']:,} stars, {stats['forks']:,} forks")

            # Rate limit: wait between requests if no token
            if not token:
                time.sleep(1.0)  # Be nice to GitHub
            else:
                time.sleep(0.1)

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    print(f"\nSuccessfully fetched: {len(all_stats)} repos")
    print(f"Errors: {len(errors)} repos")

    # Sort by stars
    all_stats_sorted = sorted(all_stats, key=lambda x: x.get("stars", 0), reverse=True)

    print("\n--- TOP 20 BY STARS ---")
    for i, repo in enumerate(all_stats_sorted[:20], 1):
        print(f"{i:2}. {repo['repo']:<40} {repo['stars']:>10,} stars  ({repo['category']})")

    # By category
    print("\n--- STATS BY CATEGORY ---")
    for category in REPOS_TO_TRACK.keys():
        cat_repos = [r for r in all_stats if r["category"] == category]
        if cat_repos:
            total_stars = sum(r["stars"] for r in cat_repos)
            avg_stars = total_stars // len(cat_repos)
            top_repo = max(cat_repos, key=lambda x: x["stars"])
            print(f"{category:<20} {len(cat_repos):>3} repos, {total_stars:>12,} total stars, top: {top_repo['repo']}")

    # -------------------------------------------------------------------------
    # INTERESTING COMPARISONS
    # -------------------------------------------------------------------------
    print("\n" + "="*60)
    print("INTERESTING COMPARISONS")
    print("="*60)

    def get_stars(repo_name):
        for r in all_stats:
            if r["repo"] == repo_name:
                return r["stars"]
        return 0

    comparisons = [
        ("Orchestration", "apache/airflow", "dagster-io/dagster", "PrefectHQ/prefect"),
        ("Transformation", "dbt-labs/dbt-core", "apache/spark", "pola-rs/polars"),
        ("ML Framework", "pytorch/pytorch", "tensorflow/tensorflow", "scikit-learn/scikit-learn"),
        ("LLM Tools", "langchain-ai/langchain", "huggingface/transformers", "ollama/ollama"),
        ("Vector DB", "chroma-core/chroma", "qdrant/qdrant", "milvus-io/milvus"),
        ("BI Tools", "metabase/metabase", "apache/superset", "getredash/redash"),
    ]

    for name, *repos in comparisons:
        print(f"\n{name}:")
        for repo in repos:
            stars = get_stars(repo)
            short_name = repo.split("/")[1]
            print(f"  {short_name:<25} {stars:>10,} stars")

    # -------------------------------------------------------------------------
    # SAVE DATA
    # -------------------------------------------------------------------------
    print("\n" + "="*60)
    print("SAVING DATA")
    print("="*60)

    # Save as JSON for now (will be parquet in pipeline)
    output_path = "data/raw/github_repo_stats.json"
    with open(output_path, "w") as f:
        json.dump({
            "fetched_at": datetime.utcnow().isoformat(),
            "repo_count": len(all_stats),
            "repos": all_stats,
            "errors": errors,
        }, f, indent=2)
    print(f"\nSaved to: {output_path}")

    # Also save as simple CSV for quick viewing
    import csv
    csv_path = "data/raw/github_repo_stats.csv"
    with open(csv_path, "w", newline="") as f:
        if all_stats:
            writer = csv.DictWriter(f, fieldnames=[
                "repo", "category", "stars", "forks", "open_issues",
                "language", "created_at", "pushed_at", "license"
            ])
            writer.writeheader()
            for r in all_stats_sorted:
                writer.writerow({
                    "repo": r["repo"],
                    "category": r["category"],
                    "stars": r["stars"],
                    "forks": r["forks"],
                    "open_issues": r["open_issues"],
                    "language": r["language"],
                    "created_at": r["created_at"],
                    "pushed_at": r["pushed_at"],
                    "license": r["license"],
                })
    print(f"Saved to: {csv_path}")

    print("\n" + "="*60)
    print("DONE")
    print("="*60)
    print("\nNotes for pipeline:")
    print("- Run daily to track star growth over time")
    print("- Store historical snapshots for trend analysis")
    print("- Consider using GitHub's star history API for backfill")
    print("- With auth token: 5000 requests/hour = can track 100s of repos")
