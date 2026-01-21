{{
    config(
        materialized='table'
    )
}}

with postings as (
    select * from {{ ref('stg_hn__job_postings') }}
),

db_mappings as (
    select * from {{ ref('database_mappings') }}
),

-- Cross join postings with database mappings and check for matches
matched as (
    select
        p.posting_id,
        p.posting_month,
        p.posting_year,
        d.canonical_name as database_name,
        d.category,
        d.era
    from postings p
    cross join db_mappings d
    where regexp_like(lower(p.posting_text), '\\b' || lower(d.keyword) || '\\b')
)

select distinct
    posting_id,
    posting_month,
    posting_year,
    database_name,
    category,
    era
from matched
