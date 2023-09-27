select station,
       name,
       CAST("date" AS DATE) AS "date",
       awnd,
       prcp,
       snow,
       snwd,
       tempmax,
       tempmin
from {{ ref('preparation_weather') }}