SELECT station,
       name,
       CAST("date" AS DATE) AS "date",
       awnd,
       prcp,
       snow,
       snwd,
       tempmax,
       tempmin
from {{ source('weather', 'NYC-weather.csv')}}