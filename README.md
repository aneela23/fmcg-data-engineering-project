# FMCG Data Engineering Platform

An end-to-end data engineering project that integrates FMCG sales data from a parent company and an acquired child company.

The project demonstrates data ingestion, data quality, transformation, dimensional modeling, incremental processing, data consolidation, and analytics using modern data engineering technologies.

---

## 📌 Project Overview

This project simulates an FMCG (Fast-Moving Consumer Goods) business scenario where a parent company acquires a child company.

The parent company already has an established analytical data platform, while the child company has data coming from separate source files with different structures and data-quality issues.

The goal is to build a scalable data pipeline that:

- Ingests child-company source data
- Preserves raw data
- Cleans and standardizes data
- Transforms data into business-ready datasets
- Aligns child-company data with the parent-company data model
- Consolidates parent and child data
- Supports analytical and BI workloads

---

## 🎯 Project Objectives

- Build an end-to-end data engineering pipeline
- Implement a Medallion Architecture
- Practice PySpark and SQL transformations
- Implement data-quality rules
- Work with fact and dimension tables
- Implement incremental data processing
- Consolidate data from parent and child companies
- Create analytics-ready datasets
- Build a foundation for BI reporting
- Practice Databricks concepts relevant to the Databricks Data Engineer certification

---

## 🏗️ Technology Stack

| Technology | Purpose |
|---|---|
| PostgreSQL | Relational source database |
| DBeaver | Database development and ER diagrams |
| Python | Data engineering and utility logic |
| SQL | Data modeling, validation and analytics |
| AWS S3 | Data lake / file storage |
| Databricks | Data engineering platform |
| PySpark | Large-scale data transformation |
| Delta Lake | Transactional data storage |
| Airflow / Databricks Workflows | Pipeline orchestration |
| GitHub | Source control and documentation |
| Power BI | Analytics and visualization |

---

## 🏛️ Architecture

The project follows a Medallion Architecture for the child-company data pipeline.

The parent company is represented by an existing analytical data model, while the acquired child company goes through the complete Bronze → Silver → Gold pipeline before being consolidated with the parent-company data.

```text
                    PARENT COMPANY
                    PostgreSQL
                         |
                         v
                  Parent Data Model
                    /    |     \
                   /     |      \
                  v      v       v
             Customers Products Gross Price
                   \      |      /
                    \     |     /
                     v    v    v
                   Fact Orders
                         |
                         |
                         |
                         v
                  Parent Gold Data
                         |
                         |
                         v
              +----------------------+
              |   CONSOLIDATED GOLD  |
              |  Parent + Child Data |
              +----------------------+
                         ^
                         |
                         |
                    CHILD COMPANY
                    Sports Bar
                         |
                         v
                        S3
                         |
                         v
                     BRONZE
                   Raw Data
                         |
                         v
                     SILVER
             Cleaning & Standardization
                         |
                         v
                      GOLD
              Business-Ready Data
                         |
                         v
                Child Gold Data
                         |
                         v
              Parent + Child Merge


---
---

## 🏛️ Architecture
## 📊 Parent Company Data Model

The parent company data represents the existing analytical data model used as the target structure for integrating the acquired child company's data.

### PostgreSQL Source Model

The parent-company data was initially loaded into PostgreSQL using DBeaver.

```text
parent_company
│
├── dim_customers
├── dim_products
├── dim_gross_price
└── fact_orders

