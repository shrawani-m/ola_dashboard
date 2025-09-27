-- All successful bookings
SELECT *
FROM ola_clean
WHERE status_norm = 'success';

-- Average ride distance for each vehicle type
SELECT 
    vehicle_type, 
    AVG(distance_km) AS avg_distance
FROM ola_clean
WHERE distance_km IS NOT NULL
GROUP BY vehicle_type;

-- Total number of cancelled rides by customers
SELECT COUNT(*) AS cancelled_by_customers
FROM ola_clean
WHERE status_norm = 'canceled by customer';

-- Top 5 customers who booked the highest number of rides
SELECT 
    customer_id, 
    COUNT(*) AS total_rides
FROM ola_clean
GROUP BY customer_id
ORDER BY total_rides DESC
LIMIT 5;

-- Number of rides cancelled by drivers due to personal and car-related issues
SELECT 
    Incomplete_Rides_Reason, 
    COUNT(*) AS total_cancellations
FROM ola_clean
WHERE status_norm = 'canceled by driver'
  AND Incomplete_Rides_Reason IN ('personal issue', 'car issue')
GROUP BY Incomplete_Rides_Reason;

-- Maximum and Minimum driver ratings for Prime Sedan bookings
SELECT 
    MAX(Driver_Ratings) AS max_rating, 
    MIN(Driver_Ratings) AS min_rating
FROM ola_clean
WHERE vehicle_type = 'Prime Sedan';

-- Rides where payment was made using UPI
SELECT *
FROM ola_clean
WHERE payment_method = 'UPI';

-- Average customer rating per vehicle type
SELECT 
    vehicle_type, 
    AVG(customer_rating) AS avg_customer_rating
FROM ola_clean
WHERE customer_rating IS NOT NULL
GROUP BY vehicle_type;

-- Total booking value of rides completed successfully
SELECT 
    SUM(total_amount) AS total_successful_revenue
FROM ola_clean
WHERE status_norm = 'success';

-- Incomplete rides along with the reason
SELECT 
    ride_id, 
    Incomplete_Rides_Reason
FROM ola_clean
WHERE Incomplete_Rides IS NOT NULL;
