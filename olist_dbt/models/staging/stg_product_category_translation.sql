-- staging 모델: 상품 카테고리명 포르투갈어 -> 영어 번역 테이블
select
    product_category_name,
    product_category_name_english

from {{ source('raw', 'product_category_translation') }}