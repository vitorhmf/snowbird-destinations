-- DIMENTIONS TABLES

--Dim City
CREATE TABLE analytics.dim_city AS 
SELECT 
    city,
    country,
    population,
    size
FROM cities_metrics;

--Dim Country
CREATE TABLE analytics.dim_country AS
WITH snowbird_period AS (
    SELECT 
        country,
        parameter,
        AVG(dec) AS dec_avg,
        AVG(jan) AS jan_avg,
        AVG(feb) AS feb_avg
    FROM analytics.fact_weather
    WHERE city <> 'Wisconsin'
    GROUP BY country, parameter
),
pivot_weather as (
    SELECT
        country,
        AVG(CASE WHEN parameter = 'wind_speed' THEN dec_avg END) AS wind_speed_dec,
        AVG(CASE WHEN parameter = 'wind_speed' THEN jan_avg END) AS wind_speed_jan,
        AVG(CASE WHEN parameter = 'wind_speed' THEN feb_avg END) AS wind_speed_feb,
        AVG(CASE WHEN parameter = 'humidity' THEN dec_avg END) AS humidity_dec,
        AVG(CASE WHEN parameter = 'humidity' THEN jan_avg END) AS humidity_jan,
        AVG(CASE WHEN parameter = 'humidity' THEN feb_avg END) AS humidity_feb,
        AVG(CASE WHEN parameter = 'temperature' THEN dec_avg END) AS temperature_dec,
        AVG(CASE WHEN parameter = 'temperature' THEN jan_avg END) AS temperature_jan,
        AVG(CASE WHEN parameter = 'temperature' THEN feb_avg END) AS temperature_feb
    FROM snowbird_period
    GROUP BY country
),
pivot_life as (
    select
        country,
        AVG(CASE WHEN "group" = 'environment' THEN score END) AS environment,
        AVG(CASE WHEN "group" = 'security' THEN score END) AS security,
        AVG(CASE WHEN "group" = 'people' THEN score END) AS people
    from analytics.fact_life
    group by country
)
select 
    distinct cm.country,
    cm.currency,
    cm.usd_quote,
    pm.wind_speed_dec,
    pm.wind_speed_jan,
    pm.wind_speed_feb,
    pm.humidity_dec,
    pm.humidity_jan,
    pm.humidity_feb,
    pm.temperature_dec,
    pm.temperature_jan,
    pm.temperature_feb,
    pl.environment,
    pl.people,
    pl.security
from cities_metrics cm
left join pivot_weather pm
    on cm.country = pm.country
left join pivot_life pl
    on cm.country = pl.country

--FACT TABLES
--Fact Life
CREATE TABLE analytics.fact_life AS 
with
impact as (
    select 
        distinct indicator,
        case 
            when indicator in ('Air pollution', 'Homicide rate') then -1
            else 1
        end as impact
    from countries_metrics 
),
score as (
    select
        distinct rank,
        case 
            when rank=1 then 25
            when rank=2 then 10
            when rank=3 then 5
            when rank=4 then 2
            else 1
        end as score
    from countries_metrics
),
final_score as (
    select
        case when c.country = 'Mexico' then 'Belize' else c.country end as country,     --Mexico represented the Central America
        c.group,
        c.indicator,
        i.impact,
        c.unit,
        c.value,
        c.rank,
        s.score,
        (i.impact * c.rank * s.score) as final_score
    from countries_metrics c
    left join impact i
        on c.indicator = i.indicator
    left join score s
        on c.rank = s.rank
)
select
    fs.country,
    fs.group,
    sum(final_score) as score
from final_score fs
group by 1,2

--Fact Weather
CREATE TABLE analytics.fact_weather AS 
with
data_fixed as (
    select
        case 
            when region = 'Florida' then 'Broward'
            when region = 'California' then 'Los Angeles'
            else region
        end as city,
        parameter,
        cast(jan as float),
        cast(feb as float),
        mar,apr,may,jun,jul,aug,sep,oct,nov,
        cast(dec as float)
    from weather
)
select
    coalesce(cm.country, 'United States') as country,
    df.*
from data_fixed df
left join cities_metrics cm
    on df.city = cm.city

--Fact Listings
CREATE TABLE analytics.fact_listings AS
select distinct
    l.*,
    cm.country
from listings l
left join cities_metrics cm
    on l.city = cm.city