-- This model cleans up the raw sales data
SELECT
    order_id,
    TRIM(customer_name) AS customer_name,
    LOWER(product_name) AS product_name,
    category,
    amount,
    CAST(order_date AS DATE) AS order_date
FROM {{ ref('raw_sales') }}