-- 날짜 차원: 원본 데이터에는 없지만, 분석 편의를 위해 직접 생성하는 테이블
-- Olist 데이터가 2016~2018년 데이터라서, 여유 있게 2016-01-01 ~ 2018-12-31 범위로 생성
with date_spine as (
    select
        -- BigQuery의 GENERATE_DATE_ARRAY로 하루 단위 날짜 배열을 만들고, UNNEST로 한 행씩 풀어줌
        date_day
    from unnest(
        generate_date_array('2016-01-01', '2018-12-31', interval 1 day)
    ) as date_day
)

select
    -- 날짜 자체를 기본 키(primary key)로 사용
    date_day as date_key,

    extract(year from date_day) as year,
    extract(month from date_day) as month,
    extract(day from date_day) as day,

    -- 분기 (1~4)
    extract(quarter from date_day) as quarter,

    -- 요일 (1=일요일 ~ 7=토요일, BigQuery 기본 방식)
    extract(dayofweek from date_day) as day_of_week,

    -- 요일 이름을 사람이 읽기 편하게 텍스트로도 제공 (BI 툴에서 바로 쓰기 좋게)
    format_date('%A', date_day) as day_name,
    format_date('%B', date_day) as month_name,

    -- 주말 여부 (BigQuery 기준 1=일요일, 7=토요일)
    case
        when extract(dayofweek from date_day) in (1, 7) then true
        else false
    end as is_weekend

from date_spine