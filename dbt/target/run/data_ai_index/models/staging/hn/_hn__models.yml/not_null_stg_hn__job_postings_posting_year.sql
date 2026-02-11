
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select posting_year
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_hn__job_postings
where posting_year is null



  
  
      
    ) dbt_internal_test