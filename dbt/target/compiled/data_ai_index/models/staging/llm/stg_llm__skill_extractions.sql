with source as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY.raw_llm_skill_extractions
),

cleaned as (
    select
        posting_id,
        technologies,
        roles,
        extraction_method,
        model as llm_model,
        extracted_at,
        error,

        -- Derived fields
        array_size(technologies) as technology_count,
        array_size(roles) as role_count,
        error is null as is_successful

    from source
)

select * from cleaned