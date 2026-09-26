import pandas as pd
from google.cloud import bigquery

PROJECT_ID = "olist-payments-dw"
DATASET_ID = "raw"
TABLE_ID = "orders"
PARQUET_DIR = "data/processed/olist_orders_cleaned"

def main():
    # PySpark가 파티션 나눠서 저장한 parquet 파일들을 하나로 합쳐서 읽기
    df = pd.read_parquet(PARQUET_DIR)
    print(f"불러온 행 수: {len(df)}")

    client = bigquery.Client(project=PROJECT_ID)
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",  # 다시 실행해도 덮어쓰기
    )

    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()  # 완료될 때까지 대기

    table = client.get_table(table_ref)
    print(f"적재 완료: {table_ref} ({table.num_rows}행)")


if __name__ == "__main__":
    main()