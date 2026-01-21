
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select technology_id
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.dim_technologies
where technology_id is null



  
  
      
    ) dbt_internal_test