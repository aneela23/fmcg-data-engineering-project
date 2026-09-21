# Data Quality Rules

Data-quality checks are applied across the parent-company source data and acquired-company transformation pipeline to ensure reliable data before consolidation into the Gold layer.

## Parent Company

Parent-company data was validated in PostgreSQL before integration.

| Table | Validation |
|---|---|
| `dim_customers` | `customer_code` uniqueness and null checks |
| `dim_products` | `product_code` uniqueness and null checks |
| `dim_gross_price` | `product_code + year` uniqueness and null checks |
| `fact_orders` | `date + product_code + customer_code` uniqueness and null checks |

Fact-to-dimension relationships were also validated between orders, customers, and products.

## Acquired Company

Data-quality issues are handled primarily during the Databricks Silver transformation stage.

### Customer Data
- Removed duplicate customer records
- Trimmed and standardized customer names
- Standardized city values
- Corrected missing city values
- Standardized data types
- Aligned customer attributes with the parent-company model

### Product Data
- Removed duplicate products
- Handled invalid product identifiers
- Standardized product and category names
- Separated product and variant information
- Standardized division values
- Aligned the schema with the parent-company product dimension

### Pricing Data
- Validated product identifiers and pricing values
- Standardized pricing data types
- Derived the required time attributes
- Aligned acquired-company pricing with the parent-company pricing model

### Order Data
- Standardized order dates, customer codes, product codes, and quantities
- Processed historical and incremental order batches separately
- Used staging tables to isolate newly arriving records
- Moved successfully processed source files from S3 `landing` to `processed`
- Used Delta Lake MERGE operations to prevent unnecessary full-table reprocessing

## Gold-Layer Validation

Before analytics consumption, the consolidated Gold layer is checked for:

- Schema consistency between parent and acquired-company data
- Valid customer and product identifiers
- Duplicate business keys
- Required field completeness
- Successful incremental record processing
- Fact and dimension compatibility
