
  
    

create or replace transient table DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.fct_hn_role_mentions
    
    
    
    as (with role_extracted as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_intermediate.int_hn__roles_extracted
),

dim_roles as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.dim_roles
)

select
    md5(cast(coalesce(cast(r.posting_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(r.role as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as mention_id,
    r.posting_id,
    dr.role_id,
    r.role as role_name,
    r.tier,
    r.posting_month,
    r.posting_year
from role_extracted r
left join dim_roles dr on r.role = dr.role_name
    )
;


  