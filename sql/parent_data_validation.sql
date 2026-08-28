-- ============================================================
-- FMCG Data Engineering Project
-- Parent Company Data Validation
-- ============================================================

-- 1. Validate customer uniqueness

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT customer_code) AS unique_customer_codes
FROM parent_company.dim_customers;


-- 2. Validate product uniqueness

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT product_code) AS unique_product_codes
FROM parent_company.dim_products;


-- 3. Validate product/year uniqueness

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT (product_code, year)) AS unique_product_years
FROM parent_company.dim_gross_price;


-- 4. Validate fact-order grain

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT (date, product_code, customer_code)) AS unique_order_records
FROM parent_company.fact_orders;
