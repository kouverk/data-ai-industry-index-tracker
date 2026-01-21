
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    role_name as unique_field,
    count(*) as n_records

from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.dim_roles
where role_name is not null
group by role_name
having count(*) > 1



  
  
      
    ) dbt_internal_test