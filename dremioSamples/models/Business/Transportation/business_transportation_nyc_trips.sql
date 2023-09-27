SELECT vendor_id,
       cast(pickup_datetime as date) as pickup_date,
       pickup_datetime,
       cast(dropoff_datetime as date) as dropoff_date,
       dropoff_datetime,
       passenger_count,
       trip_distance as trip_distance_mi,
       pickup_longitude,
       pickup_latitude,
       rate_code,
       store_and_fwd_flag,
       dropoff_longitude,
       dropoff_latitude,
       case when payment_type in ('CSH','CASH','cash','CAS','Cas') then 'Cash'
       when payment_type in ('CRE','Cre','Credit','CREDIT') then 'Credit'
       when payment_type in ('Dis','DIS','Dispute') then 'Dispute'
       else payment_type END as payment_type,
       fare_amount,
       surcharge,
       mta_tax,
       tip_amount,
       tolls_amount,
       total_amount
FROM   {{ ref('preparation_trips') }}
WHERE  trip_distance BETWEEN 0 AND 360