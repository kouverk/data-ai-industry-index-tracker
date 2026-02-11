
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select forks
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_github__repo_stats
where forks is null



  
  
      
    ) dbt_internal_test