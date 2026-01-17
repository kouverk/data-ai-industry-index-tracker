"""
Taxonomy Definitions for Data & AI Industry Index

This file contains the canonical taxonomies for:
1. Roles - Job titles in the data/AI ecosystem
2. Technologies - Tools, platforms, frameworks
3. Databases/Dialects - Database systems and SQL dialects

Historical coverage: 2011-2025 (covers Hadoop era through modern cloud/AI era)

Sources:
- Burtch Works: https://www.burtchworks.com/industry-insights/decoding-data-engineering-job-titles-and-specializations
- Teal HQ: https://www.tealhq.com/job-titles/data-engineer
- Airbyte: https://airbyte.com/blog/amazon-redshift-data-warehouse-evolution
- Databricks: https://www.databricks.com/discover/data-lakes/history
"""

# =============================================================================
# ROLE TAXONOMY
# =============================================================================
# Structure: "Canonical Name": {"keywords": [...], "variations": [...]}
# - keywords: exact phrases to match (case-insensitive)
# - variations: fuzzy matches, abbreviations (use carefully)

ROLE_TAXONOMY = {
    # -------------------------------------------------------------------------
    # TIER 1: Core Data Roles
    # -------------------------------------------------------------------------
    "Data Engineer": {
        "keywords": [
            "data engineer",
            "data engineering",
            "data pipeline engineer",
            "etl engineer",
            "elt engineer",
        ],
        "variations": [],
        "tier": 1,
    },
    "Analytics Engineer": {
        "keywords": [
            "analytics engineer",
            "analytics engineering",
        ],
        "variations": [],
        "tier": 1,
    },
    "Data Analyst": {
        "keywords": [
            "data analyst",
            "business analyst",
            "reporting analyst",
            "insights analyst",
            "analytics analyst",
        ],
        "variations": [],
        "tier": 1,
    },
    "Data Scientist": {
        "keywords": [
            "data scientist",
            "data science",
            "applied scientist",
        ],
        "variations": [],
        "tier": 1,
    },
    "Data Architect": {
        "keywords": [
            "data architect",
            "enterprise data architect",
            "solution architect, data",
        ],
        "variations": [],
        "tier": 1,
    },

    # -------------------------------------------------------------------------
    # TIER 2: Adjacent Data Roles
    # -------------------------------------------------------------------------
    "Machine Learning Engineer": {
        "keywords": [
            "machine learning engineer",
            "ml engineer",
            "applied ml engineer",
        ],
        "variations": ["mle"],
        "tier": 2,
    },
    "MLOps Engineer": {
        "keywords": [
            "mlops engineer",
            "mlops",
            "ml ops engineer",
            "machine learning operations",
        ],
        "variations": [],
        "tier": 2,
    },
    "Data Platform Engineer": {
        "keywords": [
            "data platform engineer",
            "data infrastructure engineer",
        ],
        "variations": [],
        "tier": 2,
    },
    "BI Engineer": {
        "keywords": [
            "bi engineer",
            "bi developer",
            "business intelligence engineer",
            "business intelligence developer",
            "bi analyst",
        ],
        "variations": [],
        "tier": 2,
    },
    "ETL Developer": {
        "keywords": [
            "etl developer",
            "integration developer",
            "data integration developer",
        ],
        "variations": [],
        "tier": 2,
    },
    "Database Administrator": {
        "keywords": [
            "database administrator",
            "database admin",
            "db administrator",
        ],
        "variations": ["dba"],
        "tier": 2,
    },
    "Data Warehouse Engineer": {
        "keywords": [
            "data warehouse engineer",
            "data warehousing engineer",
            "dwh engineer",
            "warehouse engineer",
        ],
        "variations": [],
        "tier": 2,
    },

    # -------------------------------------------------------------------------
    # TIER 3: AI/ML Specialized Roles
    # -------------------------------------------------------------------------
    "AI Engineer": {
        "keywords": [
            "ai engineer",
            "artificial intelligence engineer",
            "genai engineer",
            "generative ai engineer",
        ],
        "variations": [],
        "tier": 3,
    },
    "NLP Engineer": {
        "keywords": [
            "nlp engineer",
            "natural language processing engineer",
            "computational linguist",
        ],
        "variations": [],
        "tier": 3,
    },
    "Computer Vision Engineer": {
        "keywords": [
            "computer vision engineer",
            "cv engineer",
            "image processing engineer",
        ],
        "variations": [],
        "tier": 3,
    },
    "Research Scientist": {
        "keywords": [
            "research scientist",
            "ml researcher",
            "ai researcher",
            "machine learning researcher",
            "research engineer",
        ],
        "variations": [],
        "tier": 3,
    },
    "Deep Learning Engineer": {
        "keywords": [
            "deep learning engineer",
            "neural network engineer",
        ],
        "variations": [],
        "tier": 3,
    },
    "LLM Engineer": {
        "keywords": [
            "llm engineer",
            "large language model engineer",
            "prompt engineer",
        ],
        "variations": [],
        "tier": 3,
    },

    # -------------------------------------------------------------------------
    # TIER 4: Historical / Legacy Roles (pre-2015 common)
    # -------------------------------------------------------------------------
    "Hadoop Developer": {
        "keywords": [
            "hadoop developer",
            "hadoop engineer",
            "big data developer",
            "big data engineer",
        ],
        "variations": [],
        "tier": 4,
    },
    "Statistician": {
        "keywords": [
            "statistician",
            "statistical analyst",
            "biostatistician",
        ],
        "variations": [],
        "tier": 4,
    },
    "Quantitative Analyst": {
        "keywords": [
            "quantitative analyst",
            "quant analyst",
            "quantitative developer",
            "quant developer",
        ],
        "variations": ["quant"],
        "tier": 4,
    },
    "Report Developer": {
        "keywords": [
            "report developer",
            "report writer",
            "ssrs developer",
            "crystal reports developer",
        ],
        "variations": [],
        "tier": 4,
    },

    # -------------------------------------------------------------------------
    # TIER 5: Overlapping / Adjacent Tech Roles
    # -------------------------------------------------------------------------
    "Software Engineer": {
        "keywords": [
            "software engineer",
            "software developer",
            "swe",
        ],
        "variations": [],
        "tier": 5,
    },
    "Backend Engineer": {
        "keywords": [
            "backend engineer",
            "back-end engineer",
            "back end engineer",
            "backend developer",
        ],
        "variations": [],
        "tier": 5,
    },
    "Site Reliability Engineer": {
        "keywords": [
            "site reliability engineer",
            "sre",
            "reliability engineer",
        ],
        "variations": [],
        "tier": 5,
    },
    "DevOps Engineer": {
        "keywords": [
            "devops engineer",
            "devops",
            "infrastructure engineer",
        ],
        "variations": [],
        "tier": 5,
    },
    "Solutions Architect": {
        "keywords": [
            "solutions architect",
            "solution architect",
            "technical architect",
        ],
        "variations": [],
        "tier": 5,
    },
}


# =============================================================================
# TECHNOLOGY TAXONOMY
# =============================================================================
# Structure: "Canonical Name": {"keywords": [...], "category": "...", "era": "..."}
# - era: "legacy" (pre-2015), "modern" (2015-2020), "current" (2020+)

TECH_TAXONOMY = {
    # -------------------------------------------------------------------------
    # ORCHESTRATION / WORKFLOW
    # -------------------------------------------------------------------------
    "Airflow": {
        "keywords": ["airflow", "apache airflow"],
        "category": "orchestration",
        "era": "modern",
    },
    "Dagster": {
        "keywords": ["dagster"],
        "category": "orchestration",
        "era": "current",
    },
    "Prefect": {
        "keywords": ["prefect"],
        "category": "orchestration",
        "era": "current",
    },
    "Luigi": {
        "keywords": ["luigi", "spotify luigi"],
        "category": "orchestration",
        "era": "modern",
    },
    "Argo": {
        "keywords": ["argo workflows", "argo-workflows"],
        "category": "orchestration",
        "era": "modern",
    },
    "Oozie": {
        "keywords": ["oozie", "apache oozie"],
        "category": "orchestration",
        "era": "legacy",
    },
    "Azkaban": {
        "keywords": ["azkaban"],
        "category": "orchestration",
        "era": "legacy",
    },
    "Control-M": {
        "keywords": ["control-m", "controlm"],
        "category": "orchestration",
        "era": "legacy",
    },
    "Autosys": {
        "keywords": ["autosys", "ca autosys"],
        "category": "orchestration",
        "era": "legacy",
    },
    "Mage": {
        "keywords": ["mage.ai", "mage-ai"],
        "category": "orchestration",
        "era": "current",
    },
    "Temporal": {
        "keywords": ["temporal.io", "temporal workflow"],
        "category": "orchestration",
        "era": "current",
    },
    "Kestra": {
        "keywords": ["kestra"],
        "category": "orchestration",
        "era": "current",
    },

    # -------------------------------------------------------------------------
    # TRANSFORMATION / PROCESSING
    # -------------------------------------------------------------------------
    "dbt": {
        "keywords": ["dbt", "data build tool", "dbt-core", "dbt cloud"],
        "category": "transformation",
        "era": "modern",
    },
    "Spark": {
        "keywords": ["spark", "pyspark", "apache spark", "spark sql", "databricks spark"],
        "category": "transformation",
        "era": "modern",
    },
    "pandas": {
        "keywords": ["pandas"],
        "category": "transformation",
        "era": "modern",
    },
    "Polars": {
        "keywords": ["polars"],
        "category": "transformation",
        "era": "current",
    },
    "Dask": {
        "keywords": ["dask"],
        "category": "transformation",
        "era": "modern",
    },
    "Hadoop MapReduce": {
        "keywords": ["mapreduce", "map-reduce", "hadoop mapreduce"],
        "category": "transformation",
        "era": "legacy",
    },
    "Pig": {
        "keywords": ["pig", "apache pig", "pig latin"],
        "category": "transformation",
        "era": "legacy",
    },
    "Hive": {
        "keywords": ["hive", "apache hive", "hiveql"],
        "category": "transformation",
        "era": "legacy",
    },
    "Presto": {
        "keywords": ["presto", "prestodb", "presto sql"],
        "category": "transformation",
        "era": "modern",
    },
    "Trino": {
        "keywords": ["trino"],
        "category": "transformation",
        "era": "current",
    },
    "Ray": {
        "keywords": ["ray.io", "anyscale ray"],
        "category": "transformation",
        "era": "current",
    },

    # -------------------------------------------------------------------------
    # DATA WAREHOUSES - CLOUD
    # -------------------------------------------------------------------------
    "Snowflake": {
        "keywords": ["snowflake"],
        "category": "warehouse_cloud",
        "era": "modern",
    },
    "BigQuery": {
        "keywords": ["bigquery", "big query", "google bigquery"],
        "category": "warehouse_cloud",
        "era": "modern",
    },
    "Redshift": {
        "keywords": ["redshift", "aws redshift", "amazon redshift"],
        "category": "warehouse_cloud",
        "era": "modern",
    },
    "Databricks": {
        "keywords": ["databricks", "databricks sql"],
        "category": "warehouse_cloud",
        "era": "modern",
    },
    "Azure Synapse": {
        "keywords": ["azure synapse", "synapse analytics", "azure sql data warehouse"],
        "category": "warehouse_cloud",
        "era": "modern",
    },
    "ClickHouse": {
        "keywords": ["clickhouse"],
        "category": "warehouse_cloud",
        "era": "modern",
    },
    "DuckDB": {
        "keywords": ["duckdb"],
        "category": "warehouse_cloud",
        "era": "current",
    },
    "Firebolt": {
        "keywords": ["firebolt"],
        "category": "warehouse_cloud",
        "era": "current",
    },
    "MotherDuck": {
        "keywords": ["motherduck"],
        "category": "warehouse_cloud",
        "era": "current",
    },

    # -------------------------------------------------------------------------
    # DATA WAREHOUSES - ON-PREM / LEGACY
    # -------------------------------------------------------------------------
    "Teradata": {
        "keywords": ["teradata"],
        "category": "warehouse_legacy",
        "era": "legacy",
    },
    "Oracle Data Warehouse": {
        "keywords": ["oracle data warehouse", "oracle dw", "oracle exadata", "oracle autonomous"],
        "category": "warehouse_legacy",
        "era": "legacy",
    },
    "Netezza": {
        "keywords": ["netezza", "ibm netezza"],
        "category": "warehouse_legacy",
        "era": "legacy",
    },
    "Greenplum": {
        "keywords": ["greenplum"],
        "category": "warehouse_legacy",
        "era": "legacy",
    },
    "Vertica": {
        "keywords": ["vertica", "hp vertica"],
        "category": "warehouse_legacy",
        "era": "legacy",
    },
    "IBM Db2 Warehouse": {
        "keywords": ["db2 warehouse", "db2 analytics", "ibm db2"],
        "category": "warehouse_legacy",
        "era": "legacy",
    },
    "SAP BW": {
        "keywords": ["sap bw", "sap business warehouse", "sap hana"],
        "category": "warehouse_legacy",
        "era": "legacy",
    },

    # -------------------------------------------------------------------------
    # STREAMING / REAL-TIME
    # -------------------------------------------------------------------------
    "Kafka": {
        "keywords": ["kafka", "apache kafka", "confluent"],
        "category": "streaming",
        "era": "modern",
    },
    "Flink": {
        "keywords": ["flink", "apache flink"],
        "category": "streaming",
        "era": "modern",
    },
    "Kinesis": {
        "keywords": ["kinesis", "aws kinesis", "kinesis streams", "kinesis firehose"],
        "category": "streaming",
        "era": "modern",
    },
    "Pulsar": {
        "keywords": ["pulsar", "apache pulsar"],
        "category": "streaming",
        "era": "modern",
    },
    "Spark Streaming": {
        "keywords": ["spark streaming", "structured streaming"],
        "category": "streaming",
        "era": "modern",
    },
    "Storm": {
        "keywords": ["storm", "apache storm"],
        "category": "streaming",
        "era": "legacy",
    },
    "Samza": {
        "keywords": ["samza", "apache samza"],
        "category": "streaming",
        "era": "legacy",
    },
    "RabbitMQ": {
        "keywords": ["rabbitmq"],
        "category": "streaming",
        "era": "modern",
    },
    "Redis Streams": {
        "keywords": ["redis streams"],
        "category": "streaming",
        "era": "modern",
    },
    "Google Pub/Sub": {
        "keywords": ["pub/sub", "pubsub", "google pubsub"],
        "category": "streaming",
        "era": "modern",
    },
    "Amazon MSK": {
        "keywords": ["amazon msk", "aws msk"],
        "category": "streaming",
        "era": "modern",
    },

    # -------------------------------------------------------------------------
    # TABLE FORMATS / DATA LAKE
    # -------------------------------------------------------------------------
    "Delta Lake": {
        "keywords": ["delta lake", "delta.io", "delta table"],
        "category": "table_format",
        "era": "current",
    },
    "Apache Iceberg": {
        "keywords": ["iceberg", "apache iceberg"],
        "category": "table_format",
        "era": "current",
    },
    "Apache Hudi": {
        "keywords": ["hudi", "apache hudi"],
        "category": "table_format",
        "era": "current",
    },
    "Parquet": {
        "keywords": ["parquet", "apache parquet"],
        "category": "table_format",
        "era": "modern",
    },
    "ORC": {
        "keywords": ["orc", "apache orc", "optimized row columnar"],
        "category": "table_format",
        "era": "legacy",
    },
    "Avro": {
        "keywords": ["avro", "apache avro"],
        "category": "table_format",
        "era": "legacy",
    },

    # -------------------------------------------------------------------------
    # CLOUD STORAGE
    # -------------------------------------------------------------------------
    "S3": {
        "keywords": ["s3", "aws s3", "amazon s3"],
        "category": "cloud_storage",
        "era": "modern",
    },
    "GCS": {
        "keywords": ["gcs", "google cloud storage"],
        "category": "cloud_storage",
        "era": "modern",
    },
    "Azure Blob": {
        "keywords": ["azure blob", "blob storage", "azure storage"],
        "category": "cloud_storage",
        "era": "modern",
    },
    "HDFS": {
        "keywords": ["hdfs", "hadoop distributed file system"],
        "category": "cloud_storage",
        "era": "legacy",
    },

    # -------------------------------------------------------------------------
    # ETL / ELT / DATA INTEGRATION
    # -------------------------------------------------------------------------
    "Fivetran": {
        "keywords": ["fivetran"],
        "category": "etl_elt",
        "era": "modern",
    },
    "Airbyte": {
        "keywords": ["airbyte"],
        "category": "etl_elt",
        "era": "current",
    },
    "Stitch": {
        "keywords": ["stitch", "stitch data"],
        "category": "etl_elt",
        "era": "modern",
    },
    "AWS Glue": {
        "keywords": ["aws glue", "glue etl", "glue catalog"],
        "category": "etl_elt",
        "era": "modern",
    },
    "Matillion": {
        "keywords": ["matillion"],
        "category": "etl_elt",
        "era": "modern",
    },
    "Informatica": {
        "keywords": ["informatica", "informatica powercenter", "informatica cloud"],
        "category": "etl_elt",
        "era": "legacy",
    },
    "Talend": {
        "keywords": ["talend"],
        "category": "etl_elt",
        "era": "legacy",
    },
    "SSIS": {
        "keywords": ["ssis", "sql server integration services"],
        "category": "etl_elt",
        "era": "legacy",
    },
    "DataStage": {
        "keywords": ["datastage", "ibm datastage"],
        "category": "etl_elt",
        "era": "legacy",
    },
    "Pentaho": {
        "keywords": ["pentaho", "pentaho data integration", "kettle"],
        "category": "etl_elt",
        "era": "legacy",
    },
    "dlt": {
        "keywords": ["dlt", "data load tool"],
        "category": "etl_elt",
        "era": "current",
    },
    "Meltano": {
        "keywords": ["meltano"],
        "category": "etl_elt",
        "era": "current",
    },

    # -------------------------------------------------------------------------
    # BI / VISUALIZATION
    # -------------------------------------------------------------------------
    "Tableau": {
        "keywords": ["tableau"],
        "category": "bi",
        "era": "modern",
    },
    "Looker": {
        "keywords": ["looker", "lookml"],
        "category": "bi",
        "era": "modern",
    },
    "Power BI": {
        "keywords": ["power bi", "powerbi"],
        "category": "bi",
        "era": "modern",
    },
    "Metabase": {
        "keywords": ["metabase"],
        "category": "bi",
        "era": "modern",
    },
    "Superset": {
        "keywords": ["superset", "apache superset"],
        "category": "bi",
        "era": "modern",
    },
    "Mode": {
        "keywords": ["mode analytics"],
        "category": "bi",
        "era": "modern",
    },
    "Sisense": {
        "keywords": ["sisense"],
        "category": "bi",
        "era": "modern",
    },
    "Qlik": {
        "keywords": ["qlik", "qlikview", "qliksense"],
        "category": "bi",
        "era": "legacy",
    },
    "MicroStrategy": {
        "keywords": ["microstrategy"],
        "category": "bi",
        "era": "legacy",
    },
    "Cognos": {
        "keywords": ["cognos", "ibm cognos"],
        "category": "bi",
        "era": "legacy",
    },
    "Business Objects": {
        "keywords": ["business objects", "sap businessobjects", "sap bo"],
        "category": "bi",
        "era": "legacy",
    },
    "SSRS": {
        "keywords": ["ssrs", "sql server reporting services"],
        "category": "bi",
        "era": "legacy",
    },
    "Crystal Reports": {
        "keywords": ["crystal reports"],
        "category": "bi",
        "era": "legacy",
    },
    "ThoughtSpot": {
        "keywords": ["thoughtspot"],
        "category": "bi",
        "era": "current",
    },
    "Hex": {
        "keywords": ["hex.tech"],
        "category": "bi",
        "era": "current",
    },
    "Lightdash": {
        "keywords": ["lightdash"],
        "category": "bi",
        "era": "current",
    },

    # -------------------------------------------------------------------------
    # ML FRAMEWORKS - CLASSICAL
    # -------------------------------------------------------------------------
    "scikit-learn": {
        "keywords": ["scikit-learn", "sklearn", "scikit learn"],
        "category": "ml_classical",
        "era": "modern",
    },
    "XGBoost": {
        "keywords": ["xgboost"],
        "category": "ml_classical",
        "era": "modern",
    },
    "LightGBM": {
        "keywords": ["lightgbm"],
        "category": "ml_classical",
        "era": "modern",
    },
    "CatBoost": {
        "keywords": ["catboost"],
        "category": "ml_classical",
        "era": "modern",
    },
    "SAS": {
        "keywords": ["sas", "sas enterprise"],
        "category": "ml_classical",
        "era": "legacy",
    },
    "SPSS": {
        "keywords": ["spss", "ibm spss"],
        "category": "ml_classical",
        "era": "legacy",
    },
    "Stata": {
        "keywords": ["stata"],
        "category": "ml_classical",
        "era": "legacy",
    },

    # -------------------------------------------------------------------------
    # ML FRAMEWORKS - DEEP LEARNING
    # -------------------------------------------------------------------------
    "PyTorch": {
        "keywords": ["pytorch"],
        "category": "ml_deep",
        "era": "modern",
    },
    "TensorFlow": {
        "keywords": ["tensorflow"],
        "category": "ml_deep",
        "era": "modern",
    },
    "Keras": {
        "keywords": ["keras"],
        "category": "ml_deep",
        "era": "modern",
    },
    "JAX": {
        "keywords": ["jax", "google jax"],
        "category": "ml_deep",
        "era": "current",
    },
    "Theano": {
        "keywords": ["theano"],
        "category": "ml_deep",
        "era": "legacy",
    },
    "Caffe": {
        "keywords": ["caffe", "caffe2"],
        "category": "ml_deep",
        "era": "legacy",
    },
    "MXNet": {
        "keywords": ["mxnet", "apache mxnet"],
        "category": "ml_deep",
        "era": "legacy",
    },

    # -------------------------------------------------------------------------
    # LLMS & GENAI
    # -------------------------------------------------------------------------
    "OpenAI": {
        "keywords": ["openai", "gpt-4", "gpt-3", "chatgpt", "gpt-4o", "gpt-3.5"],
        "category": "llm",
        "era": "current",
    },
    "Claude": {
        "keywords": ["claude", "anthropic claude"],
        "category": "llm",
        "era": "current",
    },
    "Llama": {
        "keywords": ["llama", "llama2", "llama 2", "llama3", "meta llama"],
        "category": "llm",
        "era": "current",
    },
    "Mistral": {
        "keywords": ["mistral", "mistral ai", "mixtral"],
        "category": "llm",
        "era": "current",
    },
    "Gemini": {
        "keywords": ["gemini", "google gemini"],
        "category": "llm",
        "era": "current",
    },
    "LangChain": {
        "keywords": ["langchain"],
        "category": "llm",
        "era": "current",
    },
    "LlamaIndex": {
        "keywords": ["llamaindex", "llama index"],
        "category": "llm",
        "era": "current",
    },
    "Hugging Face": {
        "keywords": ["hugging face", "huggingface", "transformers library"],
        "category": "llm",
        "era": "current",
    },
    "Ollama": {
        "keywords": ["ollama"],
        "category": "llm",
        "era": "current",
    },
    "vLLM": {
        "keywords": ["vllm"],
        "category": "llm",
        "era": "current",
    },
    "Cohere": {
        "keywords": ["cohere"],
        "category": "llm",
        "era": "current",
    },

    # -------------------------------------------------------------------------
    # MLOPS / ML PLATFORMS
    # -------------------------------------------------------------------------
    "MLflow": {
        "keywords": ["mlflow"],
        "category": "mlops",
        "era": "modern",
    },
    "Kubeflow": {
        "keywords": ["kubeflow"],
        "category": "mlops",
        "era": "modern",
    },
    "Weights & Biases": {
        "keywords": ["weights & biases", "wandb", "w&b"],
        "category": "mlops",
        "era": "modern",
    },
    "SageMaker": {
        "keywords": ["sagemaker", "aws sagemaker", "amazon sagemaker"],
        "category": "mlops",
        "era": "modern",
    },
    "Vertex AI": {
        "keywords": ["vertex ai", "google vertex"],
        "category": "mlops",
        "era": "current",
    },
    "Azure ML": {
        "keywords": ["azure ml", "azure machine learning"],
        "category": "mlops",
        "era": "modern",
    },
    "Databricks MLflow": {
        "keywords": ["databricks mlflow"],
        "category": "mlops",
        "era": "modern",
    },
    "Neptune.ai": {
        "keywords": ["neptune.ai", "neptune ai"],
        "category": "mlops",
        "era": "modern",
    },
    "Comet ML": {
        "keywords": ["comet ml", "comet.ml"],
        "category": "mlops",
        "era": "modern",
    },
    "DVC": {
        "keywords": ["dvc", "data version control"],
        "category": "mlops",
        "era": "modern",
    },
    "BentoML": {
        "keywords": ["bentoml"],
        "category": "mlops",
        "era": "current",
    },
    "Modal": {
        "keywords": ["modal.com"],
        "category": "mlops",
        "era": "current",
    },

    # -------------------------------------------------------------------------
    # VECTOR DATABASES
    # -------------------------------------------------------------------------
    "Pinecone": {
        "keywords": ["pinecone"],
        "category": "vector_db",
        "era": "current",
    },
    "Weaviate": {
        "keywords": ["weaviate"],
        "category": "vector_db",
        "era": "current",
    },
    "Chroma": {
        "keywords": ["chroma", "chromadb"],
        "category": "vector_db",
        "era": "current",
    },
    "pgvector": {
        "keywords": ["pgvector"],
        "category": "vector_db",
        "era": "current",
    },
    "Milvus": {
        "keywords": ["milvus"],
        "category": "vector_db",
        "era": "current",
    },
    "Qdrant": {
        "keywords": ["qdrant"],
        "category": "vector_db",
        "era": "current",
    },
    "FAISS": {
        "keywords": ["faiss"],
        "category": "vector_db",
        "era": "modern",
    },

    # -------------------------------------------------------------------------
    # PROGRAMMING LANGUAGES
    # -------------------------------------------------------------------------
    "Python": {
        "keywords": ["python"],
        "category": "language",
        "era": "modern",
    },
    "SQL": {
        "keywords": ["sql"],
        "category": "language",
        "era": "legacy",
    },
    "Scala": {
        "keywords": ["scala"],
        "category": "language",
        "era": "modern",
    },
    "Java": {
        "keywords": ["java"],
        "category": "language",
        "era": "legacy",
        "require_word_boundary": True,  # Avoid matching "javascript"
    },
    "Go": {
        "keywords": ["golang"],  # Only match "golang" to avoid false positives
        "category": "language",
        "era": "modern",
    },
    "Rust": {
        "keywords": ["rust"],
        "category": "language",
        "era": "current",
        "require_word_boundary": True,
    },
    "R": {
        "keywords": ["r programming", "rstats", "r language"],
        "category": "language",
        "era": "legacy",
    },
    "Julia": {
        "keywords": ["julia lang", "julialang"],
        "category": "language",
        "era": "current",
    },
    "C++": {
        "keywords": ["c++"],
        "category": "language",
        "era": "legacy",
    },
    "Perl": {
        "keywords": ["perl"],
        "category": "language",
        "era": "legacy",
    },

    # -------------------------------------------------------------------------
    # INFRASTRUCTURE / DEVOPS
    # -------------------------------------------------------------------------
    "Kubernetes": {
        "keywords": ["kubernetes", "k8s"],
        "category": "infrastructure",
        "era": "modern",
    },
    "Docker": {
        "keywords": ["docker"],
        "category": "infrastructure",
        "era": "modern",
    },
    "Terraform": {
        "keywords": ["terraform"],
        "category": "infrastructure",
        "era": "modern",
    },
    "Ansible": {
        "keywords": ["ansible"],
        "category": "infrastructure",
        "era": "modern",
    },
    "Helm": {
        "keywords": ["helm"],
        "category": "infrastructure",
        "era": "modern",
    },
    "Pulumi": {
        "keywords": ["pulumi"],
        "category": "infrastructure",
        "era": "current",
    },

    # -------------------------------------------------------------------------
    # CLOUD PROVIDERS
    # -------------------------------------------------------------------------
    "AWS": {
        "keywords": ["aws", "amazon web services"],
        "category": "cloud",
        "era": "modern",
    },
    "GCP": {
        "keywords": ["gcp", "google cloud platform", "google cloud"],
        "category": "cloud",
        "era": "modern",
    },
    "Azure": {
        "keywords": ["azure", "microsoft azure"],
        "category": "cloud",
        "era": "modern",
    },

    # -------------------------------------------------------------------------
    # BIG DATA / HADOOP ECOSYSTEM
    # -------------------------------------------------------------------------
    "Hadoop": {
        "keywords": ["hadoop", "apache hadoop"],
        "category": "big_data",
        "era": "legacy",
    },
    "YARN": {
        "keywords": ["yarn", "hadoop yarn"],
        "category": "big_data",
        "era": "legacy",
    },
    "HBase": {
        "keywords": ["hbase", "apache hbase"],
        "category": "big_data",
        "era": "legacy",
    },
    "Impala": {
        "keywords": ["impala", "apache impala", "cloudera impala"],
        "category": "big_data",
        "era": "legacy",
    },
    "Zookeeper": {
        "keywords": ["zookeeper", "apache zookeeper"],
        "category": "big_data",
        "era": "legacy",
    },
    "Sqoop": {
        "keywords": ["sqoop", "apache sqoop"],
        "category": "big_data",
        "era": "legacy",
    },
    "Flume": {
        "keywords": ["flume", "apache flume"],
        "category": "big_data",
        "era": "legacy",
    },
    "Cloudera": {
        "keywords": ["cloudera", "cdh", "cloudera data platform"],
        "category": "big_data",
        "era": "legacy",
    },
    "Hortonworks": {
        "keywords": ["hortonworks", "hdp"],
        "category": "big_data",
        "era": "legacy",
    },
    "MapR": {
        "keywords": ["mapr"],
        "category": "big_data",
        "era": "legacy",
    },

    # -------------------------------------------------------------------------
    # DATA QUALITY / GOVERNANCE / CATALOG
    # -------------------------------------------------------------------------
    "Great Expectations": {
        "keywords": ["great expectations", "greatexpectations"],
        "category": "data_quality",
        "era": "modern",
    },
    "Monte Carlo": {
        "keywords": ["monte carlo data", "montecarlo data"],
        "category": "data_quality",
        "era": "current",
    },
    "dbt Tests": {
        "keywords": ["dbt test"],
        "category": "data_quality",
        "era": "modern",
    },
    "Soda": {
        "keywords": ["soda.io", "soda data"],
        "category": "data_quality",
        "era": "current",
    },
    "DataHub": {
        "keywords": ["datahub", "linkedin datahub"],
        "category": "data_catalog",
        "era": "current",
    },
    "Atlan": {
        "keywords": ["atlan"],
        "category": "data_catalog",
        "era": "current",
    },
    "Alation": {
        "keywords": ["alation"],
        "category": "data_catalog",
        "era": "modern",
    },
    "Collibra": {
        "keywords": ["collibra"],
        "category": "data_catalog",
        "era": "modern",
    },
    "Apache Atlas": {
        "keywords": ["atlas", "apache atlas"],
        "category": "data_catalog",
        "era": "legacy",
    },
    "Unity Catalog": {
        "keywords": ["unity catalog"],
        "category": "data_catalog",
        "era": "current",
    },
}


# =============================================================================
# DATABASE TAXONOMY
# =============================================================================
# Separate from tech taxonomy for finer-grained analysis of SQL dialects

DATABASE_TAXONOMY = {
    # -------------------------------------------------------------------------
    # RELATIONAL - OPEN SOURCE
    # -------------------------------------------------------------------------
    "PostgreSQL": {
        "keywords": ["postgresql", "postgres", "psql"],
        "category": "relational_oss",
        "era": "legacy",
    },
    "MySQL": {
        "keywords": ["mysql"],
        "category": "relational_oss",
        "era": "legacy",
    },
    "MariaDB": {
        "keywords": ["mariadb"],
        "category": "relational_oss",
        "era": "modern",
    },
    "SQLite": {
        "keywords": ["sqlite"],
        "category": "relational_oss",
        "era": "legacy",
    },
    "CockroachDB": {
        "keywords": ["cockroachdb", "cockroach db"],
        "category": "relational_oss",
        "era": "current",
    },
    "TiDB": {
        "keywords": ["tidb"],
        "category": "relational_oss",
        "era": "current",
    },

    # -------------------------------------------------------------------------
    # RELATIONAL - COMMERCIAL
    # -------------------------------------------------------------------------
    "Oracle": {
        "keywords": ["oracle database", "oracle db", "oracle rdbms", "pl/sql"],
        "category": "relational_commercial",
        "era": "legacy",
    },
    "SQL Server": {
        "keywords": ["sql server", "mssql", "microsoft sql server", "t-sql", "tsql"],
        "category": "relational_commercial",
        "era": "legacy",
    },
    "DB2": {
        "keywords": ["db2", "ibm db2"],
        "category": "relational_commercial",
        "era": "legacy",
    },

    # -------------------------------------------------------------------------
    # NOSQL - DOCUMENT
    # -------------------------------------------------------------------------
    "MongoDB": {
        "keywords": ["mongodb", "mongo"],
        "category": "nosql_document",
        "era": "modern",
    },
    "Couchbase": {
        "keywords": ["couchbase"],
        "category": "nosql_document",
        "era": "modern",
    },
    "CouchDB": {
        "keywords": ["couchdb"],
        "category": "nosql_document",
        "era": "legacy",
    },
    "DynamoDB": {
        "keywords": ["dynamodb", "aws dynamodb"],
        "category": "nosql_document",
        "era": "modern",
    },
    "Firestore": {
        "keywords": ["firestore", "cloud firestore"],
        "category": "nosql_document",
        "era": "modern",
    },

    # -------------------------------------------------------------------------
    # NOSQL - KEY-VALUE
    # -------------------------------------------------------------------------
    "Redis": {
        "keywords": ["redis"],
        "category": "nosql_kv",
        "era": "modern",
    },
    "Memcached": {
        "keywords": ["memcached"],
        "category": "nosql_kv",
        "era": "legacy",
    },
    "etcd": {
        "keywords": ["etcd"],
        "category": "nosql_kv",
        "era": "modern",
    },

    # -------------------------------------------------------------------------
    # NOSQL - WIDE COLUMN
    # -------------------------------------------------------------------------
    "Cassandra": {
        "keywords": ["cassandra", "apache cassandra"],
        "category": "nosql_column",
        "era": "modern",
    },
    "ScyllaDB": {
        "keywords": ["scylladb", "scylla"],
        "category": "nosql_column",
        "era": "current",
    },

    # -------------------------------------------------------------------------
    # NOSQL - GRAPH
    # -------------------------------------------------------------------------
    "Neo4j": {
        "keywords": ["neo4j"],
        "category": "nosql_graph",
        "era": "modern",
    },
    "Neptune": {
        "keywords": ["amazon neptune", "aws neptune"],
        "category": "nosql_graph",
        "era": "modern",
    },
    "JanusGraph": {
        "keywords": ["janusgraph"],
        "category": "nosql_graph",
        "era": "modern",
    },
    "ArangoDB": {
        "keywords": ["arangodb"],
        "category": "nosql_graph",
        "era": "modern",
    },
    "Dgraph": {
        "keywords": ["dgraph"],
        "category": "nosql_graph",
        "era": "modern",
    },

    # -------------------------------------------------------------------------
    # SEARCH
    # -------------------------------------------------------------------------
    "Elasticsearch": {
        "keywords": ["elasticsearch", "elastic search", "elk stack"],
        "category": "search",
        "era": "modern",
    },
    "OpenSearch": {
        "keywords": ["opensearch"],
        "category": "search",
        "era": "current",
    },
    "Solr": {
        "keywords": ["solr", "apache solr"],
        "category": "search",
        "era": "legacy",
    },
    "Algolia": {
        "keywords": ["algolia"],
        "category": "search",
        "era": "modern",
    },
    "Meilisearch": {
        "keywords": ["meilisearch"],
        "category": "search",
        "era": "current",
    },

    # -------------------------------------------------------------------------
    # TIME SERIES
    # -------------------------------------------------------------------------
    "InfluxDB": {
        "keywords": ["influxdb", "influx"],
        "category": "timeseries",
        "era": "modern",
    },
    "TimescaleDB": {
        "keywords": ["timescaledb", "timescale"],
        "category": "timeseries",
        "era": "modern",
    },
    "Prometheus": {
        "keywords": ["prometheus"],
        "category": "timeseries",
        "era": "modern",
    },
    "QuestDB": {
        "keywords": ["questdb"],
        "category": "timeseries",
        "era": "current",
    },
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_all_tech_categories():
    """Return a list of unique technology categories."""
    categories = set()
    for tech, config in TECH_TAXONOMY.items():
        categories.add(config["category"])
    return sorted(categories)


def get_techs_by_category(category):
    """Return all technologies in a given category."""
    return [tech for tech, config in TECH_TAXONOMY.items()
            if config["category"] == category]


def get_techs_by_era(era):
    """Return all technologies from a given era (legacy, modern, current)."""
    return [tech for tech, config in TECH_TAXONOMY.items()
            if config["era"] == era]


def get_roles_by_tier(tier):
    """Return all roles in a given tier."""
    return [role for role, config in ROLE_TAXONOMY.items()
            if config["tier"] == tier]


if __name__ == "__main__":
    # Print summary stats
    print("=" * 60)
    print("TAXONOMY SUMMARY")
    print("=" * 60)

    print(f"\nRoles: {len(ROLE_TAXONOMY)}")
    for tier in sorted(set(c["tier"] for c in ROLE_TAXONOMY.values())):
        roles = get_roles_by_tier(tier)
        print(f"  Tier {tier}: {len(roles)} roles")

    print(f"\nTechnologies: {len(TECH_TAXONOMY)}")
    for cat in get_all_tech_categories():
        techs = get_techs_by_category(cat)
        print(f"  {cat}: {len(techs)}")

    print(f"\nDatabases: {len(DATABASE_TAXONOMY)}")
    categories = set(c["category"] for c in DATABASE_TAXONOMY.values())
    for cat in sorted(categories):
        dbs = [db for db, c in DATABASE_TAXONOMY.items() if c["category"] == cat]
        print(f"  {cat}: {len(dbs)}")
