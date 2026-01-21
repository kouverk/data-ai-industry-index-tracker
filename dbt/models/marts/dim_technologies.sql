with tech_mappings as (
    select distinct
        canonical_name as technology_name,
        category,
        era
    from {{ ref('technology_mappings') }}
),

db_mappings as (
    select distinct
        canonical_name as technology_name,
        category,
        era
    from {{ ref('database_mappings') }}
),

combined as (
    select * from tech_mappings
    union all
    select * from db_mappings
)

select
    {{ dbt_utils.generate_surrogate_key(['technology_name']) }} as technology_id,
    technology_name,
    category,
    era,
    current_timestamp() as _created_at
from combined
