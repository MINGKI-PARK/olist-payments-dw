-- staging 모델: raw.order_payments를 정리
select
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    cast(payment_value as float64) as payment_value

from {{ source('raw', 'order_payments') }}