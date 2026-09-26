-- 판매자 차원: staging에서 정리된 판매자 정보를 그대로 마트 레이어로 승격
select
    seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state

from {{ ref('stg_sellers') }}