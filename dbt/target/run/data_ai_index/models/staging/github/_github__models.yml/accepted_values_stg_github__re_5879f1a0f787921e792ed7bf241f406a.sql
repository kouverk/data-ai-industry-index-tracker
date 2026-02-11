
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

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
    'orchestration','transformation','warehouses','streaming','table_formats','etl_elt','bi','ml_classical','ml_deep','llm','mlops','vector_db','data_quality','data_catalog'
)



  
  
      
    ) dbt_internal_test