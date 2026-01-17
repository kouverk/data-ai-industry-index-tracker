"""
LinkedIn Jobs Data Exploration

This script explores the Kaggle LinkedIn dataset to understand:
1. Data shape and volume across all 3 files
2. Field contents and quality
3. Pre-extracted skills (this is the easy part!)
4. How to join the tables

PREREQUISITE: Download the dataset from Kaggle first:
  kaggle datasets download -d asaniczka/1-3m-linkedin-jobs-and-skills-2024
  unzip 1-3m-linkedin-jobs-and-skills-2024.zip -d data/raw/linkedin/

Or download manually from:
  https://www.kaggle.com/datasets/asaniczka/1-3m-linkedin-jobs-and-skills-2024
"""

import pandas as pd
from pathlib import Path
import sys

# -----------------------------------------------------------------------------
# 0. CHECK IF DATA EXISTS
# -----------------------------------------------------------------------------
DATA_DIR = Path("data/raw/linkedin")

# The Kaggle dataset has these files:
POSTINGS_FILE = DATA_DIR / "linkedin_job_postings.csv"
SKILLS_FILE = DATA_DIR / "job_skills.csv"
SUMMARY_FILE = DATA_DIR / "job_summary.csv"

if not POSTINGS_FILE.exists():
    print("="*60)
    print("LINKEDIN DATA NOT FOUND")
    print("="*60)
    print(f"\nExpected files in: {DATA_DIR.absolute()}")
    print(f"  - {POSTINGS_FILE.name}")
    print(f"  - {SKILLS_FILE.name}")
    print(f"  - {SUMMARY_FILE.name}")
    print("\nTo download:")
    print("  1. Install kaggle CLI: pip install kaggle")
    print("  2. Set up ~/.kaggle/kaggle.json with your API key")
    print("  3. Run:")
    print("     mkdir -p data/raw/linkedin")
    print("     cd data/raw/linkedin")
    print("     kaggle datasets download -d asaniczka/1-3m-linkedin-jobs-and-skills-2024")
    print("     unzip 1-3m-linkedin-jobs-and-skills-2024.zip")
    print("\nOr download manually from:")
    print("  https://www.kaggle.com/datasets/asaniczka/1-3m-linkedin-jobs-and-skills-2024")
    sys.exit(0)

# -----------------------------------------------------------------------------
# 1. LOAD THE DATA
# -----------------------------------------------------------------------------
print("Loading LinkedIn dataset from Kaggle...")

# Load with low_memory=False to avoid dtype warnings on large files
print(f"\nLoading {POSTINGS_FILE.name}...")
postings = pd.read_csv(POSTINGS_FILE, low_memory=False)
print(f"  Loaded: {len(postings):,} rows, {len(postings.columns)} columns")

print(f"\nLoading {SKILLS_FILE.name}...")
skills = pd.read_csv(SKILLS_FILE, low_memory=False)
print(f"  Loaded: {len(skills):,} rows, {len(skills.columns)} columns")

print(f"\nLoading {SUMMARY_FILE.name}...")
summary = pd.read_csv(SUMMARY_FILE, low_memory=False)
print(f"  Loaded: {len(summary):,} rows, {len(summary.columns)} columns")

# -----------------------------------------------------------------------------
# 2. POSTINGS TABLE - SCHEMA AND STATS
# -----------------------------------------------------------------------------
print("\n" + "="*60)
print("POSTINGS TABLE")
print("="*60)

print(f"\nColumns: {list(postings.columns)}")
print(f"\nColumn dtypes:\n{postings.dtypes}")
print(f"\nNull counts:\n{postings.isnull().sum()}")

print("\nSample row:")
print(postings.iloc[0].to_string())

# -----------------------------------------------------------------------------
# 3. SKILLS TABLE - THE GOOD STUFF
# -----------------------------------------------------------------------------
print("\n" + "="*60)
print("SKILLS TABLE (Pre-extracted skills!)")
print("="*60)

print(f"\nColumns: {list(skills.columns)}")
print(f"\nColumn dtypes:\n{skills.dtypes}")

print("\nSample rows:")
print(skills.head(20).to_string())

# How many skills per job?
skills_per_job = skills.groupby('job_link').size()
print(f"\nSkills per job posting:")
print(skills_per_job.describe())

# Most common skills
print("\nTop 30 most common skills:")
top_skills = skills['job_skills'].value_counts().head(30)
print(top_skills.to_string())

# -----------------------------------------------------------------------------
# 4. SUMMARY TABLE
# -----------------------------------------------------------------------------
print("\n" + "="*60)
print("SUMMARY TABLE")
print("="*60)

print(f"\nColumns: {list(summary.columns)}")
print(f"\nSample rows:")
print(summary.head(5).to_string())

# -----------------------------------------------------------------------------
# 5. JOIN ANALYSIS
# -----------------------------------------------------------------------------
print("\n" + "="*60)
print("JOIN ANALYSIS")
print("="*60)

# Check join keys
postings_jobs = set(postings['job_link'].unique())
skills_jobs = set(skills['job_link'].unique())
summary_jobs = set(summary['job_link'].unique())

print(f"\nUnique job_links in postings: {len(postings_jobs):,}")
print(f"Unique job_links in skills: {len(skills_jobs):,}")
print(f"Unique job_links in summary: {len(summary_jobs):,}")

print(f"\nJobs with skills: {len(postings_jobs & skills_jobs):,}")
print(f"Jobs without skills: {len(postings_jobs - skills_jobs):,}")

# -----------------------------------------------------------------------------
# 6. DATA ENGINEERING RELEVANT JOBS
# -----------------------------------------------------------------------------
print("\n" + "="*60)
print("DATA ENGINEERING RELEVANT JOBS")
print("="*60)

# Filter for DE-related titles
de_keywords = ['data engineer', 'analytics engineer', 'data scientist',
               'machine learning', 'ml engineer', 'data analyst',
               'etl', 'data architect', 'bi developer', 'bi engineer']

de_pattern = '|'.join(de_keywords)
de_jobs = postings[postings['job_title'].str.lower().str.contains(de_pattern, na=False)]

print(f"\nData/ML related jobs: {len(de_jobs):,} ({len(de_jobs)/len(postings)*100:.1f}%)")

print("\nTop job titles in this subset:")
print(de_jobs['job_title'].value_counts().head(20).to_string())

# Skills for DE jobs
de_job_links = set(de_jobs['job_link'])
de_skills = skills[skills['job_link'].isin(de_job_links)]

print("\nTop skills for Data/ML jobs:")
print(de_skills['job_skills'].value_counts().head(30).to_string())

# -----------------------------------------------------------------------------
# 7. SAVE SAMPLE FOR MANUAL REVIEW
# -----------------------------------------------------------------------------
print("\n" + "="*60)
print("SAVING SAMPLES")
print("="*60)

# Save DE jobs sample
sample_path = "data/raw/linkedin_de_jobs_sample.csv"
de_jobs.sample(min(500, len(de_jobs))).to_csv(sample_path, index=False)
print(f"DE jobs sample (500 rows) saved to: {sample_path}")

# Save top skills
skills_path = "data/raw/linkedin_top_skills.csv"
skills['job_skills'].value_counts().head(200).to_frame().to_csv(skills_path)
print(f"Top 200 skills saved to: {skills_path}")

print("\n" + "="*60)
print("DONE")
print("="*60)
print("\nKey findings:")
print("  - Skills are PRE-EXTRACTED (huge win, no NLP needed)")
print("  - ~1.3M jobs, millions of skill mentions")
print("  - Need to standardize skill names (canonical taxonomy)")
print("  - This is a single January 2024 snapshot (no time-series)")
