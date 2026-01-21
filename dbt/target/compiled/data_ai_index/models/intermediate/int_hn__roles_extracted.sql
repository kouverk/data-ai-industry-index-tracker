

with postings as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_hn__job_postings
),

role_mappings as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY.role_mappings
),

-- Cross join postings with role mappings and check for matches
matched as (
    select
        p.posting_id,
        p.posting_month,
        p.posting_year,
        r.canonical_name as role,
        r.tier
    from postings p
    cross join role_mappings r
    where regexp_like(lower(p.posting_text), '\\b' || lower(r.keyword) || '\\b')
)

select distinct
    posting_id,
    posting_month,
    posting_year,
    role,
    tier
from matched