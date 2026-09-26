from pyspark.sql import SparkSession
from pyspark.sql.functions import to_timestamp, col

# Olist orders 데이터셋의 날짜 컬럼들 (원본은 전부 문자열로 들어있음)
DATE_COLUMNS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

def main():
    spark = (
        SparkSession.builder
        .appName("olist-orders-cleaning")
        .master("local[*]")
        .getOrCreate()
    )

    df = spark.read.csv(
        "data/raw/olist_orders_dataset.csv",
        header=True,
        inferSchema=True,
    )

    print(f"원본 행 수: {df.count()}")

    # 1. 날짜 컬럼: 문자열 -> timestamp 타입 변환
    for date_col in DATE_COLUMNS:
        df = df.withColumn(date_col, to_timestamp(col(date_col)))

    # 2. 완전 중복 행 제거
    df = df.dropDuplicates()

    # 3. 핵심 키(order_id)가 비어있는 행 제거
    df = df.filter(col("order_id").isNotNull())

    print(f"클렌징 후 행 수: {df.count()}")

    # 결과를 Parquet으로 저장 (컬럼형 포맷, BigQuery 적재에도 유리)
    df.write.mode("overwrite").parquet("data/processed/olist_orders_cleaned")

    spark.stop()


if __name__ == "__main__":
    main()