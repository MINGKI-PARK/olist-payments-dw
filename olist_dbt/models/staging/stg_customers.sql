-- staging 모델: raw.customers를 정리
select
    customer_id,
    customer_unique_id,

    -- 우편번호는 숫자가 아니라 "값 그대로의 식별자"라서 문자열로 캐스팅
    -- (숫자로 두면 나중에 평균/합계를 구하는 실수가 생길 수 있고, 앞자리 0이 있는 경우 숫자로는 표현이 깨질 수 있음)
    cast(customer_zip_code_prefix as string) as customer_zip_code_prefix,

    customer_city,
    customer_state

from {{ source('raw', 'customers') }}