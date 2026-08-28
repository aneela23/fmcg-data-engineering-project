# Data Quality Rules

## Parent Company

The parent-company data was loaded into PostgreSQL and validated for key uniqueness.

| Table | Validation |
|---|---|
| dim_customers | customer_code uniqueness |
| dim_products | product_code uniqueness |
| dim_gross_price | product_code + year uniqueness |
| fact_orders | date + product_code + customer_code uniqueness |

## Child Company

The child-company data will be analyzed and cleaned during the Silver transformation stage.

Expected issues include:

- Duplicate records
- Invalid product IDs
- Inconsistent capitalization
- Incorrect spellings
- Missing values
- Inconsistent naming conventions
- Structural differences between parent and child datasets

Each transformation will be documented as the pipeline is developed.
