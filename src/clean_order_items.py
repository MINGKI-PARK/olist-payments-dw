# PySpark: 대용량 데이터 처리를 위한 분산 처리 프레임워크
# 여기서는 단일 로컬 머신에서 실행하지만, 실무에서는 여러 서버(클러스터)에 나눠서 처리 가능
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_timestamp

# SparkSession: Spark 작업을 시작하기 위한 진입점(entry point)
# .master("local[*]") -> 별도 클러스터 없이 내 컴퓨터의 모든 CPU 코어를 써서 로컬로 실행하겠다는 뜻
spark = (
    SparkSession.builder.appName("clean_order_items")
    .master("local[*]")
    .getOrCreate()
)

# CSV 파일을 Spark 데이터프레임으로 읽어오기
# header=True -> 첫 번째 줄을 컬럼명으로 사용
# inferSchema=True -> 각 컬럼의 데이터 타입(숫자/문자/날짜 등)을 자동으로 추론
df = spark.read.csv(
    "data/raw/olist_order_items_dataset.csv", header=True, inferSchema=True
)

# 데이터 클렌징(정제) 작업
df_clean = (
    # shipping_limit_date 컬럼을 문자열이 아닌 실제 timestamp(날짜/시간) 타입으로 변환
    # -> 나중에 날짜 기준으로 필터링하거나 계산할 때 필요
    df.withColumn("shipping_limit_date", to_timestamp("shipping_limit_date"))
    # 완전히 똑같은 행(row)이 중복으로 들어있으면 하나만 남기고 제거
    .dropDuplicates()
    # order_id, product_id, seller_id 중 하나라도 비어있는(null) 행은 제외
    # -> 이 컬럼들은 나중에 다른 테이블과 조인(join)할 때 쓰이는 핵심 키라서 비어있으면 안 됨
    .filter(
        df.order_id.isNotNull()
        & df.product_id.isNotNull()
        & df.seller_id.isNotNull()
    )
)

# 정제된 데이터를 Parquet 형식으로 저장
# Parquet: CSV보다 용량이 작고 읽는 속도가 빠른 컬럼 기반 저장 포맷 (분석용 데이터에 널리 사용)
# mode("overwrite") -> 같은 경로에 이미 파일이 있으면 덮어쓰기
df_clean.write.mode("overwrite").parquet("data/processed/olist_order_items_cleaned")

# 최종적으로 몇 개의 행이 남았는지 콘솔에 출력해서 확인
print(f"Cleaned rows: {df_clean.count()}")

# Spark 세션 종료 (리소스 정리)
spark.stop()