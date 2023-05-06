-- Write a SQL script that lists all bands with Glam rock as their main style, ranked by their longevity

-- Requirements:

-- Import this table dump: metal_bands.sql
-- Column names must be: band_name and lifespan (in years)
SET SESSION sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));

SELECT origin, SUM(nb_fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
