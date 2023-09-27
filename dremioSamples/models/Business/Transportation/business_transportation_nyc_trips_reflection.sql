 -- depends_on: {{ ref('business_transportation_nyc_trips') }}
{{
    config(
        materialized='reflection',
        reflection_type='aggregate',
        dimensions=['pickup_date', 'store_and_fwd_flag', 'vendor_id', 'payment_type', 'dropoff_date', 'rate_code'],
        dimensions_by_day=[ 'pickup_datetime', 'dropoff_datetime' ],
        measures=['dropoff_latitude', 'pickup_latitude', 'dropoff_longitude', 'pickup_longitude', 'total_amount',
         'trip_distance_mi', 'tip_amount', 'fare_amount', 'tolls_amount', 'surcharge', 'mta_tax', 'passenger_count']
	)
}}
