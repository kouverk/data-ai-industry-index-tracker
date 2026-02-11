
    
    

with all_values as (

    select
        category as value_field,
        count(*) as n_records

    from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_github__repo_stats
    group by category

)

select *
from all_values
where value_field not in (
    'orchestration','transformation','warehouse','streaming','table_format','etl_elt','bi','ml_framework','llm','mlops','vector_db','data_quality','database','infrastructure'
)


