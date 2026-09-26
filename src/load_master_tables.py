import pandas as pd
from google.cloud import bigquery

PROJECT_ID = "olist-payments-dw"
DATASET = "raw"

TABLES = {
    "data/raw/olist_customers_dataset.csv": "customers",
    "data/raw/olist_sellers_dataset.csv": "sellers",
    "data/raw/olist_products_dataset.csv": "products",
    "data/raw/product_category_name_translation.csv": "product_category_translation",
}

client = bigquery.Client(project=PROJECT_ID)

for csv_path, table_name in TABLES.items():
    df = pd.read_csv(csv_path)
    table_id = f"{PROJECT_ID}.{DATASET}.{table_name}"

    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()

    print(f"{table_name}: {len(df)} rows loaded -> {table_id}")