-- Write a SQL script that ranks country origins of bands, ordered by the number of (non-unique) fans

-- Requirements:

-- Import this table dump: metal_bands.sql.zip
-- Column names must be: origin and nb_fans
-- SET SESSION sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));

SELECT origin, SUM(nb_fans) AS nb_fans
FROM metal_bands
WHERE nb_fans >= 0
GROUP BY origin
ORDER BY nb_fans DESC;
