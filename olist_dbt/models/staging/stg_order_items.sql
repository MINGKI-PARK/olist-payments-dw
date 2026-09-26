-- staging 모델: raw.order_items를 정리
select
    order_id,
    order_item_id,
    product_id,
    seller_id,

    -- 이미 클렌징 단계(PySpark)에서 timestamp로 캐스팅했지만,
    -- staging 레이어에서도 명시적으로 다시 캐스팅해서 "이 컬럼은 반드시 timestamp"라는 걸 코드로 보장함
    -- (원본 로딩 방식이 바뀌어도 이 한 줄 덕분에 안전함)
    cast(shipping_limit_date as timestamp) as shipping_limit_date,

    cast(price as float64) as price,
    cast(freight_value as float64) as freight_value

from {{ source('raw', 'order_items') }}