# Astronomer Runtime Dockerfile
# https://docs.astronomer.io/astro/runtime-image-architecture

FROM quay.io/astronomer/astro-runtime:12.1.0

# Install dbt and other dependencies
# (requirements.txt is automatically installed by Astro runtime)

# Copy extraction scripts to include directory
COPY include/extraction /usr/local/airflow/include/extraction

# Copy dbt project to include directory
COPY include/dbt /usr/local/airflow/include/dbt

# Set environment variables for script locations
ENV PROJECT_ROOT=/usr/local/airflow/include
ENV DBT_PROJECT_DIR=/usr/local/airflow/include/dbt
ENV DBT_PROFILES_DIR=/usr/local/airflow/include/dbt
ENV EXTRACTION_DIR=/usr/local/airflow/include/extraction
