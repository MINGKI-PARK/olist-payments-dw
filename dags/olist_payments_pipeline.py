"""
Olist Payments DW 파이프라인 DAG

이 DAG가 하는 일:
1. 마스터(차원) 테이블을 BigQuery에 적재 (고객/판매자/상품/카테고리)
2. PySpark로 주문(orders), 주문상품(order_items), 주문결제(order_payments) 데이터 정제
3. 정제된 데이터를 BigQuery raw 데이터셋에 적재
4. dbt로 스타 스키마(스테이징 -> 마트) 변환
5. dbt test로 데이터 품질 검증
"""

from datetime import timedelta

import pendulum
from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator

# 스크립트들이 상대경로로 파일을 읽고 쓰기 때문에,
# 반드시 이 폴더를 작업 디렉토리(cwd)로 지정해줘야 정상 동작함
PROJECT_DIR = "/home/ubuntu/projects/olist-payments-dw"
DBT_DIR = f"{PROJECT_DIR}/olist_dbt"

default_args = {
    "owner": "mingki",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="olist_payments_pipeline",
    description="Olist 결제 데이터 파이프라인: 수집 -> PySpark 정제 -> BigQuery 적재 -> dbt 변환/테스트",
    default_args=default_args,
    schedule=None,  # 우선 수동 실행만 (나중에 필요하면 "@daily" 등으로 변경 가능)
    start_date=pendulum.datetime(2026, 1, 1, tz="Asia/Seoul"),
    catchup=False,  # 과거 날짜 몰아서 실행하지 않음
    tags=["olist", "portfolio"],
) as dag:

    # 1. 마스터(차원) 테이블 적재 - 다른 작업과 독립적
    load_master_tables = BashOperator(
        task_id="load_master_tables",
        bash_command="uv run python src/load_master_tables.py",
        cwd=PROJECT_DIR,
    )

    # 2. PySpark 정제 작업 (3개 모두 서로 독립적 -> 병렬 실행 가능)
    clean_orders = BashOperator(
        task_id="clean_orders",
        bash_command="uv run python src/clean.py",
        cwd=PROJECT_DIR,
    )

    clean_order_items = BashOperator(
        task_id="clean_order_items",
        bash_command="uv run python src/clean_order_items.py",
        cwd=PROJECT_DIR,
    )

    clean_order_payments = BashOperator(
        task_id="clean_order_payments",
        bash_command="uv run python src/clean_order_payments.py",
        cwd=PROJECT_DIR,
    )

    # 3. 정제된 데이터를 BigQuery에 적재
    load_orders_to_bq = BashOperator(
        task_id="load_orders_to_bq",
        bash_command="uv run python src/load_to_bq.py",
        cwd=PROJECT_DIR,
    )

    load_cleaned_to_bq = BashOperator(
        task_id="load_cleaned_to_bq",
        bash_command="uv run python src/load_cleaned_to_bq.py",
        cwd=PROJECT_DIR,
    )

    # 4. dbt 변환 (스테이징 -> 마트, 스타 스키마 생성)
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="uv run dbt run",
        cwd=DBT_DIR,
    )

    # 5. dbt 데이터 품질 테스트
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="uv run dbt test",
        cwd=DBT_DIR,
    )

    # ---- 의존관계 설정 ----
    # orders 정제가 끝나야 orders 적재 가능
    clean_orders >> load_orders_to_bq

    # order_items, order_payments 정제가 "둘 다" 끝나야 한번에 적재
    [clean_order_items, clean_order_payments] >> load_cleaned_to_bq

    # 모든 raw 데이터(마스터 + orders + cleaned)가 다 올라가야 dbt 실행
    [load_master_tables, load_orders_to_bq, load_cleaned_to_bq] >> dbt_run

    # dbt 실행 후 테스트
    dbt_run >> dbt_test