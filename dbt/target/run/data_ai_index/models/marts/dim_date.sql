
  
    

create or replace transient table DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.dim_date
    
    
    
    as (

with date_spine as (
    





with rawdata as (

    

    

    with p as (
        select 0 as generated_number union all select 1
    ), unioned as (

    select

    
    p0.generated_number * power(2, 0)
     + 
    
    p1.generated_number * power(2, 1)
     + 
    
    p2.generated_number * power(2, 2)
     + 
    
    p3.generated_number * power(2, 3)
     + 
    
    p4.generated_number * power(2, 4)
     + 
    
    p5.generated_number * power(2, 5)
     + 
    
    p6.generated_number * power(2, 6)
     + 
    
    p7.generated_number * power(2, 7)
    
    
    + 1
    as generated_number

    from

    
    p as p0
     cross join 
    
    p as p1
     cross join 
    
    p as p2
     cross join 
    
    p as p3
     cross join 
    
    p as p4
     cross join 
    
    p as p5
     cross join 
    
    p as p6
     cross join 
    
    p as p7
    
    

    )

    select *
    from unioned
    where generated_number <= 191
    order by generated_number



),

all_periods as (

    select (
        

    dateadd(
        month,
        row_number() over (order by generated_number) - 1,
        cast('2011-01-01' as date)
        )


    ) as date_month
    from rawdata

),

filtered as (

    select *
    from all_periods
    where date_month <= cast('2026-12-01' as date)

)

select * from filtered


),

formatted as (
    select
        date_month as date_key,
        extract(year from date_month) as year,
        extract(month from date_month) as month,
        to_char(date_month, 'MMMM') as month_name,
        to_char(date_month, 'Mon') as month_short,
        to_char(date_month, 'YYYY-MM') as year_month,
        extract(quarter from date_month) as quarter,
        'Q' || extract(quarter from date_month) as quarter_name,
        case
            when extract(year from date_month) < 2015 then 'Hadoop Era'
            when extract(year from date_month) < 2020 then 'Cloud Transition'
            when extract(year from date_month) < 2023 then 'Modern Data Stack'
            else 'AI/LLM Era'
        end as data_era
    from date_spine
)

select * from formatted
    )
;


  