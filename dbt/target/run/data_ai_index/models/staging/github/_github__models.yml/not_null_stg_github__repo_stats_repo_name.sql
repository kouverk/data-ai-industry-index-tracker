
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select repo_name
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_github__repo_stats
where repo_name is null



  
  
      
    ) dbt_internal_test