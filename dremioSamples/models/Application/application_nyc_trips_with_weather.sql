select * from {{ ref('business_transportation_nyc_trips') }} trips
inner join {{ ref('business_weather_nyc') }} weather
on trips.pickup_date = weather."date"