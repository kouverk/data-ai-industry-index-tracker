
  
    

create or replace transient table DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.dim_roles
    
    
    
    as (with role_mappings as (
    select distinct
        canonical_name as role_name,
        tier
    from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY.role_mappings
)

select
    md5(cast(coalesce(cast(role_name as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as role_id,
    role_name,
    tier,
    case tier
        when 1 then 'Core Data Roles'
        when 2 then 'Adjacent Data Roles'
        when 3 then 'AI/ML Specialized'
        when 4 then 'Historical/Legacy'
        when 5 then 'Overlapping Tech'
    end as tier_description,
    current_timestamp() as _created_at
from role_mappings
    )
;


  