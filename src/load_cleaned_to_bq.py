# pandas: 정제된 Parquet 파일을 읽어서 표 형태(DataFrame)로 다루기 위한 라이브러리
import pandas as pd

# google-cloud-bigquery: 파이썬 코드에서 BigQuery에 데이터를 올리거나 쿼리하기 위한 공식 라이브러리
from google.cloud import bigquery

PROJECT_ID = "olist-payments-dw"
DATASET = "raw"

# 로드할 파일 목록: {정제된 Parquet 폴더 경로: BigQuery에 만들 테이블 이름}
# PySpark로 저장한 Parquet은 폴더 형태(내부에 여러 part 파일)라서
# pandas의 read_parquet()에 폴더 경로를 그대로 넘기면 전체를 하나로 읽어옴
TABLES = {
    "data/processed/olist_order_items_cleaned": "order_items",
    "data/processed/olist_order_payments_cleaned": "order_payments",
}

# BigQuery 클라이언트 생성 (인증은 GOOGLE_APPLICATION_CREDENTIALS 환경변수로 이미 설정된
# 서비스 계정 키를 자동으로 사용함)
client = bigquery.Client(project=PROJECT_ID)

# 딕셔너리를 하나씩 순회하면서 각 테이블을 로드
for parquet_path, table_name in TABLES.items():
    # Parquet 폴더를 통째로 읽어서 pandas DataFrame으로 변환
    df = pd.read_parquet(parquet_path)

    # 데이터를 올릴 BigQuery 테이블의 전체 경로 (프로젝트.데이터셋.테이블 형식)
    table_id = f"{PROJECT_ID}.{DATASET}.{table_name}"

    # WRITE_TRUNCATE: 이미 같은 이름의 테이블이 있으면 기존 데이터를 지우고 새로 씀
    # -> 스크립트를 여러 번 실행해도 데이터가 중복으로 쌓이지 않게 해줌
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")

    # 실제로 BigQuery에 데이터를 올리는 부분 (비동기 작업이라 job 객체를 반환)
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)

    # job.result()를 호출해야 작업이 끝날 때까지 기다림 (안 하면 완료 전에 스크립트가 끝나버릴 수 있음)
    job.result()

    # 몇 개의 행이 어느 테이블에 로드됐는지 확인용 출력
    print(f"{table_name}: {len(df)} rows loaded -> {table_id}")