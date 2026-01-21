
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    skill_name as unique_field,
    count(*) as n_records

from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.fct_linkedin_skill_counts
where skill_name is not null
group by skill_name
having count(*) > 1



  
  
      
    ) dbt_internal_test