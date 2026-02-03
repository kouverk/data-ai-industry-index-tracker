
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        extraction_method as value_field,
        count(*) as n_records

    from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.fct_llm_technology_mentions
    group by extraction_method

)

select *
from all_values
where value_field not in (
    'llm'
)



  
  
      
    ) dbt_internal_test