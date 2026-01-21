
  
    

create or replace transient table DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.dim_technologies
    
    
    
    as (with tech_mappings as (
    select distinct
        canonical_name as technology_name,
        category,
        era
    from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY.technology_mappings
),

db_mappings as (
    select distinct
        canonical_name as technology_name,
        category,
        era
    from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY.database_mappings
),

combined as (
    select * from tech_mappings
    union all
    select * from db_mappings
)

select
    md5(cast(coalesce(cast(technology_name as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as technology_id,
    technology_name,
    category,
    era,
    current_timestamp() as _created_at
from combined
    )
;


  