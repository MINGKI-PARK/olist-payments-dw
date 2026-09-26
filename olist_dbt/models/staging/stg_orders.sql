-- staging 모델: raw.orders 테이블을 가져와서 컬럼명 정리 + 타입 캐스팅만 하는 단계
-- 여기서는 조인이나 집계 같은 복잡한 로직을 넣지 않고, "원본을 다루기 좋게 다듬는" 역할만 함

select
    -- 원본 컬럼명을 그대로 쓰되, 필요하면 더 명확한 이름으로 바꿀 수 있음
    order_id,
    customer_id,
    order_status,

    -- timestamp 관련 컬럼들을 명시적으로 캐스팅
    -- (BigQuery에 로드될 때 문자열로 들어왔을 수도 있어서, 날짜 계산에 쓰기 전에 타입을 확실히 맞춰줌)
    cast(order_purchase_timestamp as timestamp) as order_purchase_ts,
    cast(order_approved_at as timestamp) as order_approved_ts,
    cast(order_delivered_carrier_date as timestamp) as order_delivered_carrier_ts,
    cast(order_delivered_customer_date as timestamp) as order_delivered_customer_ts,
    cast(order_estimated_delivery_date as timestamp) as order_estimated_delivery_ts

-- source() 함수로 raw 데이터셋의 orders 테이블을 참조
-- 하드코딩된 테이블 경로 대신 이렇게 쓰면, _sources.yml만 고치면 모든 모델에 반영됨
from {{ source('raw', 'orders') }}