-- This model calculates total spending per customer
SELECT
    customer_name,
    COUNT(order_id) AS total_orders,
    SUM(amount) AS total_spent
FROM {{ ref('stg_sales') }}
GROUP BY customer_name