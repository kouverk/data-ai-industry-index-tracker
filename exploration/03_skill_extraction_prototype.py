"""
Skill & Role Extraction Prototype

This script tests the extraction logic using the taxonomy definitions.
Uses a mix of:
- Exact keyword matching (case-insensitive)
- Word boundary awareness for short keywords
"""

import pandas as pd
import re
from collections import Counter
import html

from taxonomy import ROLE_TAXONOMY, TECH_TAXONOMY, DATABASE_TAXONOMY

# =============================================================================
# EXTRACTION FUNCTIONS
# =============================================================================

def clean_html(text):
    """Clean HTML entities and tags from text."""
    if not text:
        return ""
    # Decode HTML entities (&#x2F; -> /, &amp; -> &, etc.)
    text = html.unescape(text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    return text


def extract_from_taxonomy(text, taxonomy):
    """
    Generic extraction function that works with any taxonomy.
    Returns list of canonical names found in text.
    """
    if not text:
        return []

    text_clean = clean_html(text)
    text_lower = text_clean.lower()
    found = []

    for name, config in taxonomy.items():
        keywords = config.get("keywords", [])
        variations = config.get("variations", [])
        require_boundary = config.get("require_word_boundary", False)

        # Check keywords
        for keyword in keywords:
            keyword_lower = keyword.lower()

            # For short keywords or those requiring boundaries, use regex
            if len(keyword_lower) <= 4 or require_boundary:
                pattern = r'\b' + re.escape(keyword_lower) + r'\b'
                if re.search(pattern, text_lower):
                    found.append(name)
                    break
            else:
                # For longer keywords, simple contains is fine
                if keyword_lower in text_lower:
                    found.append(name)
                    break
        else:
            # Check variations if no keyword matched
            for variation in variations:
                variation_lower = variation.lower()
                # Variations are typically abbreviations, use word boundary
                pattern = r'\b' + re.escape(variation_lower) + r'\b'
                if re.search(pattern, text_lower):
                    found.append(name)
                    break

    return list(set(found))


def extract_roles(text):
    """Extract roles from text using role taxonomy."""
    return extract_from_taxonomy(text, ROLE_TAXONOMY)


def extract_technologies(text):
    """Extract technologies from text using tech taxonomy."""
    return extract_from_taxonomy(text, TECH_TAXONOMY)


def extract_databases(text):
    """Extract databases from text using database taxonomy."""
    return extract_from_taxonomy(text, DATABASE_TAXONOMY)


def extract_all(text):
    """Extract all entities from text."""
    return {
        "roles": extract_roles(text),
        "technologies": extract_technologies(text),
        "databases": extract_databases(text),
    }


# =============================================================================
# MAIN - TEST ON HN DATA
# =============================================================================
if __name__ == "__main__":
    import os
    # Get project root (parent of exploration/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)

    print("Loading HN data...")
    df = pd.read_parquet("data/raw/hn_who_is_hiring.parquet")

    # Filter to 2018+ and posts with text
    df = df[df['posted_at'] >= '2018-01-01']
    df = df[df['text'].notna()]
    print(f"Loaded {len(df):,} posts from 2018+")

    # -------------------------------------------------------------------------
    # EXTRACT ROLES
    # -------------------------------------------------------------------------
    print("\n" + "="*60)
    print("ROLE EXTRACTION")
    print("="*60)

    df['roles'] = df['text'].apply(extract_roles)
    df['role_count'] = df['roles'].apply(len)

    all_roles = [role for roles in df['roles'] for role in roles]
    role_counts = Counter(all_roles)

    print(f"\nPosts with at least one role detected: {(df['role_count'] > 0).sum():,} ({(df['role_count'] > 0).mean()*100:.1f}%)")
    print("\nRole frequency (top 20):")
    for role, count in role_counts.most_common(20):
        pct = count / len(df) * 100
        print(f"  {role}: {count:,} ({pct:.1f}%)")

    # -------------------------------------------------------------------------
    # EXTRACT TECHNOLOGIES
    # -------------------------------------------------------------------------
    print("\n" + "="*60)
    print("TECHNOLOGY EXTRACTION")
    print("="*60)

    df['technologies'] = df['text'].apply(extract_technologies)
    df['tech_count'] = df['technologies'].apply(len)

    all_techs = [tech for techs in df['technologies'] for tech in techs]
    tech_counts = Counter(all_techs)

    print(f"\nPosts with at least one technology detected: {(df['tech_count'] > 0).sum():,} ({(df['tech_count'] > 0).mean()*100:.1f}%)")
    print(f"Average technologies per post: {df['tech_count'].mean():.1f}")

    print("\nTop 40 technologies:")
    for tech, count in tech_counts.most_common(40):
        pct = count / len(df) * 100
        print(f"  {tech}: {count:,} ({pct:.1f}%)")

    # -------------------------------------------------------------------------
    # EXTRACT DATABASES
    # -------------------------------------------------------------------------
    print("\n" + "="*60)
    print("DATABASE EXTRACTION")
    print("="*60)

    df['databases'] = df['text'].apply(extract_databases)
    df['db_count'] = df['databases'].apply(len)

    all_dbs = [db for dbs in df['databases'] for db in dbs]
    db_counts = Counter(all_dbs)

    print(f"\nPosts with at least one database detected: {(df['db_count'] > 0).sum():,} ({(df['db_count'] > 0).mean()*100:.1f}%)")

    print("\nTop 20 databases:")
    for db, count in db_counts.most_common(20):
        pct = count / len(df) * 100
        print(f"  {db}: {count:,} ({pct:.1f}%)")

    # -------------------------------------------------------------------------
    # TECHNOLOGY TRENDS OVER TIME
    # -------------------------------------------------------------------------
    print("\n" + "="*60)
    print("TECHNOLOGY TRENDS OVER TIME")
    print("="*60)

    # Modern data stack technologies
    tracked_techs = ['Snowflake', 'dbt', 'Airflow', 'Databricks', 'Spark',
                     'Kafka', 'Kubernetes', 'Docker', 'Terraform']

    print("\nModern Data Stack (% of posts):")
    print(f"{'Year':<6}", end="")
    for tech in tracked_techs:
        print(f"{tech:<12}", end="")
    print()

    for year in sorted(df['year'].unique()):
        year_df = df[df['year'] == year]
        print(f"{year:<6}", end="")
        for tech in tracked_techs:
            count = year_df['technologies'].apply(lambda x: tech in x).sum()
            pct = count / len(year_df) * 100
            print(f"{pct:>10.1f}%", end=" ")
        print()

    # AI/ML technologies
    print("\nAI/ML Technologies (% of posts):")
    ml_techs = ['PyTorch', 'TensorFlow', 'OpenAI', 'scikit-learn', 'Hugging Face']
    print(f"{'Year':<6}", end="")
    for tech in ml_techs:
        print(f"{tech:<14}", end="")
    print()

    for year in sorted(df['year'].unique()):
        year_df = df[df['year'] == year]
        print(f"{year:<6}", end="")
        for tech in ml_techs:
            count = year_df['technologies'].apply(lambda x: tech in x).sum()
            pct = count / len(year_df) * 100
            print(f"{pct:>12.1f}%", end=" ")
        print()

    # Legacy vs Modern
    print("\nLegacy vs Modern Warehouses (% of posts):")
    wh_techs = ['Teradata', 'Oracle Data Warehouse', 'Redshift', 'Snowflake', 'BigQuery', 'Databricks']
    print(f"{'Year':<6}", end="")
    for tech in wh_techs:
        short_name = tech[:10] if len(tech) > 10 else tech
        print(f"{short_name:<12}", end="")
    print()

    for year in sorted(df['year'].unique()):
        year_df = df[df['year'] == year]
        print(f"{year:<6}", end="")
        for tech in wh_techs:
            count = year_df['technologies'].apply(lambda x: tech in x).sum()
            pct = count / len(year_df) * 100
            print(f"{pct:>10.1f}%", end=" ")
        print()

    # -------------------------------------------------------------------------
    # SAMPLE EXTRACTIONS
    # -------------------------------------------------------------------------
    print("\n" + "="*60)
    print("SAMPLE EXTRACTIONS")
    print("="*60)

    de_posts = df[df['roles'].apply(lambda x: 'Data Engineer' in x)].sample(3)

    for idx, row in de_posts.iterrows():
        print(f"\n--- Post by {row['by']} ({row['thread_month']}) ---")
        print(f"Roles: {row['roles']}")
        print(f"Technologies: {row['technologies']}")
        print(f"Databases: {row['databases']}")
        print(f"Text snippet: {clean_html(row['text'])[:400]}...")

    # -------------------------------------------------------------------------
    # SAVE ENRICHED DATA
    # -------------------------------------------------------------------------
    print("\n" + "="*60)
    print("SAVING ENRICHED DATA")
    print("="*60)

    output_path = "data/processed/hn_with_extractions.parquet"
    df.to_parquet(output_path, index=False)
    print(f"\nEnriched data saved to: {output_path}")

    print("\n" + "="*60)
    print("DONE")
    print("="*60)
