{{
    config(
        materialized='table'
    )
}}

with postings as (
    select * from {{ ref('stg_hn__job_postings') }}
),

role_mappings as (
    select * from {{ ref('role_mappings') }}
),

-- Cross join postings with role mappings and check for matches
-- Using CONTAINS for case-insensitive keyword matching (Snowflake doesn't support \b word boundaries)
matched as (
    select
        p.posting_id,
        p.posting_month,
        p.posting_year,
        r.canonical_name as role,
        r.tier
    from postings p
    cross join role_mappings r
    where contains(lower(p.posting_text), lower(r.keyword))
)

select distinct
    posting_id,
    posting_month,
    posting_year,
    role,
    tier
from matched
