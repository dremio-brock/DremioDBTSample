-- depends_on: {{ ref('business_weather_nyc') }}
{{
    config(
        materialized='reflection',
        reflection_type='aggregate',
        dimensions=['pickup_date', 'store_and_fwd_flag', 'vendor_id', 'payment_type', 'dropoff_date', 'rate_code'],
        dimensions_by_day=[ 'pickup_datetime', 'dropoff_datetime' ]
	)
}}