
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select repo_id
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.fct_github_repo_stats
where repo_id is null



  
  
      
    ) dbt_internal_test