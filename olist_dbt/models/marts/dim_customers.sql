-- 고객 차원: staging에서 정리된 고객 정보를 그대로 가져옴
-- 이 모델은 별다른 가공 없이 staging 결과를 마트 레이어로 승격시키는 역할
select
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state

-- source()가 아니라 ref()를 쓰는 이유: raw 테이블이 아니라 우리가 만든 stg_customers 모델을 참조하기 때문
from {{ ref('stg_customers') }}