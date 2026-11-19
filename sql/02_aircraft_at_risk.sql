-- Which aircraft carry the riskiest engine, and when is their next slot?
SELECT r.tail_id,
       MAX(r.risk_before_check)                       AS worst_engine_risk,
       SUM(CASE WHEN r.band = 'RED' THEN 1 ELSE 0 END) AS engines_in_red,
       MIN(r.next_check_date)                         AS next_check_date,
       ROUND(AVG(r.cycles_per_day), 2)                AS cycles_per_day
FROM gold.inspection_recommendation r
GROUP BY r.tail_id
HAVING SUM(CASE WHEN r.band = 'RED' THEN 1 ELSE 0 END) > 0
ORDER BY worst_engine_risk DESC, next_check_date;
