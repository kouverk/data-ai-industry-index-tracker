
    
    

with all_values as (

    select
        is_successful as value_field,
        count(*) as n_records

    from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_llm__skill_extractions
    group by is_successful

)

select *
from all_values
where value_field not in (
    'True','False'
)


