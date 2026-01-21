with tech_extracted as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_intermediate.int_hn__technologies_extracted
),

db_extracted as (
    select
        posting_id,
        posting_month,
        posting_year,
        database_name as technology,
        category,
        era
    from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_intermediate.int_hn__databases_extracted
),

combined as (
    select * from tech_extracted
    union all
    select * from db_extracted
),

dim_tech as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.dim_technologies
)

select
    md5(cast(coalesce(cast(c.posting_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(c.technology as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as mention_id,
    c.posting_id,
    dt.technology_id,
    c.technology as technology_name,
    c.category,
    c.era,
    c.posting_month,
    c.posting_year
from combined c
left join dim_tech dt on c.technology = dt.technology_name