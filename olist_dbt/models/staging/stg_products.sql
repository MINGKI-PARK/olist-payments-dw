-- staging 모델: raw.products를 정리
-- 원본 CSV의 컬럼명에 오타(lenght)가 있는데, 여기서 바로잡아줌
-- -> 이런 오타 수정도 staging 레이어의 역할: "지저분한 원본"과 "깔끔한 이후 모델들" 사이의 경계
select
    product_id,
    product_category_name,
    product_name_lenght as product_name_length,
    product_description_lenght as product_description_length,
    product_photos_qty,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm

from {{ source('raw', 'products') }}