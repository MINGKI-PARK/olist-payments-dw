-- 결제 팩트 테이블: 그레인 = 주문(order_id) 1건의 결제 1회차(payment_sequential)
select
    -- order_id + payment_sequential을 합쳐서 해시값을 만든 서로게이트 키
    -- -> 이 값이 유일(unique)해야만 "결제 1건당 정확히 1행"이라는 그레인이 지켜지고 있다는 뜻
    to_hex(md5(concat(p.order_id, '-', cast(p.payment_sequential as string)))) as payment_key,
    
    p.order_id,
    p.payment_sequential,

    -- 주문 정보에서 고객 id를 가져와서, 나중에 dim_customers와 조인할 수 있게 함
    o.customer_id,

    -- timestamp를 date로 변환해서 dim_date.date_key와 조인 가능하게 맞춤
    date(o.order_purchase_ts) as order_purchase_date,

    p.payment_type,
    p.payment_installments,
    p.payment_value

from {{ ref('stg_order_payments') }} as p

-- inner join을 쓰는 이유: 결제 기록은 반드시 유효한 주문에 속해야 함
-- 만약 order_id가 orders 테이블에 없다면, 그건 데이터 품질 문제이지 "그냥 조인 안 되니 넘어가면 되는" 상황이 아님
-- (product_category_translation 조인 때는 없어도 되는 정보라 left join을 썼지만, 여기는 다름)
inner join {{ ref('stg_orders') }} as o
    on p.order_id = o.order_id