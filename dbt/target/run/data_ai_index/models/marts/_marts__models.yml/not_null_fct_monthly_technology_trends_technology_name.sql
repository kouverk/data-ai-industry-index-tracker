
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select technology_name
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.fct_monthly_technology_trends
where technology_name is null



  
  
      
    ) dbt_internal_test