-- How fast does the key sensor (Ps30, sensor_11) drift in the last 30 cycles of each in-service engine?
WITH latest AS (
  SELECT engine_id, cycle, sensor_11_slope,
         ROW_NUMBER() OVER (PARTITION BY engine_id ORDER BY cycle DESC) AS rn
  FROM gold.engine_cycle_features
  WHERE split = 'test'
)
SELECT engine_id, cycle AS current_cycle, ROUND(sensor_11_slope, 4) AS ps30_slope_per_cycle,
       NTILE(4) OVER (ORDER BY sensor_11_slope DESC) AS drift_quartile
FROM latest
WHERE rn = 1
ORDER BY sensor_11_slope DESC;
