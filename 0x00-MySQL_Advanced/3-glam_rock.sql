-- Write a SQL script that lists all bands with Glam rock as their main style, ranked by their longevity

-- Requirements:

-- Import this table dump: metal_bands.sql
-- Column names must be: band_name and lifespan (in years)
SELECT band_name, 
       YEAR(MAX(year)) - YEAR(MIN(year)) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
GROUP BY band_name
ORDER BY lifespan DESC;
