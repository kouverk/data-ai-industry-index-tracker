
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select posting_id
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_llm__skill_extractions
where posting_id is null



  
  
      
    ) dbt_internal_test