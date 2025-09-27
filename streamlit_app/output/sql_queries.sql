-- 1
SELECT *
FROM ola_clean
WHERE status_norm = 'success';

-- 2
SELECT 
    vehicle_type, 
    AVG(distance_km) AS avg_distance
FROM ola_clean
WHERE distance_km IS NOT NULL
GROUP BY vehicle_type;

-- 3
SELECT COUNT(*) AS cancelled_by_customers
FROM ola_clean
WHERE status_norm = 'canceled by customer';

-- 4
SELECT 
    customer_id, 
    COUNT(*) AS total_rides
FROM ola_clean
GROUP BY customer_id
ORDER BY total_rides DESC
LIMIT 5;

-- 5
SELECT 
    Incomplete_Rides_Reason, 
    COUNT(*) AS total_cancellations
FROM ola_clean
WHERE status_norm = 'canceled by driver'
  AND Incomplete_Rides_Reason IN ('personal issue', 'car issue')
GROUP BY Incomplete_Rides_Reason;

-- 6
SELECT 
    MAX(Driver_Ratings) AS max_rating, 
    MIN(Driver_Ratings) AS min_rating
FROM ola_clean
WHERE vehicle_type = 'Prime Sedan';

-- 7
SELECT *
FROM ola_clean
WHERE payment_method = 'UPI';

-- 8
SELECT 
    vehicle_type, 
    AVG(customer_rating) AS avg_customer_rating
FROM ola_clean
WHERE customer_rating IS NOT NULL
GROUP BY vehicle_type;

-- 9
SELECT 
    SUM(total_amount) AS total_successful_revenue
FROM ola_clean
WHERE status_norm = 'success';

-- 10
SELECT 
    ride_id, 
    Incomplete_Rides_Reason
FROM ola_clean
WHERE Incomplete_Rides IS NOT NULL;
