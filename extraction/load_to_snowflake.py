"""
Load Raw Data to Snowflake

Loads extracted data from data/raw/ into Snowflake raw tables.
This is the "L" (Load) step of ELT - data is loaded as-is, then
transformed by dbt.

Usage:
    python extraction/load_to_snowflake.py              # Load all sources
    python extraction/load_to_snowflake.py hn           # Load HN only
    python extraction/load_to_snowflake.py github       # Load GitHub only
    python extraction/load_to_snowflake.py linkedin     # Load LinkedIn only
    python extraction/load_to_snowflake.py verify       # Verify row counts

Environment Variables:
    SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD,
    SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA
"""

import os
import sys
import json
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_snowflake_connection():
    """Create Snowflake connection."""
    return snowflake.connector.connect(
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA')
    )


def load_hn_data():
    """Load HN job postings from parquet to Snowflake."""
    print("Loading HN data...")

    parquet_path = os.path.join(PROJECT_ROOT, "data/raw/hn_who_is_hiring.parquet")
    if not os.path.exists(parquet_path):
        print(f"  ✗ File not found: {parquet_path}")
        print("  Run: python extraction/fetch_hn_data.py")
        return

    df = pd.read_parquet(parquet_path)

    # Rename columns to match Snowflake table
    df = df.rename(columns={
        'by': 'author',
        'parent_id': 'thread_id'
    })

    # Select columns to match table schema
    columns = ['id', 'thread_id', 'thread_month', 'author', 'text', 'posted_at']
    df = df[[c for c in columns if c in df.columns]]

    # Uppercase column names (Snowflake convention)
    df.columns = [c.upper() for c in df.columns]

    print(f"  Records: {len(df):,}")

    conn = get_snowflake_connection()
    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE raw_hn_job_postings")

    success, num_chunks, num_rows, _ = write_pandas(
        conn, df, 'RAW_HN_JOB_POSTINGS',
        quote_identifiers=False
    )

    print(f"  ✓ Loaded {num_rows:,} rows to raw_hn_job_postings")

    cursor.close()
    conn.close()


def load_github_data():
    """Load GitHub repo stats from JSON to Snowflake."""
    print("Loading GitHub data...")

    json_path = os.path.join(PROJECT_ROOT, "data/raw/github_repo_stats.json")
    if not os.path.exists(json_path):
        print(f"  ✗ File not found: {json_path}")
        print("  Run: python extraction/fetch_github_data.py")
        return

    with open(json_path) as f:
        data = json.load(f)

    rows = []
    for repo in data['repos']:
        rows.append({
            'repo_name': repo['name'],
            'full_name': repo['full_name'],
            'category': repo.get('category', 'unknown'),
            'stars': repo['stars'],
            'forks': repo['forks'],
            'open_issues': repo['open_issues'],
            'watchers': repo['watchers'],
            'language': repo['language'],
            'description': repo['description'],
            'created_at': repo['created_at'],
            'updated_at': repo['updated_at'],
            'pushed_at': repo['pushed_at'],
            'fetched_at': data['fetched_at']
        })

    df = pd.DataFrame(rows)

    # Convert timestamps
    for col in ['created_at', 'updated_at', 'pushed_at', 'fetched_at']:
        ts = pd.to_datetime(df[col], utc=True)
        df[col] = ts.dt.strftime('%Y-%m-%d %H:%M:%S')

    df.columns = [c.upper() for c in df.columns]

    print(f"  Records: {len(df):,}")

    conn = get_snowflake_connection()
    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE raw_github_repo_stats")

    success, num_chunks, num_rows, _ = write_pandas(
        conn, df, 'RAW_GITHUB_REPO_STATS',
        quote_identifiers=False
    )

    print(f"  ✓ Loaded {num_rows:,} rows to raw_github_repo_stats")

    cursor.close()
    conn.close()


def load_linkedin_data():
    """Load LinkedIn job data from CSVs to Snowflake."""
    print("Loading LinkedIn data...")

    linkedin_dir = os.path.join(PROJECT_ROOT, "data/raw/linkedin")
    if not os.path.exists(linkedin_dir):
        print(f"  ✗ Directory not found: {linkedin_dir}")
        print("  Download LinkedIn data from Kaggle first.")
        return

    conn = get_snowflake_connection()
    cursor = conn.cursor()

    # Load job postings
    postings_path = os.path.join(linkedin_dir, "linkedin_job_postings.csv")
    if os.path.exists(postings_path):
        print("  Loading job postings...")
        df = pd.read_csv(postings_path, low_memory=False)

        columns_map = {
            'job_link': 'job_link',
            'last_processed_time': 'last_processed_time',
            'got_summary': 'got_summary',
            'got_ner': 'got_ner',
            'is_being_worked': 'is_being_worked',
            'job_title': 'job_title',
            'company': 'company',
            'job_location': 'job_location',
            'first_seen': 'first_seen',
            'search_city': 'search_city',
            'search_country': 'search_country',
            'search_position': 'search_position',
            'job_level': 'job_level',
            'job_type': 'job_type'
        }

        available_cols = [c for c in columns_map.keys() if c in df.columns]
        df = df[available_cols]

        for col in ['last_processed_time', 'first_seen']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        df.columns = [c.upper() for c in df.columns]

        print(f"    Records: {len(df):,}")

        cursor.execute("TRUNCATE TABLE raw_linkedin_postings")
        success, num_chunks, num_rows, _ = write_pandas(
            conn, df, 'RAW_LINKEDIN_POSTINGS',
            quote_identifiers=False
        )
        print(f"    ✓ Loaded {num_rows:,} rows to raw_linkedin_postings")
    else:
        print(f"  ✗ Job postings not found: {postings_path}")

    # Load skills
    skills_path = os.path.join(linkedin_dir, "job_skills.csv")
    if os.path.exists(skills_path):
        print("  Loading skills...")
        df = pd.read_csv(skills_path, low_memory=False)
        df.columns = [c.upper() for c in df.columns]

        print(f"    Records: {len(df):,}")

        cursor.execute("TRUNCATE TABLE raw_linkedin_skills")
        success, num_chunks, num_rows, _ = write_pandas(
            conn, df, 'RAW_LINKEDIN_SKILLS',
            quote_identifiers=False
        )
        print(f"    ✓ Loaded {num_rows:,} rows to raw_linkedin_skills")
    else:
        print(f"  ✗ Skills not found: {skills_path}")

    # Load summaries
    summary_path = os.path.join(linkedin_dir, "job_summary.csv")
    if os.path.exists(summary_path):
        print("  Loading summaries...")
        df = pd.read_csv(summary_path, low_memory=False)
        df.columns = [c.upper() for c in df.columns]

        print(f"    Records: {len(df):,}")

        cursor.execute("TRUNCATE TABLE raw_linkedin_summaries")
        success, num_chunks, num_rows, _ = write_pandas(
            conn, df, 'RAW_LINKEDIN_SUMMARIES',
            quote_identifiers=False
        )
        print(f"    ✓ Loaded {num_rows:,} rows to raw_linkedin_summaries")
    else:
        print(f"  ✗ Summaries not found: {summary_path}")

    cursor.close()
    conn.close()


def verify_loads():
    """Verify data was loaded correctly."""
    print("\nVerifying loads...")

    conn = get_snowflake_connection()
    cursor = conn.cursor()

    tables = [
        'raw_hn_job_postings',
        'raw_github_repo_stats',
        'raw_linkedin_postings',
        'raw_linkedin_skills',
        'raw_linkedin_summaries',
        'raw_llm_skill_extractions'
    ]

    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  {table}: {count:,} rows")
        except Exception as e:
            print(f"  {table}: (not found)")

    cursor.close()
    conn.close()


def run_load_all():
    """Load all data sources to Snowflake."""
    print("=" * 60)
    print("LOAD RAW DATA TO SNOWFLAKE")
    print("=" * 60)

    load_hn_data()
    load_github_data()
    load_linkedin_data()
    verify_loads()

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        source = sys.argv[1]
        if source == "hn":
            load_hn_data()
        elif source == "github":
            load_github_data()
        elif source == "linkedin":
            load_linkedin_data()
        elif source == "verify":
            verify_loads()
        else:
            print(f"Unknown source: {source}")
            print("Usage: python extraction/load_to_snowflake.py [hn|github|linkedin|verify]")
    else:
        run_load_all()
