-- Is utilisation stable? 7-day rolling cycles per aircraft
SELECT tail_id, date, cycles,
       ROUND(AVG(cycles) OVER (PARTITION BY tail_id ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS cycles_7d_avg
FROM gold.aircraft_utilization_daily
ORDER BY tail_id, date;
