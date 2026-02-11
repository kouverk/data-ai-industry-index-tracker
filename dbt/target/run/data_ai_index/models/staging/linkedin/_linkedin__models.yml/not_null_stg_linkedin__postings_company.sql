
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select company
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_linkedin__postings
where company is null



  
  
      
    ) dbt_internal_test