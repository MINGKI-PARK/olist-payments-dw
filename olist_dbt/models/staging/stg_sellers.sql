-- staging 모델: raw.sellers를 정리 (customers와 구조가 거의 같음)
select
    seller_id,

    -- customers와 같은 이유로 우편번호는 문자열로 캐스팅
    cast(seller_zip_code_prefix as string) as seller_zip_code_prefix,

    seller_city,
    seller_state

from {{ source('raw', 'sellers') }}