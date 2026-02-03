
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select is_successful
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_llm__skill_extractions
where is_successful is null



  
  
      
    ) dbt_internal_test