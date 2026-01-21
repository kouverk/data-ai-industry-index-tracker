with tech_extracted as (
    select * from {{ ref('int_hn__technologies_extracted') }}
),

db_extracted as (
    select
        posting_id,
        posting_month,
        posting_year,
        database_name as technology,
        category,
        era
    from {{ ref('int_hn__databases_extracted') }}
),

combined as (
    select * from tech_extracted
    union all
    select * from db_extracted
),

dim_tech as (
    select * from {{ ref('dim_technologies') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['c.posting_id', 'c.technology']) }} as mention_id,
    c.posting_id,
    dt.technology_id,
    c.technology as technology_name,
    c.category,
    c.era,
    c.posting_month,
    c.posting_year
from combined c
left join dim_tech dt on c.technology = dt.technology_name
