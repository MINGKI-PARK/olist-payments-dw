# PySpark: 대용량 데이터 처리를 위한 분산 처리 프레임워크
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# SparkSession: Spark 작업을 시작하는 진입점
# .master("local[*]") -> 내 컴퓨터의 모든 CPU 코어를 써서 로컬로 실행
spark = (
    SparkSession.builder.appName("clean_order_payments")
    .master("local[*]")
    .getOrCreate()
)

# CSV 파일을 Spark 데이터프레임으로 읽어오기
# header=True -> 첫 줄을 컬럼명으로 사용
# inferSchema=True -> 각 컬럼의 데이터 타입을 자동으로 추론
df = spark.read.csv(
    "data/raw/olist_order_payments_dataset.csv", header=True, inferSchema=True
)

# 데이터 클렌징(정제) 작업
df_clean = (
    df
    # payment_value(결제 금액)를 double(소수점 있는 숫자) 타입으로 명시적으로 캐스팅
    # -> CSV에서 자동 추론된 타입이 부정확할 수 있어서, 금액처럼 계산에 쓰이는 컬럼은 직접 타입을 지정해주는 게 안전함
    .withColumn("payment_value", col("payment_value").cast("double"))
    # 완전히 똑같은 행이 중복으로 들어있으면 하나만 남기고 제거
    .dropDuplicates()
    # order_id가 비어있는(null) 행은 제외
    # -> order_id는 다른 테이블(orders, order_items)과 조인할 때 쓰이는 핵심 키라서 비어있으면 안 됨
    .filter(col("order_id").isNotNull())
)

# 정제된 데이터를 Parquet 형식으로 저장 (CSV보다 용량 작고 읽는 속도가 빠른 분석용 포맷)
# mode("overwrite") -> 같은 경로에 파일이 이미 있으면 덮어쓰기
df_clean.write.mode("overwrite").parquet(
    "data/processed/olist_order_payments_cleaned"
)

# 최종적으로 몇 개의 행이 남았는지 콘솔에 출력해서 확인
print(f"Cleaned rows: {df_clean.count()}")

# Spark 세션 종료 (리소스 정리)
spark.stop()