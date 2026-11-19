-- How many engines are in each band, and how urgent are they?
SELECT band,
       COUNT(*)                              AS engines,
       ROUND(AVG(rul_p10), 1)                AS avg_p10_cycles,
       ROUND(MIN(days_p10), 1)               AS min_days_p10,
       ROUND(AVG(risk_before_check) * 100, 1) AS avg_risk_pct
FROM gold.inspection_recommendation
GROUP BY band
ORDER BY CASE band WHEN 'RED' THEN 1 WHEN 'AMBER' THEN 2 ELSE 3 END;
