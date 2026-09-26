-- 주문 상품 팩트 테이블: 그레인 = 주문(order_id) 1건 안의 상품 1개(order_item_id)
select
    -- order_id + order_item_id를 합쳐서 만든 서로게이트 키
    to_hex(md5(concat(oi.order_id, '-', cast(oi.order_item_id as string)))) as order_item_key,

    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    oi.seller_id,

    o.customer_id,
    date(o.order_purchase_ts) as order_purchase_date,

    oi.price,
    oi.freight_value

from {{ ref('stg_order_items') }} as oi

-- 위와 같은 이유로 inner join: 주문 상품은 반드시 유효한 주문에 속해야 함
inner join {{ ref('stg_orders') }} as o
    on oi.order_id = o.order_id