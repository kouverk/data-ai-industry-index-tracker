
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select thread_id
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_hn__job_postings
where thread_id is null



  
  
      
    ) dbt_internal_test