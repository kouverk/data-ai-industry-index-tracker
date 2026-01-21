{{ config(materialized='table') }}

with date_spine as (
    {{ dbt_utils.date_spine(
        datepart="month",
        start_date="cast('2011-01-01' as date)",
        end_date="cast('2026-12-01' as date)"
    ) }}
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
