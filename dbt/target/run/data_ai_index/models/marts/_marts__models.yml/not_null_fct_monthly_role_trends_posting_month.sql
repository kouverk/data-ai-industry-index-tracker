
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select posting_month
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.fct_monthly_role_trends
where posting_month is null



  
  
      
    ) dbt_internal_test