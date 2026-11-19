-- What does a normal engine life look like (run-to-failure history)?
SELECT COUNT(*) AS engines,
       MIN(observed_cycles) AS min_life, MAX(observed_cycles) AS max_life,
       ROUND(AVG(observed_cycles), 1) AS mean_life,
       PERCENTILE_APPROX(observed_cycles, 0.1) AS p10_life,
       PERCENTILE_APPROX(observed_cycles, 0.5) AS median_life
FROM gold.engine_life_records
WHERE failed = true;
