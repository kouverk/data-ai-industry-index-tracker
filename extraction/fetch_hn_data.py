"""
Hacker News "Who Is Hiring" Data Extraction

Fetches HN job postings from HuggingFace dataset.
Saves to data/raw/hn_who_is_hiring.parquet for loading to Snowflake.

Usage:
    python extraction/fetch_hn_data.py

Data Source:
    HuggingFace: brusic/hacker-news-who-is-hiring-posts
    ~93K job postings from 2011-present
"""

import os
from datetime import datetime

from datasets import load_dataset
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def fetch_hn_data() -> pd.DataFrame:
    """
    Fetch HN Who Is Hiring posts from HuggingFace.

    Returns DataFrame with columns:
        - id: HN post ID
        - by: Author username
        - text: Job posting content
        - time: Unix timestamp
        - parent_id: Thread ID
        - thread_month: Thread month string (e.g., "April 2024")
    """
    print("Fetching HN data from HuggingFace...")

    # Load from HuggingFace
    dataset = load_dataset("brusic/hacker-news-who-is-hiring-posts", split="train")

    # Convert to DataFrame
    df = pd.DataFrame(dataset)

    print(f"  Raw records: {len(df):,}")

    # Parse timestamp
    df['posted_at'] = pd.to_datetime(df['time'], unit='s', utc=True)

    # Clean up columns
    df = df.rename(columns={
        'parent': 'parent_id'
    })

    # Select columns we need
    columns = ['id', 'by', 'text', 'time', 'parent_id', 'thread_month', 'posted_at']
    df = df[[c for c in columns if c in df.columns]]

    # Filter out empty posts
    df = df[df['text'].notna() & (df['text'].str.len() > 10)]

    print(f"  After filtering: {len(df):,}")

    return df


def save_to_parquet(df: pd.DataFrame, output_path: str):
    """Save DataFrame to parquet file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_parquet(output_path, index=False)
    print(f"\nSaved to: {output_path}")
    print(f"  File size: {os.path.getsize(output_path) / 1024 / 1024:.1f} MB")


def run_hn_extraction():
    """Main extraction function."""
    print("=" * 60)
    print("HN WHO IS HIRING DATA EXTRACTION")
    print("=" * 60)
    print(f"Started at: {datetime.now().isoformat()}")

    # Fetch data
    df = fetch_hn_data()

    # Summary stats
    print("\n" + "-" * 40)
    print("Summary:")
    print(f"  Total posts: {len(df):,}")
    print(f"  Date range: {df['posted_at'].min()} to {df['posted_at'].max()}")
    print(f"  Unique threads: {df['parent_id'].nunique():,}")

    # Year breakdown
    if 'posted_at' in df.columns:
        df['year'] = df['posted_at'].dt.year
        year_counts = df.groupby('year').size()
        print("\n  Posts by year:")
        for year, count in year_counts.items():
            print(f"    {year}: {count:,}")
        df = df.drop(columns=['year'])

    # Save to data/raw
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_path = os.path.join(project_root, "data/raw/hn_who_is_hiring.parquet")

    save_to_parquet(df, output_path)

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)

    return df


if __name__ == "__main__":
    run_hn_extraction()
