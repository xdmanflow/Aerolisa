-- Is the model most accurate where it matters (true RUL < 50)? (simulation truth: evaluation only)
SELECT CASE WHEN rul_truth_simulation_only < 50 THEN 'critical (<50)' ELSE 'non-critical' END AS zone,
       COUNT(*) AS engines,
       ROUND(SQRT(AVG(POW(rul_p50 - LEAST(rul_truth_simulation_only, 125), 2))), 2) AS rmse_vs_capped_truth,
       ROUND(AVG(CASE WHEN rul_truth_simulation_only BETWEEN rul_p10 AND rul_p90 THEN 1.0 ELSE 0.0 END), 3) AS raw_coverage
FROM gold.engine_health_snapshot
WHERE is_latest = true
GROUP BY 1;
