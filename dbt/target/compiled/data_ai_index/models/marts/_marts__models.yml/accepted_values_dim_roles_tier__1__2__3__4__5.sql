
    
    

with all_values as (

    select
        tier as value_field,
        count(*) as n_records

    from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.dim_roles
    group by tier

)

select *
from all_values
where value_field not in (
    '1','2','3','4','5'
)


