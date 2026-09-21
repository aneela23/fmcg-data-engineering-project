# Architecture

This folder contains the architecture and data-model diagrams for the **Retail Acquisition Data Integration Platform**.

The project integrates an existing parent-company analytical model with data from an acquired company using AWS S3 and Databricks.

## End-to-End Architecture

The acquired-company data is ingested from AWS S3 and processed through the Databricks **Bronze, Silver, and Gold** layers before being integrated with the parent-company data in the consolidated Gold layer.

[View End-to-End Data Architecture](images/end-to-end-data-architecture.png)

## Parent Company Data Model

The parent-company data originates from PostgreSQL and follows a dimensional model containing customer, product, pricing, date, and order data.

[View Parent Company Data Model](images/parent-company-data-model.png)

## Incremental Order Processing

New order files are processed incrementally using an S3 landing/processed pattern, Bronze historical storage, staging tables, Silver transformations, Delta Lake MERGE operations, and Gold consolidation.

[View Incremental Processing Architecture](images/incremental-processing-architecture.png)
