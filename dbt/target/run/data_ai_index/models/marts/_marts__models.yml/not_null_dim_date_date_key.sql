
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select date_key
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.dim_date
where date_key is null



  
  
      
    ) dbt_internal_test