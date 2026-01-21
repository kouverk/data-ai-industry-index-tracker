

with postings as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_hn__job_postings
),

tech_mappings as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY.technology_mappings
),

-- Cross join postings with tech mappings and check for matches
-- Using CONTAINS for case-insensitive keyword matching (Snowflake doesn't support \b word boundaries)
matched as (
    select
        p.posting_id,
        p.posting_month,
        p.posting_year,
        t.canonical_name as technology,
        t.category,
        t.era
    from postings p
    cross join tech_mappings t
    where contains(lower(p.posting_text), lower(t.keyword))
)

select distinct
    posting_id,
    posting_month,
    posting_year,
    technology,
    category,
    era
from matched