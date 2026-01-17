"""
HN "Who Is Hiring" Data Exploration

This script downloads and explores the HuggingFace HN dataset to understand:
1. Data shape and volume
2. Field contents and quality
3. Time distribution
4. Sample job posting formats (for skill extraction prototyping)

Dataset structure:
- Each row is a monthly thread (e.g., "December 2025")
- The 'comments' column contains an array of job posting dicts with: by, id, text
- No timestamp per comment, but we have thread_month for time bucketing
"""

from datasets import load_dataset
import pandas as pd
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. LOAD THE DATA
# -----------------------------------------------------------------------------
print("Loading HN Who Is Hiring dataset from HuggingFace...")
dataset = load_dataset("brusic/hacker-news-who-is-hiring-posts")

# Convert to pandas for easier exploration
threads_df = dataset['train'].to_pandas()

print(f"\nDataset loaded: {len(threads_df):,} monthly threads")
print(f"Columns: {list(threads_df.columns)}")
print(f"\nThread months range: {threads_df['month'].iloc[-1]} to {threads_df['month'].iloc[0]}")

# -----------------------------------------------------------------------------
# 2. FLATTEN COMMENTS INTO JOB POSTS
# -----------------------------------------------------------------------------
print("\n" + "="*60)
print("FLATTENING COMMENTS INTO JOB POSTS")
print("="*60)

# Each thread has a 'comments' array - flatten into individual rows
all_posts = []
for _, thread in threads_df.iterrows():
    thread_month = thread['month']  # e.g., "December 2025"
    thread_type = thread['type']
    parent_id = thread['parent_id']

    for comment in thread['comments']:
        post = {
            'thread_month': thread_month,
            'thread_type': thread_type,
            'parent_id': parent_id,
            'id': comment.get('id'),
            'by': comment.get('by'),
            'text': comment.get('text'),
        }
        all_posts.append(post)

df = pd.DataFrame(all_posts)
print(f"\nFlattened to {len(df):,} individual job posts")

# -----------------------------------------------------------------------------
# 3. BASIC STATS
# -----------------------------------------------------------------------------
print("\n" + "="*60)
print("BASIC STATS")
print("="*60)

print(f"\nRow count: {len(df):,}")
print(f"\nColumn dtypes:\n{df.dtypes}")
print(f"\nNull counts:\n{df.isnull().sum()}")

# How many posts have text?
has_text = df['text'].notna().sum()
print(f"\nPosts with text: {has_text:,} ({has_text/len(df)*100:.1f}%)")

# -----------------------------------------------------------------------------
# 4. TIME DISTRIBUTION
# -----------------------------------------------------------------------------
print("\n" + "="*60)
print("TIME DISTRIBUTION")
print("="*60)

# Parse thread_month (e.g., "December 2025") into a proper date
df['posted_at'] = pd.to_datetime(df['thread_month'], format='%B %Y')
df['year'] = df['posted_at'].dt.year
df['year_month'] = df['posted_at'].dt.to_period('M')

print(f"\nDate range: {df['posted_at'].min()} to {df['posted_at'].max()}")

print("\nPosts per year:")
print(df.groupby('year').size().to_string())

# Focus on 2018+ (modern data stack era)
df_2018_plus = df[df['year'] >= 2018]
print(f"\nPosts from 2018+: {len(df_2018_plus):,} ({len(df_2018_plus)/len(df)*100:.1f}%)")

# -----------------------------------------------------------------------------
# 5. SAMPLE JOB POSTINGS
# -----------------------------------------------------------------------------
print("\n" + "="*60)
print("SAMPLE JOB POSTINGS (2024)")
print("="*60)

df_2024 = df[df['year'] == 2024].copy()
df_2024 = df_2024[df_2024['text'].notna()]  # Only posts with text
print(f"\n2024 posts with text: {len(df_2024):,}")

# Show a few random samples
for i in range(1, 4):
    print(f"\n--- Sample {i} ---")
    sample = df_2024.sample(1).iloc[0]
    print(f"Posted: {sample['posted_at']}")
    print(f"By: {sample['by']}")
    text = sample['text'] if sample['text'] else "[No text]"
    print(f"Text:\n{text[:1500]}{'...' if len(text) > 1500 else ''}")

# -----------------------------------------------------------------------------
# 6. TEXT LENGTH ANALYSIS
# -----------------------------------------------------------------------------
print("\n" + "="*60)
print("TEXT LENGTH ANALYSIS")
print("="*60)

df_with_text = df[df['text'].notna()].copy()
df_with_text['text_length'] = df_with_text['text'].str.len()
print(f"\nText length stats (for posts with text):")
print(df_with_text['text_length'].describe())

# -----------------------------------------------------------------------------
# 7. COMMON PATTERNS
# -----------------------------------------------------------------------------
print("\n" + "="*60)
print("COMMON PATTERNS IN JOB POSTS")
print("="*60)

# Check for common keywords to understand format
keywords = ['remote', 'onsite', 'hybrid', 'salary', 'equity',
            'python', 'sql', 'snowflake', 'dbt', 'airflow',
            'data engineer', 'machine learning', 'ai', 'llm']

df_2018_text = df_2018_plus[df_2018_plus['text'].notna()]
print(f"\nKeyword frequency (2018+ posts with text, n={len(df_2018_text):,}):")
for kw in keywords:
    count = df_2018_text['text'].str.lower().str.contains(kw, na=False).sum()
    pct = count / len(df_2018_text) * 100
    print(f"  {kw}: {count:,} ({pct:.1f}%)")

# -----------------------------------------------------------------------------
# 8. DATA ENGINEERING SPECIFIC
# -----------------------------------------------------------------------------
print("\n" + "="*60)
print("DATA ENGINEERING SPECIFIC POSTS")
print("="*60)

de_keywords = ['data engineer', 'analytics engineer', 'data scientist',
               'machine learning engineer', 'ml engineer', 'mlops',
               'data platform', 'data infrastructure']

de_pattern = '|'.join(de_keywords)
df_de = df_2018_text[df_2018_text['text'].str.lower().str.contains(de_pattern, na=False)]
print(f"\nPosts mentioning DE/ML roles: {len(df_de):,} ({len(df_de)/len(df_2018_text)*100:.1f}%)")

print("\nSample DE job post:")
if len(df_de) > 0:
    sample = df_de.sample(1).iloc[0]
    print(f"Posted: {sample['posted_at']}")
    print(f"Text:\n{sample['text'][:2000]}")

# -----------------------------------------------------------------------------
# 9. SAVE DATA
# -----------------------------------------------------------------------------
print("\n" + "="*60)
print("SAVING DATA")
print("="*60)

# Save flattened dataset locally for faster re-runs
output_path = "data/raw/hn_who_is_hiring.parquet"
df.to_parquet(output_path, index=False)
print(f"\nFull dataset saved to: {output_path}")

# Save a sample for manual review
sample_path = "data/raw/hn_sample_100.csv"
df_2024.sample(min(100, len(df_2024)))[['thread_month', 'posted_at', 'by', 'text']].to_csv(sample_path, index=False)
print(f"2024 sample (100 rows) saved to: {sample_path}")

print("\n" + "="*60)
print("DONE - Next step: Review samples and prototype skill extraction")
print("="*60)
