-- 상품 차원: 상품 정보에 영어 카테고리명을 추가해서 완성
select
    p.product_id,
    p.product_category_name,

    -- 번역 테이블에 없는 카테고리명이 있을 수 있어서 left join 사용
    -- (inner join을 쓰면 번역이 없는 상품이 통째로 사라져버려서, 데이터 유실을 막기 위해 left join 선택)
    t.product_category_name_english,

    p.product_name_length,
    p.product_description_length,
    p.product_photos_qty,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm

from {{ ref('stg_products') }} as p
left join {{ ref('stg_product_category_translation') }} as t
    on p.product_category_name = t.product_category_name